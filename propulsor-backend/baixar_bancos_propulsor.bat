@echo off
setlocal enabledelayedexpansion

REM Caminho dos bancos
set "dbdir=database"
if not exist "%dbdir%" mkdir "%dbdir%"

REM IDs e nomes dos arquivos do Google Drive
set ids[0]=17XkjkSdIzzgGjcVugtRi0gaZ4eOmsTt9
set names[0]=procuracoes.db
set ids[1]=1oayVhD3knbgDLbVH00xty025dqZlltnv
set names[1]=pessoas.db
set ids[2]=1bs5lM3wx2m46RTND0WkpPwxjJzDp2ynY
set names[2]=instituicoes.db
set ids[3]=1P-2MqzjwkFWjQQmjx6qbRptivAxberJF
set names[3]=depositos.db
set ids[4]=1t2s7XXH_k7GEh8Zkra3badjAv1t95eTl
set names[4]=contratos.db
set ids[5]=1TCZ5ka33dC8qnnGlc_wTgC5p020ddDRj
set names[5]=contencioso.db
set ids[6]=1ZhXoZL45trxBOLSLoxOAe2hfPN27KhKy
set names[6]=consorcios.db
set ids[7]=1d5q9XLP0m13u2chmPWSScGX_5ndRZKmN
set names[7]=usuarios.db
set ids[8]=1yDJfk-YvXxJSTWYd7rl0zjCwWCSNkg3U
set names[8]=requisicoes.db

REM Baixar usando PowerShell (não depende de programas extras)
for /L %%i in (0,1,8) do (
    set "id=!ids[%%i]!"
    set "name=!names[%%i]!"
    echo Baixando !name! ...
    powershell -Command "Invoke-WebRequest -Uri ('https://drive.google.com/uc?export=download&id=' + '!id!') -OutFile '%dbdir%\!name!'"
)

echo --------------------------------------
echo Todos os bancos baixados para %dbdir%
pause
