
@echo off
REM Ativa o ambiente virtual
call venv\Scripts\activate

REM Configura Git se ainda não estiver configurado
git config --global user.name "Gustavo"
git config --global user.email "gustavo@example.com"

REM Adiciona todas as mudanças, comita e faz push
git add .
git commit -m "🔄 Sync automático via auto_sync.bat"
git push origin main

REM Mensagem de sucesso
echo Código sincronizado com o GitHub com sucesso!
pause
