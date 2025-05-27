exports.handler = async (event) => {
  const cnpj = event.queryStringParameters?.cnpj || '00000000000000';

  const dados = {
    cnpj,
    nome: "Propulsor Tecnologia Ltda.",
    atividade: "Desenvolvimento de software sob encomenda",
    status: "Ativa"
  };

  return {
    statusCode: 200,
    body: JSON.stringify(dados)
  };
};
