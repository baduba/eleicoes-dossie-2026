# Registro de IDs de teste (A1–A44) — coordenação entre sessões

Mapa único dos IDs do projeto, para coordenar duas sessões paralelas (**S1**: frente de análise/portal —
inversão, índice, fechamento, verificações e curva; **S2**: frente da série temporal de logs; **base**:
Fases 1–4). Fontes: `00_preregistro.md` (Adendos 1–20), `docs/resultados-fase2.md`, `docs/fase3.md`,
`docs/propostas/gatilhos-e-inversao.md`, `docs/alegacoes.md` (Inventário, A16), `CHANGELOG.md`.

Estados: **RODADO** | **REGISTRADO** (pré-registro escrito, aguardando rodada) | **EXPLORATÓRIO** (com
números, sem pré-registro formal) | **REFUTADO** | **RETIRADO** | **PROPOSTO** | **RESERVADO** |
**NÃO EXECUTADO** (registrado, sem insumo).

| ID | Título curto | Adendo | Sessão | Estado |
|---|---|---|---|---|
| A1 | Curva de apuração | 4 (+6, pós-registro) | base | RODADO |
| A2 | Continuidade municipal / transições T1→T2 seção a seção | 4 (+6) | base | RODADO |
| A3 | Origem dos votos novos de Lula | 4 (+6) | base | RODADO |
| A4 | Cadeia BU/RDV/hash (da urna ao TSE) | 4 | base | RODADO |
| A5 | Votos após as 17h (estimativa, logs) | 4 | base | RODADO (amostra; logs parciais) |
| A6 | Troca de urna / contingência | 4 | base | RODADO |
| A7 | Pesquisas e resultado (contexto, sem veredito) | 4 | base | RODADO |
| A8 | Coerência entre cargos no mesmo boletim | 4 | base | RODADO |
| A9 | Perfil do comparecimento | 4 | base | RODADO |
| A10 | Modelo de urna, exterior e locais especiais | 4 | base | RODADO |
| A11 | Transferência de votos dos derrotados no T1 | 5 | base | RODADO |
| A12 | Seções com zero voto para um candidato | 5 (+6) | base | RODADO |
| A12b | "106 urnas 100% Lula, 0% BN e oponente" (zero BN em seção grande) | 12 | base | RODADO |
| A13 | Curva de apuração: inversões, trechos lineares, "método do vídeo" | 5 | base | RODADO |
| A14 | Recebimento × totalização × divulgação em 25/10/2026 | 5 | base | RODADO |
| A15 | Modelo de urna em 2022 (relatório PL/Cerimedo) | 5 | base | RODADO |
| A16 | Inventário de alegações | 5 | base | RODADO (vivo, recebe itens) |
| A17 | Questões em aberto | 5 | base | RODADO (vivo) |
| A18 | Alteração de arquivo no meio da apuração | 7 | base | RODADO |
| A19 | Voto digitado × voto registrado (ponto cego) | 7 | base | RODADO (ponto cego permanece aberto) |
| A20 | Cadastro: eleitorado apto × população Censo 2022 | 8 | base | RODADO |
| A20b | Cadastro e comparecimento dos mais idosos | 9 | base | RODADO |
| A21 | Forense temporal dos logs (ritmo de votação) | 8 | base | RODADO (parcial, amostra) |
| A22 | Coerência entre cargos (Fase 3) | 8/9 | base | RODADO |
| A23 | Fiscais | 8 | base | NÃO EXECUTADO (sem insumo) |
| A24 | Experimento natural do teste de integridade | 8/9 | base | NÃO EXECUTADO (sem insumo) |
| A25 | Urnas substituídas antes/depois | 8 | base | RODADO (parcial) |
| A26 | Integridade da publicação | 8 | base | RODADO |
| A27 | As 427 seções novas com comparecimento ≥ 95% | 8 | base | RODADO |
| A28 | Pedidos de acesso à informação (LAI) | 8/9 | base | RODADO (pedidos em curso) |
| A29 | Primeira página (resultado verificado, cartões, contribuir) — item de portal | — | base | RODADO |
| A30 | Gráficos G1–G4 — item de portal | — | base | RODADO |
| A31 | Municípios extremos na transferência T1→T2 (Silva Jardim/RJ) | 10 | base | RODADO |
| A31b | Municípios com dOponente ≤ +1 (decomposição) | 13 | base | RODADO |
| A32 | Liberação manual como canal de abuso local (rajadas de log) | 11 | base | RODADO |
| A32b | Rajadas com limiar absoluto (prevalência) | 14 | base | RODADO |
| A33 | Liberação manual no nível da escola | 15 | base | RODADO |
| A34 | Duração do voto por eleitor | 16, 16a, 16b | base | RODADO (amostra; universo NÃO EXECUTADO) |
| A35 | Extremos no universo geral | 17 | base | RODADO |
| A36 | Canal 2 de envio de boletins (formulário externo) | — | base | **RETIRADO** (a pedido do autor, antes da publicação; ver CHANGELOG v0.9.4) |
| A37 | Inversão de voto (eleitor vota 13, registra 22) | pré-registro em `docs/propostas/gatilhos-e-inversao.md` PARTE 1 (a promover a adendo) | S1 | REGISTRADO |
| A37b | Presidente × deputado (braço de A37) | idem, PARTE 1b; script `scripts/exploratorio/05_a37b_presidente_x_deputado.py` escrito | S1 | REGISTRADO (pendente de rodar; insumo `parquet2/cargos_*` já local) |
| A38 | Índice de exposição por seção | esboço em `gatilhos-e-inversao.md` §2.4 | S1 | PROPOSTO |
| A39 | Fechamento de fluxo T1→T2, 2002–2026 | proposta de pré-registro em `gatilhos-e-inversao.md` PARTE 6 | S1 | EXPLORATÓRIO com números (`results/exploratorio/FLX_*`; desvio 2026 +5,8M, cross-over implícito 90–99%) |
| A40 | Curva taxa manual × voto no incumbente ("sobe linearmente acima de 61%") | — | S1 | **REFUTADO PUBLICADO** (inventário de alegações, `docs/alegacoes.md`, com figura `a40_curva_manual`; curva estrutural, mais fraca em 2026, máx. 59,8%) |
| A41 | Comparecimento acima da população 16+ (reescreve "23 municípios BA") | **19** | S1 | REGISTRADO — insumo pronto (`data/ibge_populacao_municipios_2022.csv`, sha256 292dbf32…, 31/10; ver `docs/propostas/a41-insumo-sidra.md`); **autorizado a rodar** |
| A42 | Leitura completa dos logs por UF (etapa B do A43) | **21** | S1 | REGISTRADO (Adendo 21, 31/10/2026; regra de decisão a ser fixada pelo dono antes de assinar) |
| A43 | Série temporal dos votos a cada 15 minutos (M1–M6) | **18** | S2 | **ETAPA A RODADA-parcial (31/10, S1)**: extrator pronto (`scripts/50_a43_etapaA_janelas.py`), amostra RR 2026/2022 T2 100% lida, sem anomalias (0,05% de votos após 17h nos dois anos); medição de escala feita (3,5–7,5 h CPU total, ver `docs/propostas/a43-etapaA-amostra.md`); regra de horário com fonte pendente (TRE-PE 403, `fontes/`); Etapa B = A42 (Adendo 21), aguardando assinatura do dono |
| A44 | Quedas verticais na curva acumulada de apuração (vídeo Prof. Trindade) | **20** | S1 | **RODADO (31/10) — EXPLICADO**: quedas só na janela inicial de base pequena (máx. −3,02 p.p. às 19:03; ≤0,091 p.p. após 20h), 100% dos 95 eventos fecham com o lote (dif. 0,0), mistas não adicionam eventos, placebo 2022 tem quedas maiores (−8,41 p.p.); memorando `docs/propostas/a44-quedas-curva.md` |

