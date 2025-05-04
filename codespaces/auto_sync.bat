@echo off
REM Sincroniza alterações com o repositório GitHub em ciclos
echo Sincronizando repositório...
call push_auto.bat
timeout /t 1800 >nul
exit
