# SG-POL-17 — Uso responsável da IA generativa

**Versão:** 1.0 | **Status:** vigente | **Fonte:** Manual fictício StockGuard 1.0 (material didático)

**Palavras-chave:** ia generativa help online agente assistente resposta fonte politica alucinação

## Política e orientações

O endpoint `/help` faz busca lexical nos arquivos Markdown de políticas, recupera trechos relevantes e envia somente esse contexto a um provedor de IA online integrado por API (ou a um agente online que disponha de endpoint HTTP). O Help devolve uma resposta explicativa em português e os identificadores das políticas consultadas. O aluno poderá usar um assistente de IA na web para planejar o código, mas isso, isoladamente, não implementa a integração programática do endpoint `/help`.

O assistente deve responder dentro dos limites das políticas recuperadas. Quando não houver base documental suficiente, indique a limitação; não invente saldo atual, preço, fornecedor, prazo ou aprovação de compra. O Help não executa operações de escrita, compra, movimentação nem consulta automática aos saldos. Toda movimentação permanece nos endpoints determinísticos.

As chaves da IA são segredos: ficam no `.env` local, não no repositório, nos prompts exibidos em sala ou nas respostas HTTP. Use apenas políticas fictícias do exercício ao chamar provedores externos. Um resultado gerado não equivale a autorização.

**Exemplo:** "Qual o saldo atual do SKU X?" deve direcionar à rota `GET /items` ou `GET /items/{id}`; o corpus de políticas não contém saldo em tempo real.
