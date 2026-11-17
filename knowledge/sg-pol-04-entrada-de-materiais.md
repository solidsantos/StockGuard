# SG-POL-04 — Entrada de materiais

**Versão:** 1.0 | **Status:** vigente | **Fonte:** Manual fictício StockGuard 1.0 (material didático)

**Palavras-chave:** entrada reposicao recebimento movimento IN quantidade

## Política e orientações

Uma entrada IN aumenta o saldo atual pela quantidade informada. Registre apenas unidades realmente recebidas e conferidas; pedido de compra emitido não é entrada. A quantidade de IN precisa ser maior que zero e a movimentação deve registrar o saldo anterior, o novo saldo, a data e uma justificativa.
Se a entrada elevar o estoque acima do mínimo, o alerta ainda aberto será resolvido na próxima execução da automação /automation/check. Isso é uma decisão da atividade: movimentação e varredura de alertas são operações distintas.
Exemplo: saldo 2, entrada 5, saldo final 7.
