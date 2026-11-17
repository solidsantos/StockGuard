# SG-POL-08 — Resolução de alertas

**Versão:** 1.0 | **Status:** vigente | **Fonte:** Manual fictício StockGuard 1.0 (material didático)

**Palavras-chave:** resolver resolvido RESOLVED reposicao alerta automatico

## Política e orientações

Na próxima varredura, se stock > min_stock, qualquer alerta OPEN daquele item passa para RESOLVED e recebe data de resolução. O sistema conserva o registro resolvido, permitindo histórico.
Uma entrada de estoque não deve apagar o alerta nem resolvê-lo silenciosamente fora da varredura, pois a atividade mede explicitamente a automação.
Exemplo: havia alerta OPEN em estoque 2/mínimo 5; após entrada de 5 unidades, a varredura o resolve. Se o estoque cair novamente, um novo alerta poderá ser aberto.
