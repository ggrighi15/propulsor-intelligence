@echo off
setlocal

set BRANCH=main
echo ========================================
echo  SINCRONIZANDO PROJETO COM O GITHUB
echo ========================================

echo.
echo [1] Atualizando do repositório remoto...
git pull origin %BRANCH% --rebase

echo.
echo [2] Adicionando arquivos alterados...
git add .

echo.
echo [3] Criando commit...
git commit -m "Atualização completa do Codespace para o repositório remoto"

echo.
echo [4] Enviando para o GitHub...
git push origin %BRANCH%

echo.
echo ========================================
echo  CONCLUÍDO COM SUCESSO
echo ========================================

endlocal
pause