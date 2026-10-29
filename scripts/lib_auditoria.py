"""Biblioteca comum da auditoria 2026: carga, regressao com efeito fixo, contrastes com placebo, correcao de p."""
import os
import numpy as np
import pandas as pd
from scipy import stats

KEY = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
MARGEM = 4_430_191
Z95 = 1.645  # limite superior unilateral 95%


class NaoExecutado(Exception):
    """Teste que nao pode rodar: o runner registra o motivo, imprime em stderr e encerra com codigo != 0."""


def carrega(dirp, anos=(2014, 2018, 2022, 2026)):
    D = {}
    for a in anos:
        for t in (1, 2):
            p = os.path.join(dirp, f"bu_{a}_t{t}.parquet")
            if not os.path.exists(p):
                raise NaoExecutado(f"falta {p}")
            D[(a, t)] = pd.read_parquet(p)
    return D


def base(d, minvalid=30, exterior=False):
    """Secoes apuradas com votos validos suficientes para share. Exterior fora por padrao (fuso e perfil proprios)."""
    m = d.DS_TIPO_URNA.str.upper().eq("APURADA") & (d.valid2 >= minvalid) & (d.QT_APTOS > 0)
    if not exterior:
        m &= d.SG_UF != "ZZ"
    return d[m]


def par_ano(D, ano, minvalid=30):
    """Largo: T2 com colunas do T1 (sufixo _t1), mesmas secoes."""
    t1 = D[(ano, 1)].set_index(KEY)
    t2 = D[(ano, 2)].set_index(KEY)
    cols = ["lula", "dir", "lula_sh", "valid2", "turnout", "manual_rate", "QT_APTOS", "QT_COMPARECIMENTO", "atraso_min", "nominal", "branco", "nulo"]
    w = t2.join(t1[cols], rsuffix="_t1", how="inner").reset_index()
    w = w[w.DS_TIPO_URNA.str.upper().eq("APURADA") & (w.SG_UF != "ZZ") & (w.valid2 >= minvalid) &
          (w.valid2_t1 >= minvalid) & (w.QT_APTOS > 0)]
    w["lula_pa"] = w.lula / w.QT_APTOS
    w["dir_pa"] = w["dir"] / w.QT_APTOS
    w["lula_pa_t1"] = w.lula_t1 / w.QT_APTOS_t1
    w["dir_pa_t1"] = w["dir_t1"] / w.QT_APTOS_t1
    w["outros_pa_t1"] = (w.nominal_t1 - w.lula_t1 - w.dir_t1) / w.QT_APTOS_t1      # votos T1 em outros candidatos, por apto
    w["bn_pa_t1"] = (w.branco_t1 + w.nulo_t1) / w.QT_APTOS_t1                      # brancos e nulos T1, por apto
    return w


def fe_ols(df, y, xs, group, cluster=None):
    """OLS com efeito fixo por 'group' (within) e erro padrao CR1 agrupado por 'cluster' (padrao = group).
    Retorna DataFrame com coef, se, z, p (normal) e n, grupos. Levanta ValueError se amostra insuficiente."""
    cluster = cluster or group
    cols = list(dict.fromkeys([y] + xs + [group, cluster]))
    d = df[cols].replace([np.inf, -np.inf], np.nan).dropna()
    d = d[d.groupby(group)[y].transform("size") > 1]
    if len(d) < 200 or d[group].nunique() < 20:
        raise ValueError(f"amostra insuficiente para {y} ~ {xs} | {group}: n={len(d)}")
    g = d.groupby(group)
    Y = (d[y] - g[y].transform("mean")).values
    X = np.column_stack([(d[x] - g[x].transform("mean")).values for x in xs])
    if np.linalg.matrix_rank(X) < X.shape[1]:
        raise ValueError(f"colineariedade em {xs} (variacao intra-grupo insuficiente)")
    b, *_ = np.linalg.lstsq(X, Y, rcond=None)
    e = Y - X @ b
    cl = d[cluster].values
    order = np.argsort(cl, kind="stable")
    cs = cl[order]
    starts = np.r_[0, np.flatnonzero(cs[1:] != cs[:-1]) + 1]
    sc = np.add.reduceat(X[order] * e[order, None], starts, axis=0)
    G, N, K = len(starts), len(d), X.shape[1]
    bread = np.linalg.inv(X.T @ X)
    V = bread @ (sc.T @ sc) @ bread * (G / (G - 1)) * ((N - 1) / (N - K))
    se = np.sqrt(np.diag(V))
    z = b / se
    return pd.DataFrame({"coef": b, "se": se, "z": z, "p": 2 * stats.norm.sf(np.abs(z))}, index=xs).assign(n=N, grupos=G)


def pool_placebos(ests):
    """Media ponderada pelo inverso da variancia de [(b, se), ...]. Retorna (b0, se0)."""
    w = np.array([1 / s ** 2 for _, s in ests])
    b = np.array([b for b, _ in ests])
    return float((w * b).sum() / w.sum()), float(1 / np.sqrt(w.sum()))


def contraste(b, se, placebos):
    """Diferenca entre a estimativa de 2026/T2 e o placebo agrupado. Retorna (diff, se_diff, z, p).
    Conservador: trata as amostras como independentes (T1 e T2 do mesmo ano compartilham secoes)."""
    b0, se0 = pool_placebos(placebos)
    diff = b - b0
    sed = float(np.sqrt(se ** 2 + se0 ** 2))
    z = diff / sed
    return diff, sed, z, float(2 * stats.norm.sf(abs(z)))


