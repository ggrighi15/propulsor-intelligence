# Checklist de Endpoints por Módulo

Este documento resume os principais endpoints REST disponíveis no projeto **Propulsor** e apresenta um exemplo de integração simples via JavaScript.

## Pessoas
- `GET /api/pessoas/pessoas` – lista todas as pessoas.
- `GET /api/pessoas/pessoas/search?campo=nome&valor=Gustavo` – busca pessoas pelo nome.

## Contratos
- `GET /api/contratos/contratos` – lista todos os contratos.
- `GET /api/contratos/contratos/search?campo=numero&valor=123` – busca contratos pelo número.

## Contencioso
- `GET /api/contencioso/contencioso` – lista todos os processos.
- `GET /api/contencioso/contencioso/search?campo=pasta&valor=001` – busca processo por pasta ou código.

## Consórcios
- `GET /api/consorcios/consorcios` – lista todos os consórcios.

## Instituições
- `GET /api/instituicoes/instituicoes` – lista todas as instituições.

## Usuários
- `GET /api/usuarios/usuarios` – lista todos os usuários.

## CRUD Genérico
Para qualquer tabela é possível realizar a consulta via:
- `GET /api/<nome_db>/<tabela>`
- `GET /api/<nome_db>/<tabela>/search?campo=CAMPO&valor=VALOR`

Os métodos `POST`, `PUT` e `DELETE` podem seguir o mesmo padrão, conforme necessidade.

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
- Crie o endpoint seguindo o padrão `/api/<db>/<tabela>`.
- O frontend deve consumir os dados via `fetch` ou AJAX a partir da pasta `static/`.

Estas diretrizes servem de referência rápida para onboarding de desenvolvedores e para a manutenção dos padrões do Propulsor.

