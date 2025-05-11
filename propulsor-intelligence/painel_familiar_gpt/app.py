from flask import Flask, render_template, request, redirect, session
import openai
from dotenv import load_dotenv
import os
load_dotenv()
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Config da OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

USERS = {
    'regina': {'senha': 'regina123', 'modo': 'senior'},
    'arnaldo': {'senha': 'arnaldo123', 'modo': 'senior'},
    'thais': {'senha': 'thais123', 'modo': 'senior'},
    'carolina': {'senha': 'carol123', 'modo': 'moderno'},
    'giovana': {'senha': 'giovana123', 'modo': 'moderno'},
    'admin': {'senha': 'admin123', 'modo': 'admin'}
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome'].lower()
        senha = request.form['senha']
        if nome in USERS and USERS[nome]['senha'] == senha:
            session['usuario'] = nome
            return redirect('/painel')
        return render_template('login.html', erro='Usuário ou senha inválidos.')
    return render_template('login.html')

@app.route('/painel', methods=['GET', 'POST'])
def painel():
    if 'usuario' not in session:
        return redirect('/')
    usuario = session['usuario']
    modo = USERS[usuario]['modo']
    resposta = ''
    if request.method == 'POST':
        pergunta = request.form['pergunta']
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": pergunta}]
        )
        resposta = completion.choices[0].message['content']
    return render_template('painel.html', usuario=usuario, modo=modo, resposta=resposta)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)