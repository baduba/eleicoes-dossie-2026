#!/usr/bin/env python3
"""Runner das hipoteses. Uso:
  python -I 02_executa.py DIR_PARQUET DIR_SAIDA --anos 2022 2026 --h H1 H2 H3 H4 ...
Cada hipotese roda isolada. Falha => mensagem em stderr, linha em nao_executados.csv e codigo de saida 2 ao final.
Nunca pula em silencio."""
import argparse, importlib, json, os, sys, time, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from lib_auditoria import carrega, Registro, NaoExecutado

MODULOS = {"H1": ("h1_h4", "h1"), "H2": ("h1_h4", "h2"), "H3": ("h1_h4", "h3"), "H4": ("h1_h4", "h4"),
           "H5": ("h5_h8", "h5"), "H6": ("h5_h8", "h6"), "H7": ("h5_h8", "h7"), "H8": ("h5_h8", "h8"),
           "ABC": ("h5_h8", "abc"), "H9": ("h9_h10", "h9"),
           "A1": ("f2_a1_a3", "a1"), "A2": ("f2_a1_a3", "a2"), "A3": ("f2_a1_a3", "a3"),
           "A4": ("f2_a4_a5", "a4"), "A5": ("f2_a4_a5", "a5"), "A6": ("f2_a6_a10", "a6"), "A7": ("f2_a6_a10", "a7"), "A8": ("f2_a6_a10", "a8"), "A9": ("f2_a6_a10", "a9"), "A10": ("f2_a6_a10", "a10"), "A11": ("f2_a11_a15", "a11"), "A12": ("f2_a11_a15", "a12"), "A13": ("f2_a11_a15", "a13"), "A14": ("f2_a11_a15", "a14"), "A15": ("f2_a11_a15", "a15"),
           "C1": ("f2_posregistro", "c1"), "C2": ("f2_posregistro", "c2"), "C3": ("f2_posregistro", "c3"), "C12": ("f2_posregistro", "c12"),
           "A18": ("f2_a18", "a18"), "H10": ("h9_h10", "h10"), "BU": ("h9_h10", "bu_impresso")}


def salva(out, saida, prefixo):
    for k, v in out.items():
        if isinstance(v, pd.DataFrame):
            v.to_csv(os.path.join(saida, f"{prefixo}_{k}.csv"), index=isinstance(v.index, pd.Index) and v.index.name is not None or not isinstance(v.index, pd.RangeIndex))
        elif isinstance(v, (int, float, str, dict, list)) and k != "nao_executados":
            json.dump(v, open(os.path.join(saida, f"{prefixo}_{k}.json"), "w"), ensure_ascii=False, indent=1, default=str)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("parquet"); ap.add_argument("saida")
    ap.add_argument("--anos", type=int, nargs="+", default=[2014, 2018, 2022, 2026])
    ap.add_argument("--h", nargs="+", default=list(MODULOS))
    ap.add_argument("--zips", default=None, help="dir com votacao_secao/detalhe (H9)")
    ap.add_argument("--parquet2", default=None, help="dir com cargos_*, carga_*, perfil_agg_* (Fase 2)")
    ap.add_argument("--cesp", default=None, help="dir com os zips CESP (A6)")
    ap.add_argument("--urna", default=None, help="dir com os parquets de arquivos de urna (A4/A5)")
    a = ap.parse_args()
    os.makedirs(a.saida, exist_ok=True)
    D = carrega(a.parquet, tuple(a.anos))
    reg = Registro(); reg_pos = Registro(); reg_a18 = Registro(); falhas = []
    for h in a.h:
        mod, fn = MODULOS[h]
        out = {"zips": a.zips, "anos": a.anos, "_saida": a.saida, "_parquet": a.parquet, "_parquet2": a.parquet2 or a.parquet, "_cesp": a.cesp, "_urna": a.urna, "_reg_pos": reg_pos, "_reg_a18": reg_a18}
        t0 = time.time()
        try:
            getattr(importlib.import_module(mod), fn)(D, reg, out)
            print(f"[{h}] ok em {time.time()-t0:.0f}s", flush=True)
        except Exception as e:                                   # noqa: BLE001  (registrado, nao silencioso)
            msg = f"{type(e).__name__}: {e}"
            print(f"[{h}] NAO EXECUTADO: {msg}", file=sys.stderr, flush=True)
            if not isinstance(e, NaoExecutado):
                traceback.print_exc()
            falhas.append((h, msg))
        for r in out.get("nao_executados", []):
            falhas.append((f"{h}/{r[0]}", r[1]))
        out.pop("zips", None)
        salva({k: v for k, v in out.items() if not k.startswith("_")}, a.saida, h)
    df = reg.frame()
    if len(df):
        df.to_csv(os.path.join(a.saida, "registro_testes.csv"), index=False)
    dfp = reg_pos.frame()
    if len(dfp):
        dfp.to_csv(os.path.join(a.saida, "posregistro_testes.csv"), index=False)
    dfa = reg_a18.frame()
    if len(dfa):
        dfa.to_csv(os.path.join(a.saida, "a18_testes.csv"), index=False)
    pd.DataFrame(falhas, columns=["teste", "motivo"]).to_csv(os.path.join(a.saida, "nao_executados.csv"), index=False)
    print(f"\n{len(df)} testes no registro; {len(falhas)} nao executados")
    sys.exit(2 if falhas else 0)


if __name__ == "__main__":
    main()
