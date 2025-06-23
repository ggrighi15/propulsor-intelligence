from __future__ import annotations

import logging
import shutil
import sqlite3
from pathlib import Path

import pandas as pd
from utils import DATA_DIR

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Conjuntos adicionais de bancos a consolidar
EXTRA_DBS = [
    DATA_DIR / "dados_contencioso_final.db",
    DATA_DIR / "relacionamento_contencioso.db",
    DATA_DIR / "jurisprudencias.db",
    DATA_DIR / "sistema_juridico.db",
    DATA_DIR / "consorcios.db",
]

SOURCE_DB = DATA_DIR / "contencioso.db"
TARGET_DB = DATA_DIR / "contencioso_atualizado.db"


def copy_base() -> None:
    if SOURCE_DB.exists():
        try:
            shutil.copy(SOURCE_DB, TARGET_DB)
        except Exception as e:
            logging.error("Erro ao copiar o DB: %s", e)
            logging.warning("Verifique se o arquivo está aberto ou bloqueado.")
    else:
        Path(TARGET_DB).touch()


def append_tables(db_path: Path) -> None:
    prefix = db_path.stem
    with sqlite3.connect(TARGET_DB) as conn_dest, sqlite3.connect(db_path) as conn_src:
        tables = conn_src.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        for (table,) in tables:
            df = pd.read_sql_query(f'SELECT * FROM "{table}"', conn_src)
            sanitized = f"mes_{table}" if table and table[0].isdigit() else table
            dest_name = f"{prefix}_{sanitized}"
            df.to_sql(dest_name, conn_dest, if_exists="replace", index=False)
            logging.info("Tabela '%s' de '%s' importada como '%s'", table, prefix, dest_name)


def consolidar() -> None:
    copy_base()
    for db in EXTRA_DBS:
        if db.exists():
            append_tables(db)
        else:
            logging.warning("Arquivo não encontrado: %s", db)
    logging.info("Consolidação concluída")


if __name__ == "__main__":
    consolidar()
