
@echo off
echo ===============================
echo VERIFICANDO GITHUB CLI (gh)
echo ===============================
where gh >nul 2>nul

IF %ERRORLEVEL% NEQ 0 (
    echo GitHub CLI não encontrado. Baixando instalador...
    powershell -Command "Invoke-WebRequest -Uri https://github.com/cli/cli/releases/download/v2.46.0/gh_2.46.0_windows_amd64.msi -OutFile gh_cli.msi"
    echo Instalando GitHub CLI...
    msiexec /i gh_cli.msi /quiet /norestart
    echo Instalado. Reinicie o terminal se necessário.
) ELSE (
    echo GitHub CLI já instalado.
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
