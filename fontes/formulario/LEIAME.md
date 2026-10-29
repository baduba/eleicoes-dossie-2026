# Exportações do formulário (canal 2 da coleta de boletins)

Coloque aqui, **sem commitar**, a exportação do Jotform (CSV mais a pasta de anexos). O que está nesta pasta é ignorado pelo Git (`.gitignore`), porque a exportação pode trazer endereço IP, e-mail e metadados das fotos.

```
python scripts/importa_formulario.py fontes/formulario/exportacao.csv parquet results/formulario --anexos fontes/formulario
```

O script mapeia as colunas pelo texto da pergunta, exclui as submissões marcadas "TESTE" em Observações, remove EXIF e todo metadado das fotos (a imagem publicada é recomposta só com os pixels), confere a transcrição com o BWeb e grava os resultados com origem "formulario" e o ID da submissão em `results/formulario/`. O arquivo original nunca é copiado nem publicado.
