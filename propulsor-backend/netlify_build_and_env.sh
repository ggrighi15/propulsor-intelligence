# netlify_build.sh - Hook de build automatizado para baixar bancos e rodar backend

# 1. Baixa bancos do Google Drive usando o script anterior
echo 'Baixando bancos do Propulsor...'
bash baixar_bancos_propulsor.sh

# 2. Exporta variáveis de ambiente (ajustando caminhos para o backend)
export DB_PESSOAS="$(pwd)/database/pessoas.db"
export DB_CONTRATOS="$(pwd)/database/contratos.db"
export DB_INSTITUICOES="$(pwd)/database/instituicoes.db"
export DB_CONTENCIOSO="$(pwd)/database/contencioso.db"
export DB_PROCURACOES="$(pwd)/database/procuracoes.db"
export DB_DEPOSITOS="$(pwd)/database/depositos.db"
export DB_CONSORCIOS="$(pwd)/database/consorcios.db"
export DB_REQUISICOES="$(pwd)/database/requisicoes.db"
export DB_USUARIOS="$(pwd)/database/usuarios.db"

# 3. Rodar a build normal do frontend (ajuste o comando abaixo)
# Exemplo para Vite/React:
npm run build

# 4. Se for backend Flask, execute:
# python src/main.py

echo 'Build e bancos prontos.'

#---
# .env.example para backend Python (ajuste conforme seu backend)
DB_PESSOAS=./database/pessoas.db
DB_CONTRATOS=./database/contratos.db
DB_INSTITUICOES=./database/instituicoes.db
DB_CONTENCIOSO=./database/contencioso.db
DB_PROCURACOES=./database/procuracoes.db
DB_DEPOSITOS=./database/depositos.db
DB_CONSORCIOS=./database/consorcios.db
DB_REQUISICOES=./database/requisicoes.db
DB_USUARIOS=./database/usuarios.db
