#!/bin/bash
# Script definitivo para baixar bancos Propulsor do Google Drive
# Necessário: instalar gdown (pip install gdown) para lidar com Google Drive links rapidamente
# Uso: bash baixar_bancos_propulsor.sh

# Mapeamento: [nome_destino]=ID_GOOGLE_DRIVE

# IDs extraídos dos seus links:
declare -A BANCOS
BANCOS=(
  [procuracoes.db]="17XkjkSdIzzgGjcVugtRi0gaZ4eOmsTt9"
  [pessoas.db]="1oayVhD3knbgDLbVH00xty025dqZlltnv"
  [instituicoes.db]="1bs5lM3wx2m46RTND0WkpPwxjJzDp2ynY"
  [depositos.db]="1P-2MqzjwkFWjQQmjx6qbRptivAxberJF"
  [contratos.db]="1t2s7XXH_k7GEh8Zkra3badjAv1t95eTl"
  [contencioso.db]="1TCZ5ka33dC8qnnGlc_wTgC5p020ddDRj"
  [consorcios.db]="1ZhXoZL45trxBOLSLoxOAe2hfPN27KhKy"
  [usuarios.db]="1d5q9XLP0m13u2chmPWSScGX_5ndRZKmN"
  [requisicoes.db]="1yDJfk-YvXxJSTWYd7rl0zjCwWCSNkg3U"
)

mkdir -p ./database

for arquivo in "${!BANCOS[@]}"; do
  id="${BANCOS[$arquivo]}"
  dest="./database/$arquivo"
  if [ ! -f "$dest" ]; then
    echo "Baixando $arquivo ..."
    gdown --id "$id" -O "$dest"
    echo "Arquivo salvo em: $dest"
  else
    echo "Banco já existe em $dest"
  fi
  ls -lh "$dest"
done

echo "Todos os bancos baixados com sucesso."
