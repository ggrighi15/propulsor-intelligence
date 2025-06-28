# Script: Conversão de Excel (.xlsx) para CSV (modelo Instituições) — 100% PRONTO PARA WINDOWS
# Gustavo: Caminho raw string, checagem robusta, feedback direto e tudo pronto pra batch.

import pandas as pd
from pathlib import Path

# === CONFIGURAÇÃO: AJUSTE AQUI O CAMINHO DOS ARQUIVOS ===
CAMINHO_XLSX = r"C:\ulsor\propulsor-intelligence\propulsor-backend\database\Smart Report - Configuração Societário - Instituições (So_02)_2025_06_23_09_56_32_67.xlsx"
CAMINHO_CSV = r"C:\ulsor\propulsor-intelligence\propulsor-backend\database\importar_instituicoes.csv"

# ============= CHECKLIST DE EXECUÇÃO =============
def checagem_basica(path):
    if not Path(path).exists():
        print(f"[ERRO] Arquivo não encontrado:\n  {path}")
        print("→ Verifique o caminho, extensao ou se o arquivo está aberto no Excel (tem que fechar tudo).\n→ Caminho com espaço ou caractere especial pode dar pau se não copiar pelo explorer.")
        raise FileNotFoundError(f"Arquivo Excel não encontrado: {path}")
    return True

checagem_basica(CAMINHO_XLSX)

# ===== EXECUÇÃO DA CONVERSÃO =====
try:
    # 1. Carrega Excel
    xls = pd.ExcelFile(CAMINHO_XLSX)
    print("Abas encontradas:", xls.sheet_names)
    aba = xls.sheet_names[0]  # usa a primeira aba (ajuste se quiser outra)
    df = pd.read_excel(CAMINHO_XLSX, sheet_name=aba)
    print("Colunas detectadas:", list(df.columns))

    # 2. Mapeamento dinâmico das colunas para o padrão do banco
    colunas_banco = ['instituicao', 'tipo_instituicao', 'status', 'data_constituicao', 'tipo_de_capital', 'pasta', 'nucleo', 'cnpj']
    mapa = {}
    for col in df.columns:
        for alvo in colunas_banco:
            if alvo.replace('_', '').lower() in col.replace('_', '').lower():
                mapa[col] = alvo
                break
    if mapa:
        df = df.rename(columns=mapa)

    # 3. Mantém apenas as colunas do banco e ajusta ordem
    df = df[[c for c in colunas_banco if c in df.columns]]

    # 4. Remove linhas totalmente vazias
    df = df.dropna(how='all')

    # 5. Validação final e exporta CSV
    if df.empty:
        print('[ALERTA] Nenhuma linha válida encontrada para exportar!')
    else:
        df.to_csv(CAMINHO_CSV, index=False)
        print(f'[OK] CSV gerado em: {CAMINHO_CSV}')
        print(df.head(10))

except Exception as e:
    print('[ERRO CRÍTICO]:', e)
    print('Falha ao processar. Reveja caminho do arquivo e a planilha.')
