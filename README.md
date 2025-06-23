# 🚀 Propulsor Intelligence

## Estrutura para Deploy no Codespaces

Este repositório contém a infraestrutura modular do **Propulsor**, já integrada para rodar direto no Codespaces ou localmente via `.bat`.

### ✅ Estrutura consolidada
- **bots/**: Teliga_bot, Teapruma_bot, Teacher_Emma e Eva_pro
- **services/**: consorcios, cadastro_pessoas, contencioso, contratos, procuracoes,
  requisicoes, societario, financas_pessoais e ciencia_dados
- **painel/**: familiar_gpt e consorcios

### 🔐 Variáveis de ambiente
Crie um arquivo `.env` baseado em `.env.example` contendo:

```
APP_SECRET_KEY=<sua-chave>
DEFAULT_USERNAME=<usuario>
DEFAULT_PASSWORD=<senha>
```

### ▶️ Execução direta
```bash
start run_propulsor.bat
```

Ou no Linux:

```bash
./start.sh
```

### 📂 Importar relatórios Espaider
Coloque os arquivos Excel na pasta `emails/` e execute:

```bash
python scripts/importador_espader.py
```

O script gera `data/propulsor.db` com as tabelas unificadas para consulta.

### 📥 Consolidar bancos do contencioso
Coloque os arquivos `.db` adicionais na pasta `data/` e execute:

```bash
python scripts/consolidar_contencioso.py
```

Será criado `data/contencioso_atualizado.db` mesclando todas as tabelas.

### 🔗 Gerar `propulsor.db` conectado
Com os bancos na pasta `data/`, execute:

```bash
python scripts/criar_propulsor_db.py
```

O arquivo final conterá a view `view_clientes` para consulta consolidada.
