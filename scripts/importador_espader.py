from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

import pandas as pd
from utils import DATA_DIR, EMAIL_DIR

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

SOURCE_MAP = {
    'pessoas': ['Smart Report - Pessoas.xlsx'],
    'instituicoes': ['Smart Report - Instituicoes.xlsx'],
    'depositos': ['Smart Report - Depósitos.xlsx'],
    'requisicoes': ['Requisições.xlsx'],
    'contratos': ['BDContratos.xlsx'],
    'contencioso': ['Relatório Mensal _ Contencioso.xlsx'],
    'procuracoes': [
        'Relatório _ Procurações Públicas.xlsx',
        'Relatório _ Procurações Particulares.xlsx',
    ],
}

DB_PATH = DATA_DIR / 'propulsor.db'


def limpeza_espaider(caminho_excel: Path) -> pd.DataFrame | None:
    try:
        df = (
            pd.read_excel(caminho_excel, skiprows=4)
            .dropna(axis=1, how='all')
        )
        campos = ['Pasta', 'Número do Processo', 'ID', 'Código']
        for campo in campos:
            if campo in df.columns:
                df = df[df[campo].notnull()]
        df = df[~df.iloc[:, 0].astype(str).str.contains('Total', na=False)]
        return df
    except Exception as exc:
        logging.error('Erro ao processar %s: %s', caminho_excel, exc)
        return None


def importar():
    with sqlite3.connect(DB_PATH) as conn:
        for tabela, arquivos in SOURCE_MAP.items():
            frames = []
            for nome in arquivos:
                caminho_excel = EMAIL_DIR / nome
                if caminho_excel.exists():
                    logging.info('Importando %s para %s...', caminho_excel, tabela)
                    df = limpeza_espaider(caminho_excel)
                    if df is not None and not df.empty:
                        frames.append(df)
                    else:
                        logging.warning('Nenhum dado válido em %s', caminho_excel)
                else:
                    logging.warning('Arquivo não encontrado: %s', caminho_excel)
            if frames:
                merged = pd.concat(frames, ignore_index=True)
                merged.to_sql(tabela, conn, if_exists="replace", index=False)
                logging.info('%s importado com sucesso.', tabela)
    logging.info('Processo de importação concluído.')


if __name__ == "__main__":
    importar()
