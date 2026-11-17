# SG-POL-01 — Objetivo e escopo do estoque

**Versão:** 1.0 | **Status:** vigente | **Fonte:** Manual fictício StockGuard 1.0 (material didático)

**Palavras-chave:** estoque gestão inventário produto cadastro objetivo

## Política e orientações

O StockGuard é um sistema didático para controlar produtos físicos, movimentações e alertas de reposição. O estoque disponível representa unidades registradas e não considera reservas, pedidos de compra ou integração com fornecedores. A fonte de verdade sobre a quantidade é o SQLite acessado pela API.
Um colaborador deve usar as rotas de cadastro e movimentação para produzir alterações rastreáveis. O assistente de ajuda explica políticas; ele não deve alterar quantidades, prometer entregas, executar compras nem afirmar conhecer o saldo atual sem consultar uma rota de dados.
Exemplo: para perguntar quando reabastecer um item, consulte a política de limite mínimo; para saber a quantidade real de um SKU, use a API de itens.
