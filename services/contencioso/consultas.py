from __future__ import annotations

import sqlite3
from pathlib import Path
from flask import Blueprint, jsonify

from utils import DATA_DIR

bp = Blueprint('consultas_contencioso', __name__)

DB_PATH = DATA_DIR / 'propulsor.db'


def _buscar_texto(table: str, texto: str, conn: sqlite3.Connection) -> list[dict]:
    cur = conn.execute(f"PRAGMA table_info('{table}')")
    columns = [row[1] for row in cur.fetchall() if row[2].lower() == 'text']
    if not columns:
        return []
    conditions = ' OR '.join([f"lower({col}) LIKE ?" for col in columns])
    params = [f'%{texto.lower()}%'] * len(columns)
    query = f"SELECT *, '{table}' as tabela FROM {table} WHERE {conditions}"
    result = conn.execute(query, params).fetchall()
    headers = [d[0] for d in conn.execute(f"PRAGMA table_info('{table}')").fetchall()]
    return [dict(zip(headers + ['tabela'], row)) for row in result]


@bp.route('/api/consultas/vipal')
def consultar_vipal() -> 'Response':
    tabelas = ['contencioso', 'contratos']
    resultados: list[dict] = []
    if not DB_PATH.exists():
        return jsonify(resultados)
    with sqlite3.connect(DB_PATH) as conn:
        for tabela in tabelas:
            try:
                resultados.extend(_buscar_texto(tabela, 'borrachas vipal', conn))
            except sqlite3.OperationalError:
                continue
    return jsonify(resultados)
