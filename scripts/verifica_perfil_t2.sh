#!/usr/bin/env bash
# Verifica se o TSE publicou o perfil de comparecimento e abstenção do 2º turno de 2026.
# Sinal: a data de modificação do arquivo no CDN mudou em relação à última conferida (21/10/2026 16:40:26 GMT, só 1º turno).
# Saída: 0 = sem mudança; 10 = mudou (conferir se há NR_TURNO = 2 e rodar scripts/31_a20b_idosos.py).
set -u
URL="https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_comparecimento_abstencao/perfil_comparecimento_abstencao_2026.zip"
BASE="Wed, 21 Oct 2026 16:40:26 GMT"
LM=$(curl -sI -m 60 "$URL" | tr -d '\r' | awk -F': ' 'tolower($1)=="last-modified"{print $2}')
echo "Last-Modified atual: ${LM:-indisponivel} (base: $BASE)"
if [ -z "$LM" ]; then echo "AVISO: sem resposta do CDN"; exit 0; fi
if [ "$LM" != "$BASE" ]; then echo "MUDOU: conferir se o arquivo traz o 2o turno (NR_TURNO=2) e rodar scripts/31_a20b_idosos.py"; exit 10; fi
echo "sem mudanca"
