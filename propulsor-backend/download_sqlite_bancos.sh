#!/bin/bash
set -e

# Função para baixar arquivos do Google Drive por ID
baixar_gdrive() {
  FILE_ID=$1
  DESTINO=$2
  if [ ! -f "$DESTINO" ]; then
    echo "Baixando $DESTINO..."
    curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${FILE_ID}" > /tmp/intermedio
    CONFIRM=$(awk '/download/ {print $NF}' /tmp/intermedio | head -n1)
    curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=${CONFIRM}&id=${FILE_ID}" -o "${DESTINO}"
    rm ./cookie /tmp/intermedio
  else
    echo "$DESTINO já existe, ignorando download."
  fi
}

mkdir -p ./database

baixar_gdrive "17XkjkSdIzzgGjcVugtRi0gaZ4eOmsTt9" "./database/procuracoes.db"
baixar_gdrive "1oayVhD3knbgDLbVH00xty025dqZlltnv" "./database/pessoas.db"
baixar_gdrive "1bs5lM3wx2m46RTND0WkpPwxjJzDp2ynY" "./database/instituicoes.db"
baixar_gdrive "1P-2MqzjwkFWjQQmjx6qbRptivAxberJF" "./database/depositos.db"
baixar_gdrive "1t2s7XXH_k7GEh8Zkra3badjAv1t95eTl" "./database/contratos.db"
baixar_gdrive "1TCZ5ka33dC8qnnGlc_wTgC5p020ddDRj" "./database/contencioso.db"
baixar_gdrive "1ZhXoZL45trxBOLSLoxOAe2hfPN27KhKy" "./database/consorcios.db"
baixar_gdrive "1d5q9XLP0m13u2chmPWSScGX_5ndRZKmN" "./database/usuarios.db"
baixar_gdrive "1yDJfk-YvXxJSTWYd7rl0zjCwWCSNkg3U" "./database/requisicoes.db"

echo "Todos os bancos baixados!"
