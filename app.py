# Certifique-se de instalar as dependências antes de rodar:
# pip install flask flask-cors
# pip install types-flask  # Opcional, para suporte a tipagem

from flask import Flask, render_template, request, redirect, url_for, session
import os
from config import get_config
try:
    from flask_cors import CORS  # flask-cors não possui pacote oficial de tipagem
except ImportError:
    CORS = None  # type: ignore
# Se você usa análise de tipo (ex: mypy), instale também:
# pip install types-flask

config = get_config()
app = Flask(__name__)
if CORS:
    CORS(app)
app.secret_key = config['SECRET_KEY']

USUARIO_PADRAO = config['DEFAULT_USERNAME']
SENHA_PADRAO = config['DEFAULT_PASSWORD']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USUARIO_PADRAO and password == SENHA_PADRAO:
            session['user'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', erro='Usuário ou senha inválidos!')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        modulos = {
            'Bots': sorted(os.listdir('bots')),
            'Serviços': sorted(os.listdir('services')),
            'Painéis': sorted(os.listdir('painel'))
        }
        return render_template('dashboard.html', user=session['user'], modulos=modulos)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

