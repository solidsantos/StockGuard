# SG-POL-19 — Perguntas frequentes do operador

**Versão:** 1.0 | **Status:** vigente | **Fonte:** Manual fictício StockGuard 1.0 (material didático)

**Palavras-chave:** perguntas frequentes faq como fazer alerta produto ajuda

## Política e orientações

Pergunta: "Como sei quais itens exigem reposição?" Execute POST /automation/check e consulte GET /alerts; um item exige atenção quando stock <= min_stock.
Pergunta: "Como reponho cinco unidades?" Registre POST /items/{id}/movements com type=IN, quantity=5, reason; depois execute a varredura para resolver alertas, se stock > min_stock.
Pergunta: "Posso mudar saldo com PATCH do cadastro?" Não. PATCH /items/{id} modifica atributos cadastrais; alterações de saldo passam pelo histórico de movimentos.
Pergunta: "Por que a IA não atualiza estoque?" O Help oferece orientações; não possui ferramentas de escrita.
