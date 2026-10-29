"""Traducao para o ingles dos textos das figuras G0 a G4 (GRAF_LANG=en). Os graficos continuam sendo desenhados pelo mesmo codigo e pelos mesmos dados; so os textos mudam.
Chave: texto em portugues com quebras de linha e espacos repetidos colapsados. Valor: texto em ingles; se o original tinha quebras de linha e o valor nao, o valor e requebrado na mesma largura.
Numeros: separador de milhar e decimal trocados (1.000 -> 1,000; 0,1% -> 0.1%). Texto sem traducao: aviso em stderr e o proprio texto (para a figura nao sair com buraco)."""
import re
import sys
import textwrap
from matplotlib.text import Text

PARCIAL = []
TEXTOS = {}
META = {}
PADROES = []


def numeros(s):
    def f(m):
        t = m.group(0)
        if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", t):
            return t.replace(".", "\0").replace(",", ".").replace("\0", ",")
        if re.fullmatch(r"\d+,\d+", t):
            return t.replace(",", ".")
        return t
    return re.sub(r"\d[\d.,]*\d|\d", f, s)


def colapsa(s):
    return re.sub(r"\s+", " ", s).strip()


def traduz(s):
    if not s.strip():
        return s
    if "teto, não estimativa" in s:
        return numeros(s.replace("teto, não estimativa:", "ceiling, not an estimate:").replace("medido:", "measured:"))
    k = colapsa(s)
    pref = ""
    m = re.match(r"^(\d+\. )(.*)$", k)
    if m and m.group(2) in TEXTOS:
        pref, k = m.group(1), m.group(2)
    if k in TEXTOS:
        en = TEXTOS[k]
    else:
        en = None
        for rx, fn in PADROES:
            mm = rx.match(k)
            if mm:
                en = fn(*mm.groups()); break
        if en is None:
            if re.fullmatch(r"[\d\s.,%+\-−x/|:()A-Za-z]*", k) and not re.search(r"[a-z]{4,}", k):
                return numeros(s)
            PARCIAL.append(k); return s
    en = numeros(pref + en)
    if "\n" in s and "\n" not in en:
        w = max(len(l) for l in s.split("\n"))
        if s.split("\n")[0].rstrip().endswith(":") and ": " in en:
            cab, resto = en.split(": ", 1); en = cab + ":\n" + textwrap.fill(resto, max(w + 6, 12))
        else:
            en = textwrap.fill(en, max(w, 12))
    return en


def traduz_figura(fig):
    from matplotlib.ticker import FuncFormatter
    for ax in fig.axes:
        for eixo in (ax.xaxis, ax.yaxis):
            velho = eixo.get_major_formatter()
            eixo.set_major_formatter(FuncFormatter(lambda x, pos, v=velho: traduz(v(x, pos))))
    for t in fig.findobj(Text):
        s = t.get_text()
        if s:
            t.set_text(traduz(s))
    if PARCIAL:
        print("SEM TRADUCAO:", *sorted(set(PARCIAL)), sep="\n  ", file=sys.stderr)


def _p(rx, fn):
    PADROES.append((re.compile(rx), fn))


