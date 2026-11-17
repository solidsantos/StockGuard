# SG-POL-02 — Cadastro de itens e identificação

**Versão:** 1.0 | **Status:** vigente | **Fonte:** Manual fictício StockGuard 1.0 (material didático)

**Palavras-chave:** cadastro cadastrar sku nome unidade produto duplicado

## Política e orientações

Todo produto deve ter SKU único, nome compreensível, quantidade inicial não negativa e mínimo de estoque não negativo. O SKU funciona como identificador comercial estável, enquanto o id numérico é a chave interna. Não cadastre produtos repetidos com alterações apenas de caixa ou espaços do SKU; normalize o identificador antes de persistir.
Alterações em nome, mínimo, unidade ou localização são permitidas pela rota de edição. Alterações posteriores na quantidade não devem usar a edição cadastral; precisam ser registradas como movimentações.
Exemplo: SKU CABO-HDMI-02, nome Cabo HDMI 2 m, estoque inicial 8, mínimo 5, unidade UN.
