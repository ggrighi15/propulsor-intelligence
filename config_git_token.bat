
@echo off
REM Configura Git com nome e email
git config --global user.name "ggrighi15"
git config --global user.email "ggrighi15@gmail.com"

REM Define a URL remota do repositório com HTTPS
git remote set-url origin https://github.com/ggrighi15/propulsor-intelligence.git

REM Mensagem de sucesso
echo Git configurado com sucesso para ggrighi15.
echo Em seu próximo 'git push', use:
echo.
echo   Username: ggrighi15
echo   Password: [cole o seu Personal Access Token]
echo.
echo O Windows deve salvar essa autenticação automaticamente.
pause