_p(r"^teto, não estimativa: (\S+)(?: \| medido: (\S+))?$", lambda a, b=None: f"ceiling, not an estimate: {a}" + (f" | measured: {b}" if b else ""))
_p(r"^(\d+) trocas/seção: (\S+) seções \((\S+)%\)$", lambda k, n, p: f"{k} switches/section: {n} sections ({p}%)")
_p(r"^(\d+) trocas/seção: mudar a margem exige (\S+)% das seções$", lambda k, p: f"{k} switches/section: changing the margin requires {p}% of sections")
_p(r"^(\d+) trocas por seção: mudar a margem exige (\S+)% das seções$", lambda k, p: f"{k} switches per section: changing the margin requires {p}% of sections")
_p(r"^5 trocas/seção: (\S+)% das seções \(fora do gráfico\)$", lambda p: f"5 switches/section: {p}% of sections (off the chart)")
_p(r"^\(a\) teste de integridade, todas as urnas \(n = (\d+)\)$", lambda n: f"(a) integrity test, all voting machines (n = {n})")
_p(r"^\(b\) só urnas com biometria \(n = (\d+) a (\d+); faixa\)$", lambda a, b: f"(b) only machines with biometrics (n = {a} to {b}; band)")
_p(r"^\(c\) boletins impressos conferidos, n = (\d+)$", lambda n: f"(c) printed poll-receipts checked, n = {n}")
_p(r"^\(c\) n real conferido em (\S+): (\d+) boletins( \(sem curva\))?$", lambda d, n, c=None: f"(c) actual n checked on {d}: {n} poll-receipts" + (" (no curve)" if c else ""))
_p(r"^Cada voto trocado muda a margem em 2\. Limiar de (\d+) trocas por seção: desvio padrão do resíduo local de (\S+) p\.p\. \(medido nesta auditoria\), (\d+) votos válidos por seção, \|z\| > 3\. Região à esquerda do limiar: uma seção alterada não se destaca das vizinhas; só aparece em conjunto \(comparação com outros cargos, A22, não executada\) ou conferindo boletins impressos e o teste de integridade\. Premissas: amostra aleatória de seções; não descreve como uma alteração seria feita\.$",
   lambda k, sd, v: f"Each switched vote changes the margin by 2. Threshold of {k} switches per section: standard deviation of the local residual of {sd} p.p. (measured in this audit), {v} valid votes per section, |z| > 3. Region to the left of the threshold: an altered section does not stand out from its neighbors; it only shows up in aggregate (comparison with other offices, A22, not run) or by checking printed poll-receipts and the integrity test. Assumptions: random sample of sections; it does not describe how an alteration would be made.")

