from __future__ import annotations

import os
import re
import shutil
import sqlite3
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(os.getenv("PROPULSOR_ROOT", Path(__file__).resolve().parents[1]))
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

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
        shutil.copy(SOURCE_DB, TARGET_DB)
    else:
        Path(TARGET_DB).touch()


def sanitize_name(name: str) -> str:
    return f"mes_{name}" if re.match(r"^\d", name) else name


def append_tables(db_path: Path) -> None:
    prefix = db_path.stem
    with sqlite3.connect(TARGET_DB) as conn_dest, sqlite3.connect(db_path) as conn_src:
        tables = conn_src.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        for (table,) in tables:
            df = pd.read_sql_query(f'SELECT * FROM "{table}"', conn_src)
            dest_name = f"{prefix}_{sanitize_name(table)}"
            df.to_sql(dest_name, conn_dest, if_exists="replace", index=False)
            print(f"✅ Tabela '{table}' de '{prefix}' importada como '{dest_name}'")


def consolidar() -> None:
    copy_base()
    for db in EXTRA_DBS:
        if db.exists():
            append_tables(db)
        else:
            print(f"❌ Arquivo não encontrado: {db}")
    print("🏁 Consolidação concluída.")


if __name__ == "__main__":
    consolidar()
