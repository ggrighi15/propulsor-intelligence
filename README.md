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
