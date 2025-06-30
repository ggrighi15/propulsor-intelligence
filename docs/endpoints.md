# Checklist de Endpoints por Módulo

Este documento resume os principais endpoints REST disponíveis no projeto **Propulsor**. Os bancos SQLite devem estar na pasta `database/` e cada tabela recebe automaticamente um endpoint CRUD no formato `/api/<tabela>`.

## Exemplos de Uso
- `GET /api/pessoas` — lista todos os registros da tabela `pessoas`.
- `GET /api/contratos/5` — busca o contrato com ID 5.
- `POST /api/instituicoes` — cria uma instituição.
- `PUT /api/contencioso/10` — atualiza o registro 10.
- `DELETE /api/procuracoes/3` — remove a procuração de ID 3.

Os endpoints são gerados de forma dinâmica para cada banco e tabela encontrada em `database/`.

## Exemplo de Integração
```html
<!-- Lista pessoas em uma tabela -->
<table id="pessoas-tabela"></table>
<script>
fetch('/api/pessoas/pessoas')
  .then(res => res.json())
  .then(data => {
    const tabela = document.getElementById('pessoas-tabela');
    tabela.innerHTML = `
      <tr>
        <th>ID</th><th>Nome</th><th>CPF/CNPJ</th>
      </tr>
      ${data.map(p => `
        <tr>
          <td>${p.id}</td>
          <td>${p.nome}</td>
          <td>${p.cpf_cnpj}</td>
        </tr>
      `).join('')}
    `;
  });
</script>
```

---

### Orientações para novos módulos
- Adicione o `.db` correspondente em `database/`.
- O endpoint será criado automaticamente no formato `/api/<tabela>`.
- O frontend deve consumir os dados via `fetch` a partir da pasta `static/`.

Estas diretrizes servem de referência rápida para onboarding de desenvolvedores e para a manutenção dos padrões do Propulsor.

