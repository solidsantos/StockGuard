# SG-POL-07 — Geração de alertas de reposição

**Versão:** 1.0 | **Status:** vigente | **Fonte:** Manual fictício StockGuard 1.0 (material didático)

**Palavras-chave:** alerta aberto OPEN varredura automation check duplicidade

## Política e orientações

A rota POST /automation/check percorre os itens e cria um alerta OPEN quando stock <= min_stock e ainda não existe alerta aberto para o item. Executar a automação repetidamente não deve criar alertas OPEN duplicados.
O histórico de alertas permanece gravado. A proteção contra duplicidade deve existir também no banco com índice único parcial, não apenas em condicionais Python.
Exemplo: duas varreduras com estoque 2 e mínimo 5 devem resultar em um único alerta aberto para o mesmo item.
