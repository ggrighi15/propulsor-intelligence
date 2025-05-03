
@echo off
REM Navega até a pasta do projeto
cd /d C:\propulsor-intelligence

REM Inicializa o repositório Git
git init

REM Adiciona origem remota (AJUSTE O LINK ABAIXO COM O REPO REAL)
git remote add origin https://github.com/ggrighi15/propulsor-intelligence.git

REM Configura Git globalmente com os dados fornecidos
git config --global user.name "ggrighi15"
git config --global user.email "ggrighi15@gmail.com"

REM Cria arquivo .gitignore padrão
echo venv/ > .gitignore
echo __pycache__/ >> .gitignore
echo *.pyc >> .gitignore
echo *.zip >> .gitignore

REM Cria um README simples
echo # Propulsor Intelligence > README.md
echo Projeto automatizado por Gustavo com suporte de IA >> README.md

REM Adiciona tudo e faz commit inicial
git add .
git commit -m "🚀 Commit inicial do Propulsor Intelligence"

REM Cria branch main e faz push
git branch -M main
git push -u origin main --force

pause
