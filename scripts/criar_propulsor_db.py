from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(os.getenv("PROPULSOR_ROOT", Path(__file__).resolve().parents[1]))
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

PROPULSOR_DB = DATA_DIR / "propulsor.db"

EXTERNAL_DBS = [
    "pessoas.db",
    "instituicoes.db",
    "depositos.db",
    "requisicoes.db",
    "procuracoes.db",
    "contratos.db",
    "contencioso_atualizado.db",
    "procuracoes_particulares.db",
]


def attach_databases(cursor: sqlite3.Cursor) -> None:
    for db_name in EXTERNAL_DBS:
        path = DATA_DIR / db_name
        if path.exists():
            alias = path.stem
            alias_safe = alias.replace("\"", "").replace("'", "")
            cursor.execute(f'ATTACH DATABASE "{path}" AS "{alias_safe}"')
            print(f"✅ {db_name} conectado como {alias_safe}")
        else:
            print(f"❌ Arquivo não encontrado: {path}")


def criar_view_clientes(cursor: sqlite3.Cursor) -> None:
    query = """
        CREATE VIEW IF NOT EXISTS view_clientes AS
        SELECT * FROM pessoas.pessoas
        UNION ALL
        SELECT * FROM instituicoes.instituicoes
    """
    cursor.execute(query)
    print("✅ View 'view_clientes' criada")


def criar_propulsor_db() -> None:
    with sqlite3.connect(PROPULSOR_DB) as conn:
        cursor = conn.cursor()
        attach_databases(cursor)
        try:
            criar_view_clientes(cursor)
        finally:
            conn.commit()
    print(f"🏁 propulsor.db criado em {PROPULSOR_DB}")


if __name__ == "__main__":
    criar_propulsor_db()
