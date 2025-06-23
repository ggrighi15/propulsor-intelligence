
@echo off
REM Ativa o ambiente virtual (se existir) ou cria um novo
IF NOT EXIST venv (
    python -m venv venv
)
call venv\Scripts\activate

REM Instala dependências
pip install -r requirements.txt

REM Executa o app Flask
python app.py