## Colisões resolvidas

- **A37 (resolvida em 31/10/2026).** O rascunho da Fase 5 chamou de "A37" a alegação da Bahia ("23
  municípios com mais eleitores que habitantes"), mas A37 já era a inversão de voto (pré-registro de S1).
  Correção: a alegação da BA virou **A41**, pré-registrada no Adendo 19. Nenhum resultado foi publicado com
  o ID errado.

## Ambiguidades a resolver com o dono (não mexidas)

- **A29 tem dois usos.** No CHANGELOG (v0.9.x), A29 é o item de portal "primeira página"; no Adendo 11
  (A32, item 4) e no Adendo 18 (limites), "A18/A29" aparece como a **verificação de assinatura de logs**,
  pendente. Ou o ID A29 foi usado duas vezes, ou a verificação de assinatura precisa de ID próprio.
  Sugestão: reservar **A45** para "verificação da assinatura dos logs" se o dono confirmar.
- **A16/A17 são itens vivos** (inventário e questões em aberto), não testes com veredito; mantidos como
  RODADO por convenção.

## Regra operacional (obrigatória nas duas sessões)

**Antes de escrever qualquer adendo novo: reservar o próximo ID livre AQUI, neste arquivo, com commit+push;
nunca reutilizar ID; uma sessão por vez faz push na `main`, a outra trabalha em branch.** Próximo ID livre
após este registro: **A45** (ver observação sobre A29 acima). Próximo adendo livre: **22** (o 21 é A42).
