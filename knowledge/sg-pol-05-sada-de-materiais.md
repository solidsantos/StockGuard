# SG-POL-05 — Saída de materiais

**Versão:** 1.0 | **Status:** vigente | **Fonte:** Manual fictício StockGuard 1.0 (material didático)

**Palavras-chave:** saida baixa retirada consumo movimento OUT negativo insuficiente

## Política e orientações

Uma saída OUT reduz o estoque por consumo, entrega ou transferência. A quantidade deve ser inteira positiva. O sistema deve recusar saídas superiores ao saldo disponível, preservando o registro e sem permitir estoque negativo.
Registre motivo para auditoria. Um item que ficar abaixo ou igual ao mínimo após a saída será detectado na próxima execução de /automation/check.
Exemplo: saldo 7 e saída 9 são inválidos; a operação retorna conflito de negócio e não grava movimentação.
