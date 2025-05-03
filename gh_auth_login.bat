
@echo off
REM Verifica se GitHub CLI está instalado
where gh >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo GitHub CLI não encontrado. Baixando...
    powershell -Command "Invoke-WebRequest -Uri https://github.com/cli/cli/releases/download/v2.0.0/gh_2.0.0_windows_amd64.msi -OutFile gh_cli.msi"
    msiexec /i gh_cli.msi /quiet
)

echo.
echo ===============================
echo AUTENTICACAO GITHUB VIA TOKEN
echo ===============================
echo.
echo OBS: Gere seu token em https://github.com/settings/tokens
echo.
set /p GITHUB_TOKEN=Digite seu GitHub Token Pessoal (PAT):

REM Autentica com o token fornecido
echo %GITHUB_TOKEN% | gh auth login --with-token

echo.
echo ✅ Autenticado com sucesso!
pause
