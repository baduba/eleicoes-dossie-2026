# Modelo de requerimento de partido ou coligação (fiscalização)

**Aviso.** Este é um **modelo para ser revisado por advogado(a) eleitoral do partido, da coligação ou do candidato**. O projeto não dá aconselhamento jurídico e **não protocola** nada. A base normativa e os prazos de guarda dos documentos de seção devem ser confirmados pelo(a) advogado(a) antes do envio; o projeto não verificou o prazo de guarda da ata e da folha de votação em cada zona eleitoral (**a confirmar**).

**Destinatário:** Juízo da Zona Eleitoral (cartório eleitoral) da seção, com cópia ao TRE da UF.
**Requerente:** [partido, coligação ou candidato; nome do(a) representante e do(a) advogado(a); número de inscrição na OAB]
**Referência:** Eleições de 2026, 1º turno (04/10/2026) e 2º turno (25/10/2026). Zona [__], seção(ões) [__] do município de [__]/[UF].

**Requerimento**

O(A) requerente, na qualidade de fiscal do processo de votação e apuração das eleições (Lei 9.504/1997, art. 66), requer, para a(s) seção(ões) acima:

1. cópia da **ata da mesa receptora de votos**, com as ocorrências;
2. acesso, para conferência na presença do cartório, à **folha de votação** (ou caderno de votação), ou cópia com **dados pessoais dos eleitores tarjados**, constando a ordem das linhas, a presença ou ausência de assinatura e as anotações de habilitação manual ou de liberação pelo mesário;
3. o **boletim de urna** impresso (via do cartório ou do partido), se houver.

Finalidade: conferir, seção por seção, o número de assinaturas da folha, o número de votantes da ata, o comparecimento do boletim de urna e o número de habilitações registradas pelo log da urna. Nenhuma pessoa será identificada; apenas contagens serão publicadas.

[Local e data]  [Assinatura do(a) advogado(a)]

**Como registrar o resultado.** Preencha uma linha por seção e turno no arquivo de entrada de `scripts/37_confere_ata.py` (colunas: `ano;turno;uf;cd_municipio;zona;secao;votantes_ata;assinaturas_folha`, opcionais `manuais_anotados_folha` e `comparecimento_bu_impresso`) e envie o CSV por *issue* ou PR. O script compara com o BWeb e com as habilitações do log e lista **qualquer** divergência, inclusive as que não indicam nada (erro de contagem, folha ilegível).