TEXTOS.update({
    # G1
    "Cadastro de eleitores": "Voter registry", "Habilitação (biometria / liberação manual)": "Check-in (biometrics / manual release)",
    "Voto digitado → voto registrado (software)": "Typed vote → recorded vote (software)", "RDV (registro digital do voto)": "RDV (digital vote record)", "BU digital": "Digital BU\n(poll-receipt)",
    "BU impresso": "Printed BU\n(poll-receipt)", "Assinatura digital": "Digital signature", "Transmissão": "Transmission", "Recepção": "Receipt", "Totalização": "Tabulation", "Publicação (BWeb)": "Publication (BWeb)", "Divulgação ao vivo": "Live reporting",
    "A20, A20b, A9": "A20, A20b, A9", "A18, boletins": "A18, BUs",
    "comparado ao Censo; sem cruzamento nominal": "compared with the Census; no name-level cross-check", "o log registra, mas não prova quem era o eleitor": "the log records it, but does not prove who the voter was",
    "verificado só por amostragem no teste de integridade": "checked only by sampling in the integrity test", "recontado e igual ao boletim; mesmo software da urna": "recounted and equal to the poll-receipt; same voting-machine software",
    "igual ao BWeb; mesmo software da urna": "equal to BWeb; same voting-machine software", "0 boletins conferidos até agora": "0 poll-receipts checked so far", "certificado lido; assinatura 0% verificada": "certificate read; signature 0% verified",
    "canal não público": "non-public channel", "horários públicos; sem o registro interno": "public timestamps; no internal record", "igual por seção, município e zona; mesmo fluxo": "equal by section, municipality and zone; same flow",
    "hash e tamanho iguais ao primeiro download": "hash and size equal to the first download", "curva analisada; sem capturas da época": "curve analyzed; no captures from the time",
    "◐ verificado parcialmente": "◐ partially verified", "✓ verificado pelos testes": "✓ verified by the tests", "✕ não verificável com dados públicos": "✕ not verifiable with public data",
    "A cadeia continua na linha de baixo": "The chain continues on the line below", "Leia da esquerda para a direita, de cima para baixo (1 a 12).": "Read left to right, top to bottom (1 to 12).",
    "Elo destacado em vermelhão: o voto digitado e o voto registrado só são conferidos por amostragem, no teste de integridade.": "Link highlighted in red: the typed vote and the recorded vote are only checked by sampling, in the integrity test.",
    "Elo 3, em vermelhão: o voto digitado e o voto registrado só são conferidos por amostragem, no teste de integridade.": "Link 3, in red: the typed vote and the recorded vote are only checked by sampling, in the integrity test.",
    "Mapa da cadeia do voto: o que os testes verificam e o que não verificam": "Map of the vote chain: what the tests verify and what they do not",
    "Mapa da cadeia do voto: o que os testes verificam e não verificam": "Map of the vote chain: what the tests verify and do not verify",
    # G0
    "verificados": "verified", "parciais": "partial", "não verificáveis": "not verifiable", "cadeia do voto: 12 elos": "vote chain: 12 links",
    "azul: verificado · ocre: parcial · vermelho: não verificável — 33% totalmente verificada, 25% não verificável": "blue: verified · ochre: partial · red: not verifiable; 33% fully verified, 25% not verifiable",
    "100% dos votos atravessam pelo menos um elo não verificável": "100% of votes pass through at least one non-verifiable link", "todos os votos": "all votes",
    # G2
    "Quanto cada verificação enxerga: probabilidade de detectar ao menos uma urna alterada": "How much each check sees: probability of detecting at least one altered voting machine",
    "Quanto cada verificação enxerga: chance de detectar ao menos uma urna alterada": "How much each check sees: chance of detecting at least one altered voting machine",
    "Fração das urnas ou seções alteradas (escala log)": "Fraction of voting machines or sections altered (log scale)", "Chance de ver ao menos uma alterada": "Chance of seeing at least one altered",
    "Premissas: amostra aleatória; em (b), software que se comporta normalmente no teste sem biometria. Não descreve como um ataque seria feito. As linhas verticais mostram a fração de seções que precisaria ser alterada para mudar a margem de 4.430.191 votos.":
        "Assumptions: random sample; in (b), software that behaves normally in the test without biometrics. It does not describe how an attack would be carried out. The vertical lines show the fraction of sections that would have to be altered to change the margin of 4.430.191 votes.",
    # G3
    "Liberação manual, 1º turno (sem controle do 1º turno)": "Manual release, 1st round (uncontrolled)", "Cadastro: eleitores muito idosos (80+)": "Voter registry: very elderly (80+)",
    "Urna modelo UE2022": "UE2022 voting machine", "Flávio x liberação manual": "Flávio x manual release", "Seções novas": "New sections", "639 seções com comparecimento ≥ 95%": "639 sections with turnout ≥ 95%",
    "Seção de 2022 com log divergente": "2022 section with divergent log", "Presidente x governador (AM e DF)": "President x governor (AM and DF)", "Comparecimento x fração 80+ por seção": "Turnout x 80+ fraction by section",
    "Voto x fração 80+ por seção": "Vote x 80+ fraction by section", "Votantes 95+ acima da razão de 2022": "Voters 95+ above 2022 ratio", "Transferência T1 a T2: 3 municípios fora da cauda": "Round 1 to 2 transfer: 3 outlier municipalities",
    "Zero Flávio, brancos e nulos (106 seções)": "Zero Flávio, blank and null (106 sections)", "Liberação manual além do ruído do modelo de 2022": "Manual release beyond 2022 model noise",
    "Escolas com liberação manual extrema (além do ruído)": "Schools with extreme manual release",
    "Zero brancos e nulos em seção grande (todo o país)": "Zero blank and null in large section (nationwide)",
    "Escala linear (proporção real)": "Linear scale (true proportion)", "Escala logarítmica (itens pequenos visíveis)": "Logarithmic scale (small items visible)", "Margem 4.430.191": "Margin 4.430.191", "Votos de margem": "Margin votes",
    "1 mil": "1K", "10 mil": "10K", "100 mil": "100K", "1 mi": "1M", "2 mi": "2M", "3 mi": "3M", "4 mi": "4M",
    "Tamanho dos itens em aberto, em votos de margem, contra a margem de 4.430.191": "Size of the open items, in margin votes, against the margin of 4.430.191",
    "excesso medido, a favor de Lula": "measured excess, in favor of Lula", "excesso medido, a favor de Flávio": "measured excess, in favor of Flávio", "sem direção identificável": "no identifiable direction",
    "hachurado: teto de pior caso, não estimativa": "hatched: worst-case ceiling, not an estimate",
    "Não mensuráveis com os dados públicos (sem barra): curva de apuração do 1º turno; testes não executados (A21, A23 a A25, A28); voto digitado x voto registrado; alteração coerente antes da publicação. O que falta para medir cada um está na lista de perguntas em aberto. Cada barra é um item; não há soma. A escala linear começa em zero. Tetos inflados por construção ou sem poder (por exemplo, o registrado de A32 e os de A31b, A32b, A33 e A34) não são plotados; aparecem só como texto, com a razão (CHANGELOG, regra de exibição).":
        "Not measurable with public data (no bar): 1st-round counting curve; tests not run (A21, A23 to A25, A28); typed vote x recorded vote; coherent alteration before publication. What is missing to measure each one is in the list of open questions. Each bar is one item; there is no sum. The linear scale starts at zero. Ceilings inflated by construction or without power (for example, the recorded one for A32 and those of A31b, A32b, A33 and A34) are not plotted; they appear only as text, with the reason (CHANGELOG, display rule).",
    # G4
    "todas as 499.248 seções": "all 499.248 sections", "só em conjunto, boletins impressos ou teste de integridade": "only in aggregate, printed poll-receipts or integrity test",
    "só em conjunto, BUs impressos ou teste de integridade": "only in aggregate, printed poll-receipts or integrity test",
    "aparece como valor atípico no local (já alcançada pelos testes executados)": "shows up as a local outlier (already reached by the tests run)", "valor atípico no local (alcançada pelos testes)": "local outlier (reached by the tests)",
    "Quantas seções precisariam ser alteradas para inverter a margem de 4.430.191 votos": "How many sections would have to be altered to flip the margin of 4.430.191 votes",
    "Quantas seções precisariam ser alteradas para inverter a margem de 4.430.191 votos": "How many sections would have to be altered to flip the margin of 4.430.191 votes",
    "Votos trocados por seção (escala log)": "Votes switched per section (log scale)", "Seções necessárias para mudar a margem (log)": "Sections needed to change the margin (log)",
})
META.update({
    "g0_verificacao": ("Verification coverage of the vote chain", "Stacked bar of the 12 links in the vote chain: 4 verified (33%), 5 partially verified (42%) and 3 not verifiable with public data (25%). A second bar indicates that 100% of votes pass through at least one non-verifiable link."),
    "g1_cadeia": ("Map of the vote chain", "Twelve steps of the vote, from registration to publication, each with its verification status (verified, partial or not verifiable with public data) and the corresponding test; the link between typed vote and recorded vote is highlighted as not verifiable with public data."),
    "g2_deteccao": ("Detection curves", "Probability of detecting at least one altered voting machine or section as a function of the altered fraction, for the integrity test, for machines with biometrics and for printed poll-receipts checked, with marks of the fraction needed to change the margin."),
    "g3_impacto": ("Size of the open items", "Horizontal bars, in margin votes, for each open item with a number: measured excess (solid) and worst-case ceiling (hatched), against the margin of 4.430.191 votes, on linear and logarithmic scales."),
    "g4_secoes": ("Sections needed to flip the margin", "Number of sections that would have to be altered to change the margin as a function of votes switched per section, with the region the tests run already reach and the region only printed poll-receipts and the integrity test reach."),
})
_p(r"^teto, não estimativa: (\S+) medido: (\S+)$", lambda a, b: f"ceiling, not an estimate: {a} | measured: {b}")
_p(r"^(\d+) (verificados|parciais|não verificáveis) (\d+)%$", lambda k, r, p: f"{k} {TEXTOS[r]}\n{p}%")
