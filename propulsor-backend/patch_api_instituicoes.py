# PATCH INSTITUIÇÕES — VERSÃO OTIMIZADA (usa o .db direto)
# Gustavo, agora acessa o SQLite direto, sem CSV e sem Excel no meio. Consulta, atualiza ou insere instituições.

import sqlite3
import pandas as pd
from pathlib import Path

CAMINHO_DB = r"C:\ulsor\propulsor-intelligence\propulsor-backend\database\instituicoes.db"

# 1. Checagem básica
def checar_db(path):
    if not Path(path).exists():
        raise FileNotFoundError(f'[ERRO] DB não encontrado em: {path}')
    return True

checar_db(CAMINHO_DB)

# 2. Funções principais

def listar_instituicoes():
    with sqlite3.connect(CAMINHO_DB) as conn:
        df = pd.read_sql_query("SELECT * FROM instituicoes", conn)
    print(df.head())
    return df

def atualizar_instituicao(id, dados):
    """
    Atualiza instituição pelo id. Dados = dict(coluna: valor)
    """
    with sqlite3.connect(CAMINHO_DB) as conn:
        sets = ', '.join([f"{col}=?" for col in dados])
        valores = list(dados.values()) + [id]
        conn.execute(f"UPDATE instituicoes SET {sets} WHERE id=?", valores)
        conn.commit()
        print(f'[OK] Atualizado ID {id}:', dados)

# 3. Teste básico (só rodar se quiser ver output direto)
if __name__ == "__main__":
    print('Primeiras instituições:')
    listar_instituicoes()
    # Exemplo de update
    # atualizar_instituicao(1, {'status': 'Atualizado', 'tipo_instituicao': 'Sociedade'})
