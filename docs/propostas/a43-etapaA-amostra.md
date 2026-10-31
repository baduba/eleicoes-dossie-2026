# A43 — Etapa A: extrator de janelas de 15 minutos + amostra RR (31/10/2026)

Pré-registro: **Adendo 18** (A43) e **Adendo 21** (A42, leitura completa). Extrator:
`scripts/50_a43_etapaA_janelas.py`, reutilizando o parser do projeto (`scripts/urna_parse.py`,
`scripts/08_arquivos_urna.py` — os mesmos de A21/A32/A34; nada reescrito). Dependência nova no venv:
`py7zr` (exigida pelo parser para logs de 2022, que são 7z; caminho de código já existente).

## Regra de horário — fonte pendente (rótulo obrigatório: "regra de horário não confirmada em fonte")

Regra usada: votação das **08:00 às 17:00, horário de Brasília**, em todo o país (fonte indicada pelo autor:
notícia do TRE-PE de setembro/2026). O acesso automatizado à notícia foi **negado (HTTP 403, Akamai,
31/10/2026)**; a recusa está salva em `fontes/tre-pe/` e o LEIAME de `fontes/` registra a pendência: o texto
oficial precisa ser salvo pelo autor para fechar a confirmação exigida pelo Adendo 18. **Decisão de fuso
(registrada):** o log traz o relógio **local** da urna (descoberta do Adendo 18); RR = Brasília −1, então
somou-se 1h em todos os carimbos (mesma regra do adendo: +1h em AM, MS, MT, RO, RR; +2h no AC).

## Amostra: Roraima inteira, 2º turno, 2026 e 2022

Cobertura: **100% das seções com log lido** (2026: 1.519/1.519; 2022: 1.268/1.268; zero erros).

| métrica (horário de Brasília) | 2022 T2 | 2026 T2 |
|---|---|---|
| votos confirmados no log | 286.160 | 308.239 |
| primeiro voto — mediana | 08:03 | 08:02 |
| primeiro voto — P99 / máx | 08:24 / 12:49 | 08:21 / 14:50 |
| último voto — mediana | 16:53 | 16:52 |
| último voto — P99 / máx | 17:03 / 17:12 | 17:02 / 17:08 |
| **votos após 17h (exato)** | **169 (0,06%)**, 145 seções | **144 (0,05%)**, 134 seções |
| seções com primeiro voto antes das 08:00 | **0** | **0** |
| votos fora do dia legal (antes 08:00) | 0 | 0 |

Distribuição por janela de 15 minutos: quase plana ao longo do dia nos dois anos (topo entre 12,3 mil e
13,2 mil votos/janela em 2026; 10,5 a 11,9 mil em 2022), sem vazio seguido de rajada chamativo na agregação
da UF (o detalhe por seção — M1 a M6 do Adendo 18 — fica para a corrida em cima destes CSVs).

**Leitura:** nada de anômalo na amostra; 2026 é indistinguível de 2022 nos carimbos. Os votos após 17h são
raras sessões com fila (0,05%), coerentes com o encerramento mediano do BWeb (17:01–17:05, Adendo 18).
A estimativa nacional por amostra segue sendo a do A5; o **exato nacional** é saída registrada do A42.

## Medição de escala (exigida antes da Etapa B / A42)

| UF | ano | zip (MB) | logs extraídos (MB) | seções | tempo | s/seção | MB log/seção |
|---|---|---|---|---|---|---|---|
| RR | 2026 | 325,1 | 222,2 | 1.519 | 9,4 s | 0,006 | 0,146 |
| RR | 2022 | 214,8 | 133,1 | 1.268 | 16,2 s | 0,013 | 0,105 |

**Projeção (27 UFs + ZZ × 2 anos × 2 turnos, ~500 mil seções por turno):**
- **CPU:** 0,006–0,013 s/seção × 2,0 M seções ≈ **3,5–7,5 h single-thread** no total; com 8–12 threads
  (o extrator é paralelizável por seção) ≈ **30–60 min de CPU**, mais o download.
- **Rede:** zips ≈ 387 GB no total (estimativa do Adendo 18); a 50–100 MB/s ≈ **1–2,5 h** de transferência.
- **Disco:** transitório de 1 zip por UF (pico = maior UF, dezenas de GB; o zip é apagado após a extração,
  conforme o Adendo 21); logs não são persistidos; saídas CSV ≈ 1–5 MB por UF (janelas por seção).
- **Custo de VM (ordem de grandeza):** 8 vCPU/32 GB spot por ~1 dia ≈ **US$ 5–15** por ciclo completo
  (2 anos × 2 turnos), mais egress se houver.

## Saídas

`results/fase5/A43A_RR_2026_t2_janelas.csv`, `A43A_RR_2022_t2_janelas.csv`, `A43A_RR_*_cobertura.csv`,
`A43A_medicao_escala.csv`. **Rótulo em todas:** "Etapa A — amostra (Roraima); regra de horário não
confirmada em fonte".
