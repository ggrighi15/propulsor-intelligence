#!/bin/bash
set -e
dbdir="database"
mkdir -p "$dbdir"

declare -a ids=(
"17XkjkSdIzzgGjcVugtRi0gaZ4eOmsTt9"
"1oayVhD3knbgDLbVH00xty025dqZlltnv"
"1bs5lM3wx2m46RTND0WkpPwxjJzDp2ynY"
"1P-2MqzjwkFWjQQmjx6qbRptivAxberJF"
"1t2s7XXH_k7GEh8Zkra3badjAv1t95eTl"
"1TCZ5ka33dC8qnnGlc_wTgC5p020ddDRj"
"1ZhXoZL45trxBOLSLoxOAe2hfPN27KhKy"
"1d5q9XLP0m13u2chmPWSScGX_5ndRZKmN"
"1yDJfk-YvXxJSTWYd7rl0zjCwWCSNkg3U"
)
declare -a names=(
"procuracoes.db"
"pessoas.db"
"instituicoes.db"
"depositos.db"
"contratos.db"
"contencioso.db"
"consorcios.db"
"usuarios.db"
"requisicoes.db"
)
for i in "${!ids[@]}"; do
    echo "Baixando ${names[$i]} ..."
    curl -L "https://drive.google.com/uc?export=download&id=${ids[$i]}" -o "$dbdir/${names[$i]}"
done
echo "--------------------------------------"
echo "Todos os bancos baixados para $dbdir"
