@echo off
REM Ativa o ambiente virtual e executa o painel principal
call .\venv\Scripts\activate.bat
streamlit run app.py
pause
