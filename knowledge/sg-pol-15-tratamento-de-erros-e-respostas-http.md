# SG-POL-15 — Tratamento de erros e respostas HTTP

**Versão:** 1.0 | **Status:** vigente | **Fonte:** Manual fictício StockGuard 1.0 (material didático)

**Palavras-chave:** erro http 400 404 409 422 503 validação indisponibilidade

## Política e orientações

Use 201 para cadastro e movimentação criados, 200 para consultas e operações concluídas, 404 para item inexistente, 409 para SKU duplicado ou saldo insuficiente e 422 para entrada inválida pelo contrato. Se o provedor de IA online estiver indisponível, a rota de ajuda deve retornar 503 de forma explícita.
Não devolva stack trace, endereço interno do banco ou credenciais em respostas. Mensagens devem indicar a causa operacional sem expor detalhes sensíveis.
Exemplo: saída de 10 quando existem 3 unidades retorna 409; não deve alterar estoque nem histórico.
