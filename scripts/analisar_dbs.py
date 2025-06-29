from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
import sys

from utils import DATA_DIR

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def listar_tabelas(conn: sqlite3.Connection) -> list[str]:
    return [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]


def resumir_db(db_path: Path) -> None:
    try:
        with sqlite3.connect(db_path) as conn:
            tabelas = listar_tabelas(conn)
            logging.info("%s (%d tabelas)", db_path.name, len(tabelas))
            for tabela in tabelas:
                try:
                    qtd = conn.execute(f"SELECT COUNT(*) FROM '{tabela}'").fetchone()[0]
                except sqlite3.OperationalError:
                    qtd = 0
                logging.info("  %s: %d registros", tabela, qtd)
    except sqlite3.DatabaseError:
        logging.error("Arquivo inválido: %s", db_path)


def main() -> None:
    db_files = sorted(DATA_DIR.glob("*.db"))
    if not db_files:
        logging.warning("Nenhum arquivo .db encontrado em %s", DATA_DIR)
    for db in db_files:
        resumir_db(db)


if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    main()
