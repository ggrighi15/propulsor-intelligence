#!/bin/bash

echo "INICIANDO SINCRONIZAÇÃO DO CODESPACE COM O GITHUB"

# Configura o nome do branch principal
BRANCH="main"

# Etapa 1: Atualiza o repositório remoto localmente com rebase (preserva histórico limpo)
echo "Atualizando repositório local com rebase do branch remoto '$BRANCH'..."
git pull origin $BRANCH --rebase

# Etapa 2: Adiciona todas as mudanças no Codespace
echo "Adicionando todas as mudanças (novos arquivos, modificações e exclusões)..."
git add .

# Etapa 3: Commit das alterações
echo "Criando commit com mensagem automática..."
git commit -m "Atualização completa do Codespace para o repositório remoto"

# Etapa 4: Envia para o GitHub
echo "Enviando alterações para o GitHub no branch '$BRANCH'..."
git push origin $BRANCH

echo "SINCRONIZAÇÃO CONCLUÍDA COM SUCESSO"
