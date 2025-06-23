from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

from utils import DATA_DIR

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

PROPULSOR_DB = DATA_DIR / "propulsor.db"

# Exclude the main database from the automatic listing
EXCLUDE = {PROPULSOR_DB.name}


def list_databases() -> list[Path]:
    """Return all .db files in DATA_DIR except the main one."""
    return [p for p in DATA_DIR.glob("*.db") if p.name not in EXCLUDE]


def attach_databases(cursor: sqlite3.Cursor) -> None:
    for path in list_databases():
        alias = path.stem
        try:
            cursor.execute("ATTACH DATABASE ? AS ?", (str(path), alias))
        except sqlite3.OperationalError:
            alias_safe = alias.replace('"', '').replace("'", "")
            cursor.execute(f'ATTACH DATABASE "{path}" AS "{alias_safe}"')
        logging.info("%s conectado como %s", path.name, alias)


def criar_view_clientes(cursor: sqlite3.Cursor) -> None:
    query = """
        CREATE VIEW IF NOT EXISTS view_clientes AS
        SELECT * FROM pessoas.pessoas
        UNION ALL
        SELECT * FROM instituicoes.instituicoes
    """
    cursor.execute(query)
    logging.info("View 'view_clientes' criada")


def criar_propulsor_db() -> None:
    with sqlite3.connect(PROPULSOR_DB) as conn:
        cursor = conn.cursor()
        attach_databases(cursor)
        try:
            criar_view_clientes(cursor)
        finally:
            conn.commit()
    logging.info("propulsor.db criado em %s", PROPULSOR_DB)


if __name__ == "__main__":
    criar_propulsor_db()
