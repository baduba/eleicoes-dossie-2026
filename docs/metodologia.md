# Metodologia

## Princípios
1. Só entra número que sai de script versionado sobre dado oficial com hash conferido, ou afirmação com fonte citada.
2. Hipótese antes do dado: previsões "se houver manipulação espero X / se não houver espero Y" estão em [Pré-registro](preregistro.md), escritas antes de rodar cada bloco de análises (Fase 1; Adendos 1 a 3) e antes das análises da Fase 2 (Adendo 4).
3. Todo teste tem placebo (2014, 2018, 2022, 1º turno de 2026) e é simétrico (PT e oponente).
4. Resultado nulo recebe o mesmo destaque que resultado positivo. Teste que não pôde rodar fica listado como NÃO EXECUTADO, com o motivo e o insumo que faltou.
5. Mudanças feitas depois de ver resultados são publicadas como tais (adendos e [Changelog](changelog.md)).

## Dados
- **BWeb** (boletim de urna por seção) de 2014, 2018, 2022 e 2026, 1º e 2º turnos, 224 zips por UF. Hash SHA-512 (2018 a 2026) ou SHA-1 (2014) conferido contra o publicado pelo TSE.
- `votacao_secao`, `detalhe_votacao_secao`, `votacao_candidato_munzona`, perfil de comparecimento e abstenção, correspondências esperadas, pesquisas registradas.
- **Arquivos de urna** (BU, RDV, imagem, assinatura e log) do conjunto "arquivos transmitidos para totalização": amostra por seção (ver A4 e A5).
- Lista completa com URL e hash em `data/`.

## Unidades (leia antes dos números)
- **Votos de margem** é a unidade de todo teto, estimativa central e agregado em votos desta auditoria. É a variação da diferença Lula menos Flávio: trocar um voto de um candidato para o outro muda a margem em 2; um voto a mais para um candidato, sem tirar do outro, muda em 1. A fórmula do teto já inclui o fator 2 (parâmetro `fator`) e a margem oficial, 4.430.191, está na mesma unidade. Para inverter o resultado, a margem teria de cair em pelo menos 4.430.191, o que equivale a 2.215.096 votos trocados.
- **Votos (contagem)** é o número simples de votos (por exemplo, os 23 mil votos depois das 17h do A5 ou as 8,6 milhões de liberações manuais). Toda tabela e todo número de destaque traz o rótulo da unidade. Contagem e votos de margem **não** se somam nem se comparam sem conversão.
- O agregado do H10 (38.394 pró-Lula e 122.543 pró-Flávio) e as somas de Questões em aberto estão na **mesma unidade** (votos de margem), porque ambos vêm das colunas `votos_max_pior_caso` e `votos_central` do registro de testes.

## Estatística
- **Efeito fixo de local de votação** (escola): a comparação é entre seções do mesmo local, o que absorve geografia, população e perfil do local.
- **Controle do 1º turno:** quando o desfecho é o 2º turno, o voto da própria seção no 1º turno entra como controle.
- **Teste de interseção-união contra os placebos:** um efeito só conta como excesso se superar **cada** placebo. O p de "excesso" é unilateral. Correção Holm e Benjamini-Hochberg sobre todos os testes do registro.
- **Teto em votos:** `fator x max(0, diferença + 1,645 x erro padrão) x exposição`, o máximo de votos de margem que o fenômeno poderia explicar se fosse causal. Dois tetos: contra o placebo mais exigente e contra o mais frouxo (pior caso).
- **Regra de veredito:** *excesso detectado e relevante* (Holm < 0,05 e pior caso >= 1% da margem de 4.430.191); *excesso detectável, magnitude irrelevante* (Holm < 0,05 e < 1%); *refutada* (Holm >= 0,05 e < 1%); *inconclusiva* (Holm >= 0,05 e >= 1%). Testes de forma, sem conversão em votos, são rotulados à parte.
- **Ressalva de desenho:** quando um controle posterior mostra que o desenho pré-registrado era inadequado, a linha é mantida como saiu e marcada; o impacto agregado (H10) é publicado com e sem essas linhas.

## O que esta auditoria não é
Não é laudo, perícia oficial nem documento homologado: nenhum órgão homologou. É uma auditoria independente reproduzível, feita para que qualquer perito, de qualquer lado, repita e conteste.

## Como contestar
Abra uma *issue* no repositório com o número ou a tabela contestada, o script que reproduz a sua versão e o dado de origem. Correções aceitas entram no [Changelog](changelog.md).
