from __future__ import annotations

import os
import sqlite3
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(os.getenv('PROPULSOR_ROOT', Path(__file__).resolve().parents[1]))
BASE_DIR = ROOT_DIR / 'data'
EMAIL_DIR = ROOT_DIR / 'emails'

BASE_DIR.mkdir(parents=True, exist_ok=True)
EMAIL_DIR.mkdir(parents=True, exist_ok=True)

excel_files = {
    'pessoas': EMAIL_DIR / 'Smart Report - Pessoas.xlsx',
    'instituicoes': EMAIL_DIR / 'Smart Report - Instituicoes.xlsx',
    'depositos': EMAIL_DIR / 'Smart Report - Depósitos.xlsx',
    'requisicoes': EMAIL_DIR / 'Requisições.xlsx',
    'contratos': EMAIL_DIR / 'BDContratos.xlsx',
    'contencioso': EMAIL_DIR / 'Relatório Mensal _ Contencioso.xlsx',
    'procuracoes_publicas': EMAIL_DIR / 'Relatório _ Procurações Públicas.xlsx',
    'procuracoes_particulares': EMAIL_DIR / 'Relatório _ Procurações Particulares.xlsx'
}

tabelas = {
    'pessoas': ['pessoas'],
    'instituicoes': ['instituicoes'],
    'depositos': ['depositos'],
    'requisicoes': ['requisicoes'],
    'contratos': ['contratos'],
    'contencioso': ['contencioso'],
    'procuracoes': ['procuracoes_publicas', 'procuracoes_particulares']
}

DB_PATH = BASE_DIR / 'propulsor.db'


def limpeza_espaider(caminho_excel: Path) -> pd.DataFrame | None:
    try:
        df = pd.read_excel(caminho_excel, skiprows=4)
        df.dropna(axis=1, how='all', inplace=True)
        campos_chave = ['Pasta', 'Número do Processo', 'ID', 'Código']
        for campo in campos_chave:
            if campo in df.columns:
                df = df[df[campo].notnull()]
        df = df[~df.iloc[:, 0].astype(str).str.contains('Total', na=False)]
        return df
    except Exception as exc:
        print(f'Erro ao processar {caminho_excel}: {exc}')
        return None


def importar():
    with sqlite3.connect(DB_PATH) as conn:
        for tabela, chaves in tabelas.items():
            frames = []
            for chave in chaves:
                caminho_excel = excel_files[chave]
                if caminho_excel.exists():
                    print(f'Importando {caminho_excel} para {tabela}...')
                    df = limpeza_espaider(caminho_excel)
                    if df is not None and not df.empty:
                        frames.append(df)
                    else:
                        print(f'⚠️ Nenhum dado válido em {caminho_excel}')
                else:
                    print(f'❌ Arquivo não encontrado: {caminho_excel}')
            if frames:
                merged = pd.concat(frames, ignore_index=True)
                merged.to_sql(tabela, conn, if_exists="replace", index=False)
                print(f'✅ {tabela} importado com sucesso.')
    print('🏁 Processo de importação concluído.')


if __name__ == "__main__":
    importar()
