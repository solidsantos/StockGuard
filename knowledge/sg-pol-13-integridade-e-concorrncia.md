# SG-POL-13 — Integridade e concorrência

**Versão:** 1.0 | **Status:** vigente | **Fonte:** Manual fictício StockGuard 1.0 (material didático)

**Palavras-chave:** concorrencia transacao simultâneo banco dados integridade

## Política e orientações

Toda movimentação deve ser executada em uma transação. Primeiro leia o saldo, depois valide a operação, grave o movimento e atualize o item; em caso de erro, desfaça tudo. Na implementação SQLite de referência, BEGIN IMMEDIATE reduz a janela para atualizações concorrentes conflitantes.
Não permita saldo negativo mesmo se duas requisições chegarem próximas. Restrições no banco e testes de conflito complementam as validações do FastAPI.
Exemplo: duas saídas simultâneas não podem consumir o mesmo saldo duas vezes.
