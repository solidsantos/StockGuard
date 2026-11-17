# SG-POL-03 — Definição do estoque mínimo

**Versão:** 1.0 | **Status:** vigente | **Fonte:** Manual fictício StockGuard 1.0 (material didático)

**Palavras-chave:** estoque minimo limite ponto reposicao calcular alerta

## Política e orientações

O estoque mínimo é a quantidade de referência definida para cada item pela operação. Na simulação, um item exige atenção quando sua quantidade é menor OU igual ao mínimo: stock <= min_stock. A regra inclui a igualdade de propósito.
O valor mínimo deve ser revisado quando o padrão de consumo mudar. A API não calcula previsão de demanda nem lead time; a turma pode propor essas evoluções em trabalhos futuros.
Exemplo: estoque 5 e mínimo 5 geram alerta; estoque 6 e mínimo 5 não geram.
