@echo off
REM Ativa o ambiente virtual, executa painel e inicia sincronização automática
call .\venv\Scripts\activate.bat

REM Executa o painel principal
start "" python app.py

REM Inicia o auto sync do repositório
start "" cmd /c auto_sync.bat

REM Sincroniza arquivos da pasta Contencioso com o GitHub
cd Contencioso
git add 03-2025.xlsx
git add relatorio_risco_estruturado.xlsx
git add relatorio_valores_em_ordem_correta.xlsx
git commit -m "feat(contencioso): atualiza planilhas locais"
git push origin main
cd..