def votos_max(diff, sed, exposicao, fator_margem=2.0):
    """Limite superior (95% unilateral) em votos de margem: fator * max(0, diff + 1.645*sed) * exposicao."""
    return float(fator_margem * max(0.0, diff + Z95 * sed) * exposicao)


class Registro:
    """Acumula os testes primarios. Cada teste e comparado com CADA placebo (teste de interseção-uniao):
    p_excesso = max dos p unilaterais (estimativa 2026/T2 > placebo); so ha evidencia de excesso se superar todos.
    Holm e Benjamini-Hochberg sao aplicados a p_excesso sobre toda a familia."""

    def __init__(self):
        self.rows = []

    def add(self, h, teste, est, ep, placebos, expo=np.nan, fator=2.0, nota="", sentido="PT", ressalva=""):
        """placebos: lista de (nome, b, se). expo: exposicao (soma de votos validos ou equivalente) para converter em votos."""
        pr = []
        for nome, b0, s0 in placebos:
            diff = est - b0
            sed = float(np.hypot(ep, s0))
            pr.append(dict(nome=nome, b=b0, se=s0, diff=diff, sed=sed, z=diff / sed, p1=float(stats.norm.sf(diff / sed)),
                           p2=float(2 * stats.norm.sf(abs(diff / sed)))))
        ex = max(pr, key=lambda r: r["b"])      # placebo mais exigente (maior estimativa)
        fr = min(pr, key=lambda r: r["b"])      # placebo mais frouxo
        v_ex = votos_max(ex["diff"], ex["sed"], expo, fator) if expo == expo else np.nan
        v_fr = votos_max(fr["diff"], fr["sed"], expo, fator) if expo == expo else np.nan
        cen = fator * ex["diff"] * expo if expo == expo else np.nan                       # estimativa central (vs placebo mais exigente)
        ci_inf = fator * (ex["diff"] - 1.96 * ex["sed"]) * expo if expo == expo else np.nan
        ci_sup = fator * (ex["diff"] + 1.96 * ex["sed"]) * expo if expo == expo else np.nan
        self.rows.append(dict(
            votos_central=cen, votos_ic95_inf=ci_inf, votos_ic95_sup=ci_sup,
            H=h, teste=teste, est_2026T2=est, ep=ep, comparador_exigente=ex["nome"], b_comp=ex["b"], ep_comp=ex["se"],
            placebos=" | ".join(f"{r['nome']}: {r['b']:.5f} (ep {r['se']:.5f}, p_exc {r['p1']:.3g})" for r in pr),
            p_bruto_2lados=max(r["p2"] for r in pr), p_excesso=max(r["p1"] for r in pr),
            votos_max_margem=v_ex, pct_margem=100 * v_ex / MARGEM if v_ex == v_ex else np.nan,
            votos_max_pior_caso=v_fr, pct_pior_caso=100 * v_fr / MARGEM if v_fr == v_fr else np.nan, nota=nota, sentido=sentido, ressalva=ressalva))

    def add_raw(self, h, teste, est, ep, p_excesso, p_bruto=np.nan, votos=np.nan, votos_pior=np.nan, nota="", comp="", placebos="", sentido="PT", ressalva=""):
        self.rows.append(dict(H=h, teste=teste, est_2026T2=est, ep=ep, comparador_exigente=comp, b_comp=np.nan, ep_comp=np.nan,
                              placebos=placebos, p_bruto_2lados=p_bruto, p_excesso=p_excesso, votos_max_margem=votos,
                              pct_margem=100 * votos / MARGEM if votos == votos else np.nan, votos_max_pior_caso=votos_pior,
                              pct_pior_caso=100 * votos_pior / MARGEM if votos_pior == votos_pior else np.nan, nota=nota, sentido=sentido, ressalva=ressalva))

    def frame(self):
        df = pd.DataFrame(self.rows)
        if df.empty:
            return df
        p = df.p_excesso.values
        n = len(p)
        order = np.argsort(p)
        holm = np.empty(n); run = 0.0
        for rank, i in enumerate(order):
            run = max(run, min(1.0, (n - rank) * p[i])); holm[i] = run
        bh = np.empty(n); prev = 1.0
        for rank in range(n - 1, -1, -1):
            i = order[rank]; prev = min(prev, p[i] * n / (rank + 1)); bh[i] = min(1.0, prev)
        df["p_holm"] = holm; df["p_bh"] = bh
        sem_voto = df.pct_pior_caso.isna()
        rel = df.pct_pior_caso.fillna(0) >= 1.0          # relevante: o pior caso explicaria >= 1% da margem
        det = df.p_holm < 0.05
        df["veredito"] = np.select(
            [sem_voto & det, sem_voto & ~det, det & rel, det & ~rel, ~det & ~rel, ~det & rel],
            ["EXCESSO DETECTADO (teste de forma, sem conversao em votos)", "SEM EXCESSO (teste de forma, sem conversao em votos)",
             "EXCESSO DETECTADO e relevante (pior caso >= 1% da margem)", "excesso detectavel, magnitude irrelevante (<1% da margem)",
             "REFUTADA (sem excesso, teto <1% da margem)", "INCONCLUSIVA (sem excesso, mas teto >=1% da margem)"],
            default="?")
        return df
