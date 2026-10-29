# Auditoria independente reproduzível: 2º turno presidencial de 2026

Repositório com scripts, previsões pré-registradas, resultados e documentação de uma auditoria estatística dos dados oficiais do TSE sobre o 2º turno de 25/10/2026 (Lula x Flávio Bolsonaro). **Não é laudo, perícia oficial nem documento homologado.**

Portal: https://baduba.github.io/eleicoes-dossie-2026/ (após a publicação) · PDF: `relatorio/` e release v0.9.1 (versão preliminar).

**Versão preliminar (v0.9.1).** A v1.0 sai depois do relatório consolidado do TCU (até 24/11/2026), da verificação da assinatura e de um lote inicial de boletins impressos.

## Objetivo
Permitir que qualquer perito, de qualquer lado, reproduza cada número e conteste o que discordar. Só entra o que sai de script versionado sobre dado oficial com hash conferido, ou afirmação com fonte citada. Todo código e dado estão no repositório para verificação independente. (Os arquivos de origem do TSE entram por URL e hash SHA-512 conferido, em `data/`, e não como cópia; scripts, previsões, resultados e tabelas completos estão no repositório.)

## O que foi e o que não foi testado
- **Testado:** consistência BWeb x `votacao_secao` x totalização; BU digital x BWeb; RDV x BU; vínculo de hash dos arquivos de urna; log x BU e votos depois das 17h (amostra); estatística de seção com placebos (2014, 2018, 2022, 1º turno de 2026); curva de apuração; transições entre turnos; zero voto; modelo de urna; coerência entre cargos; alegações do relatório original.
- **Não testado / NÃO EXECUTADO:** cruzamento com boletins impressos (sem insumo); assinatura criptográfica da urna (sem a especificação); curva de divulgação (sem snapshots); perfil de comparecimento de 2026/2º turno; curva de 2014; as "472 urnas". Lista completa e motivos em [`results/fase2/nao_executados.csv`](results/fase2/nao_executados.csv).

## Resumo dos vereditos
Nenhum achado, isolado ou somado, alcança a margem de 4.430.191 votos. Itens sem causa identificada estão em [Questões em aberto](docs/residuos.md). Detalhes em [`dossie.md`](dossie.md) (Fase 1) e [`docs/resultados-fase2.md`](docs/resultados-fase2.md).

## Estrutura
`00_preregistro.md` (previsões e adendos), `dossie.md` (Fase 1), `docs/` (portal), `scripts/`, `results/fase1` e `results/fase2` (tabelas e figuras), `data/` (URLs e hashes), `tests/`, `CHANGELOG.md`, `LICENSE`.

## Como reproduzir
Ver [Dados e reprodução](docs/dados-reproducao.md): requisitos, comandos na ordem, tempo e espaço.

## Como contestar
Abra uma *issue* com o número ou a tabela contestada, o script que reproduz a sua versão e o dado de origem.

## Licença
Código: MIT. Texto, tabelas e figuras: CC BY 4.0. Os dados de origem são do TSE e não são redistribuídos aqui.

## Autoria
Projeto sem autoria nominal, mantido pela conta baduba no GitHub. Contato, correções e contestações por *issue* em https://github.com/baduba/eleicoes-dossie-2026/issues.
