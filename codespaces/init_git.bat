@echo off
REM Inicializa repositório Git e faz primeiro commit
git init
git config user.name "Gustavo Righi"
git config user.email "gustavo@vipal.com.br"
git remote add origin https://github.com/seu-usuario/seu-repo.git
git add .
git commit -m "🚀 Commit inicial"
git push -u origin main
pause
