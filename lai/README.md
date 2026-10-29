# Pedidos de acesso à informação (A28)

Textos prontos para protocolo ao TSE e aos TREs, um por assunto. Cada pedido pede arquivo aberto, sem dados pessoais, e cita a Lei 12.527/2011 (prazo de 20 dias, prorrogável por 10).

| arquivo | assunto | para quê (teste que depende da resposta) |
|---|---|---|
| `01_urnas_substituidas.md` | urnas substituídas, horário e motivo | A25, A6 |
| `02_codigo_de_carga.md` | código de carga por urna | A6, A25 |
| `03_teste_de_integridade.md` | seções, sorteio, observadores, relatórios e vídeos por UF | A19, A24 |
| `04_logs_de_totalizacao.md` | incidente de 04/10, retenção até 19h em 25/10, horários por seção | A18, A1 |
| `05_fiscais_credenciados.md` | fiscais por seção, agregado | A23 |
| `06_assinatura_e_chaves.md` | certificados, especificação e ferramenta de verificação | A4, A18 |
| `07_ata_e_folha_de_votacao.md` | ata da mesa receptora e folha de votação (nomes tarjados) de 83 seções (50 do A32 e 33 das 20 escolas extremas do A33; lista em `07_secoes.csv`) | A32, A33 |
| `08_modelo_requerimento_partidos.md` | **modelo** de requerimento de partido ou coligação ao cartório eleitoral, para o mesmo fim (revisão por advogado eleitoral; não é pedido LAI) | A32 |

## Quem recebe cada pedido e por qual canal (A28, Fase 3.1)
Veja `canais.csv` (órgão, canal, base normativa, estado da verificação, por que este órgão) e `canais_tres.csv` (domínio e página do SIC dos 27 TREs). Resumo: 01, 02, 04 e 06 vão ao **TSE**; 03 vai ao **TSE e a cada TRE** (um protocolo por órgão, mesmo texto); 05 vai a **cada TRE** (e ao TSE só se houver consolidado). O canal do TSE é o Formulário Eletrônico da Ouvidoria (SIC); o dos TREs é o e-SIC de cada site. **Estado da verificação:** o TSE e os TREs bloqueiam acesso automatizado (403), então os canais foram conferidos em resultados de busca, não abrindo o formulário; confirme o canal, os campos e o prazo no momento do protocolo. A identificação de quem pede é exigida (Resolução CNJ 215/2015, art. 11, § 2º, citada pelo TRE-SP); o projeto não tem autor nominal, então quem protocola assina.

## Como usar
1. Quem for protocolar preenche a identificação e envia pelo canal de acesso à informação do TSE ou do TRE competente.
2. Registra em `registro.csv` a data, o protocolo e o prazo. **Negativa também é registrada**, com o fundamento legal informado, e o recurso, quando houver.
3. Envia a resposta por *issue* (ou PR) neste repositório; o resultado entra na página do teste correspondente e no [CHANGELOG](../CHANGELOG.md).

Estado atual: **nenhum pedido protocolado** (NÃO EXECUTADO). Os textos não contêm nome de pessoa nem acusação.
