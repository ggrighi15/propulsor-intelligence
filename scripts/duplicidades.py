from __future__ import annotations

import argparse
import logging
import sqlite3
from pathlib import Path
import sys

import pandas as pd
from utils import DATA_DIR

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def verificar(db_path: Path, tabela: str, coluna: str) -> pd.DataFrame:
    try:
        with sqlite3.connect(db_path) as conn:
            existe = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (tabela,),
            ).fetchone()
            if not existe:
                return pd.DataFrame()
            info = conn.execute(f"PRAGMA table_info('{tabela}')").fetchall()
            if coluna not in [row[1] for row in info]:
                return pd.DataFrame()
            df = pd.read_sql_query(
                f"SELECT {coluna}, COUNT(*) AS qtd FROM '{tabela}' "
                f"GROUP BY {coluna} HAVING COUNT(*) > 1",
                conn,
            )
            return df
    except sqlite3.DatabaseError:
        logging.error("Arquivo inválido: %s", db_path)
        return pd.DataFrame()


def main() -> None:
    parser = argparse.ArgumentParser(description="Checar duplicidades em bancos")
    parser.add_argument("tabela")
    parser.add_argument("coluna")
    args = parser.parse_args()

    db_files = sorted(DATA_DIR.glob("*.db"))
    if not db_files:
        logging.warning("Nenhum arquivo .db encontrado em %s", DATA_DIR)
        return

    for db in db_files:
        df = verificar(db, args.tabela, args.coluna)
        if not df.empty:
            logging.info("Duplicidades em %s -> %s.%s:", db.name, args.tabela, args.coluna)
            for _, row in df.iterrows():
                logging.info("  %s (%d ocorrências)", row[args.coluna], row["qtd"])


if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    main()
