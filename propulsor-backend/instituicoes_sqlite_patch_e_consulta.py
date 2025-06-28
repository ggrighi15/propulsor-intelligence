# Script patch e consulta instituições — banco já pronto
# Gustavo, aqui operamos o .db de instituições sem contar número de registro.

import sqlite3
import pandas as pd
from pathlib import Path

CAMINHO_DB = r"C:\ulsor\propulsor-intelligence\propulsor-backend\database\instituicoes.db"

# 1. Checagem
if not Path(CAMINHO_DB).exists():
    raise FileNotFoundError(f"DB não encontrado: {CAMINHO_DB}")

# 2. Consulta total

def listar_instituicoes():
    with sqlite3.connect(CAMINHO_DB) as conn:
        df = pd.read_sql_query("SELECT * FROM instituicoes", conn)
    print(df.head())
    return df

# 3. Atualizar instituição

def atualizar_instituicao(id, dados):
    with sqlite3.connect(CAMINHO_DB) as conn:
        sets = ', '.join([f"{col}=?" for col in dados])
        valores = list(dados.values()) + [id]
        conn.execute(f"UPDATE instituicoes SET {sets} WHERE id=?", valores)
        conn.commit()
        print(f'[OK] Atualizado ID {id}:', dados)

# 4. Uso exemplo (não conta total de registros)
if __name__ == "__main__":
    listar_instituicoes()
    # Exemplo:
    # atualizar_instituicao(2, {'status': 'Inativo'})
