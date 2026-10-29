# Boletins de urna impressos: como enviar fotos

**Por que.** O boletim de urna impresso é a única cópia dos resultados de uma seção que **não passa** pelos arquivos que o TSE publica. Todo o resto (RDV, BU digital, BWeb, totalização) nasce do mesmo software da urna: se esse software registrasse diferente do digitado, todos esses arquivos concordariam entre si — e com o erro. A foto do boletim afixado na seção é a **única verificação independente** desse elo cego. Comparar o que está impresso com o BWeb exclui, para as seções conferidas, uma alteração coerente feita depois do fechamento da urna. Nenhuma foto foi recebida até agora; o teste direto permanece **NÃO EXECUTADO** ([A18](a18-alteracao-no-meio.md)).

**Quem pode enviar.** Mesários, eleitores, imprensa e fiscais de qualquer partido ou coligação. Pela lei, o presidente da mesa receptora é obrigado a entregar cópia do boletim aos partidos e coligações que a requeiram até uma hora após a expedição (Lei 9.504/1997, art. 68, § 1º, [texto no Planalto](https://www.planalto.gov.br/ccivil_03/leis/l9504compilado.htm)); o boletim também fica afixado na seção e pode ser fotografado por qualquer pessoa. Não é preciso identificar-se publicamente.

## O que fotografar

1. O **boletim inteiro, de frente e legível**, sem cortar o **cabeçalho** (onde estão UF, município, zona e seção) nem as linhas de votos do fim. Se não couber tudo, vale uma foto do cabeçalho e outra das linhas de votos.
2. Ou, em vez da foto inteira, o **QR Code** do boletim, nítido e sem reflexo.
3. Anote **UF, município, zona, seção e turno** (estão no boletim) e a **origem** da foto: mesário, eleitor, imprensa ou fiscal (e de qual partido, se quiser dizer). A origem é registrada junto com a foto.
4. Nenhum dado pessoal de eleitor. O boletim não os contém; não envie fotos de outros documentos.

## Como enviar: dois canais

Os dois canais levam à mesma conferência (BWeb, divergência publicada uma a uma). **Canal 1** exige conta no GitHub; o **canal 2** não.

[**Enviar sem conta no GitHub**](https://form.jotform.com/263017066351047)  ·  [**Enviar pelo GitHub**](https://github.com/baduba/eleicoes-dossie-2026/issues/new?template=envio-bu.yml)

### Canal 2: sem conta no GitHub (formulário)

1. Abra o [formulário](https://form.jotform.com/263017066351047).
2. Preencha UF, município, zona, seção, turno e origem (mesário, eleitor, imprensa ou fiscal), anexe a foto do boletim inteiro ou o QR Code nítido e, se puder, transcreva os números.
3. Envie. Não é preciso conta no GitHub.

**O que acontece com a foto no canal 2.** As respostas são exportadas e importadas periodicamente (não é em tempo real) por `scripts/importa_formulario.py`, que remove o **EXIF e todo metadado** (local, data, aparelho): a imagem publicada é recomposta só com os pixels e **o arquivo original nunca é publicado**. O texto livre do campo Observações, o endereço IP e qualquer dado que o serviço do formulário guarde não são publicados. A foto passa pelo mesmo pipeline do canal 1 (leitura do QR Code quando legível, conferência com o BWeb, tabela de resultados), com a origem registrada como "formulario" e o ID da submissão. Envios de teste (campo Observações com a palavra TESTE) são excluídos dos resultados.

### Canal 1: com conta no GitHub (passo a passo)

1. Abra o formulário: [https://github.com/baduba/eleicoes-dossie-2026/issues/new?template=envio-bu.yml](https://github.com/baduba/eleicoes-dossie-2026/issues/new?template=envio-bu.yml).
2. O título já vem com o prefixo "BU: "; complete com UF, zona, seção e turno (ex.: "BU: SP-123-456-2").
3. Preencha UF, município, zona, seção, turno e origem nos campos do formulário.
4. **Arraste a foto para a caixa de texto do corpo da issue** — o formulário não tem campo de anexo; a foto entra como anexo do comentário. Confira na pré-visualização que ela abre legível.
5. Se preferir, transcreva os números no formato abaixo (uma linha por boletim), no campo próprio do formulário.
6. Envie. Não é preciso conta verificada nem identificação além da conta do GitHub.

```
ano;turno;uf;cd_municipio;zona;secao;aptos;comparecimento;lula;oponente;brancos;nulos
```

## O que acontece com cada lote

1. Cada lote recebido é conferido automaticamente com o BWeb por `scripts/04_cruza_bu_impresso.py`, que reporta **qualquer** divergência, de um voto que seja.
2. **Cada divergência é publicada individualmente**, com a foto, a seção e a origem, e com o que o BWeb mostra.
3. O **total conferido sem divergência** é publicado a cada lote, junto com o poder estatístico abaixo.
4. Fotos ilegíveis ou sem os dados de identificação da seção são listadas como descartadas, com o motivo.

## Situação

| lotes recebidos | BUs conferidos | divergências | origem das fotos |
|---|---|---|---|
| 0 | 0 | 0 | n/a |

## Meta de coleta: o que cada total de boletins enxerga

Chance de flagrar **ao menos uma** seção alterada, em função do total de boletins conferidos e da fração de seções alteradas no país (amostra aleatória; cálculo hipergeométrico de [G2](index.md#g2)):

| fração de seções alteradas | 100 boletins | 300 boletins | 1.000 boletins |
|---|---|---|---|
| 0,1% (500 seções) | 10% | 26% | 63% |
| 1% (4.993 seções) | 64% | 95% | 100% |
| 2% (9.985 seções) | 86% | 100% | 100% |
| 5% (24.963 seções) | 99% | 100% | 100% |

Para amostras aleatórias de seções (as fotos voluntárias não são aleatórias; ver ressalva em [A18](a18-alteracao-no-meio.md)), quantos boletins seriam necessários para detectar, com 95% e 99% de probabilidade, ao menos uma seção alterada:

| fracao_alterada | secoes_alteradas | n_para_95 | n_para_99 |
|---|---|---|---|
| 0.1% | 500 | 2.981 | 4.575 |
| 1% | 4.993 | 298 | 458 |
| 2% | 9.985 | 149 | 228 |
| 5% | 24.963 | 59 | 90 |
| 9% | 44.933 | 32 | 49 |