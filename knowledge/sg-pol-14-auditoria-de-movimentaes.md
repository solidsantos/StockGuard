# SG-POL-14 — Auditoria de movimentações

**Versão:** 1.0 | **Status:** vigente | **Fonte:** Manual fictício StockGuard 1.0 (material didático)

**Palavras-chave:** historico auditoria trilha motivo quando registro

## Política e orientações

O histórico de movimentações deve ser consultável por item e apresentar tipo, quantidade, saldo antes, saldo depois, data e motivo. A operação não apaga nem reescreve movimentos antigos no projeto da disciplina.
Em ambiente de produção, inclua usuário responsável, correlação da requisição e regras de retenção; esses campos não são obrigatórios no MVP didático.
Exemplo: uma reposição IN seguida de uma baixa OUT deve produzir duas entradas distintas no histórico.
