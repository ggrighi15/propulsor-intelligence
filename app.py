# Certifique-se de instalar as dependências antes de rodar:
# pip install flask flask-cors
# pip install types-flask  # Opcional, para suporte a tipagem

from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from services.contencioso.consultas import bp as consultas_bp
import os
from dotenv import load_dotenv
try:
    from flask_cors import CORS  # flask-cors não possui pacote oficial de tipagem
except ImportError:
    CORS = None  # type: ignore
# Se você usa análise de tipo (ex: mypy), instale também:
# pip install types-flask

load_dotenv()
app = Flask(__name__, static_folder='painel')
if CORS:
    CORS(app)
app.secret_key = os.getenv('APP_SECRET_KEY', 'propulsor_secret_key_2025')
app.register_blueprint(consultas_bp)

USUARIO_PADRAO = os.getenv('DEFAULT_USERNAME', 'gustavo')
SENHA_PADRAO = os.getenv('DEFAULT_PASSWORD', 'propulsor2025')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/react-vipal')
def react_vipal():
    return send_from_directory('painel/react_vipal', 'index.html')

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

