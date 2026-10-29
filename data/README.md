# Dados

Os dados brutos (~8,5 GB, mais ~25 GB de arquivos de urna se baixados por inteiro) **não** estão neste repositório. Aqui estão:

- `urls_origem.txt`: URL oficial de cada arquivo usado.
- `sha256_entradas.txt`: SHA-256 dos arquivos como foram baixados nesta auditoria.
- `manifest_hash_oficial.csv`: hash oficial publicado pelo TSE (SHA-512 para 2018 a 2026, SHA-1 para 2014) e se conferiu.
- `baixar_e_verificar.sh`: baixa os arquivos e confere os hashes oficiais.

Quirk conhecido do catálogo do TSE: os dois recursos de RR/2º turno/2026 apontam para o `.sha512`; o zip real existe em `.../buweb/bweb_2t_RR_261020260742.zip`.
