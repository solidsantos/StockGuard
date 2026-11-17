# SG-POL-18 — Incidentes e indisponibilidade

**Versão:** 1.0 | **Status:** vigente | **Fonte:** Manual fictício StockGuard 1.0 (material didático)

**Palavras-chave:** incidente falha online agente provedor api timeout contingencia indisponivel

## Política e orientações

Quando o provedor de IA online estiver indisponível, lento, devolver 401/429/5xx ou um erro de rede, somente o `/help` deve ficar prejudicado. Cadastro, movimentações e automação de alertas são operações determinísticas e não podem depender de inferência externa. A API deve devolver 503 para falha de integração (ou 502 se o serviço responder um conteúdo inválido), sem inventar uma resposta gerada.

Se o SQLite estiver indisponível, não aceite movimentações como se houvessem sido concluídas. Em aula, quando não houver chave ou serviço externo acessível, permita testes com cliente HTTP simulado; isso valida contrato e tratamento de erros, mas não comprova uma geração real.

**Exemplo:** com `AI_API_KEY` ausente, o `/help` devolve 503; `GET /items` continua operando normalmente.
