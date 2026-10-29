#!/bin/sh
# Baixa os zips BWeb listados em urls_origem.txt (excluindo as linhas de hash) e confere o hash oficial publicado pelo TSE.
# Uso: sh baixar_e_verificar.sh DIR_DESTINO
set -e
D=${1:-bweb}; mkdir -p "$D"; cd "$D"
grep -E 'buweb/.*\.zip$|BWEB_.*\.zip$' ../urls_origem.txt | xargs -P 4 -n 1 sh -c 'curl -sS -f -C - -O "$0" && curl -sS -f -C - -O "$0.sha512" 2>/dev/null || curl -sS -f -C - -O "$0.sha1" 2>/dev/null || true'
# RR/2o turno/2026: catalogo do TSE aponta para .sha512; o zip real:
curl -sS -f -C - -O https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/buweb/bweb_2t_RR_261020260742.zip
ok=0; bad=0
for z in *.zip; do
  if [ -f "$z.sha512" ]; then a=sha512sum; h="$z.sha512"; elif [ -f "$z.sha1" ]; then a=sha1sum; h="$z.sha1"; else echo "SEM HASH $z"; continue; fi
  e=$(awk '{print tolower($1)}' "$h" | head -1); g=$($a "$z" | awk '{print $1}')
  if [ "$e" = "$g" ]; then ok=$((ok+1)); else bad=$((bad+1)); echo "HASH DIVERGENTE: $z"; fi
done
echo "hash ok=$ok divergente=$bad"
