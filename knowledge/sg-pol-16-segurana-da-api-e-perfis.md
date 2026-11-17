# SG-POL-16 — Segurança da API e perfis

**Versão:** 1.0 | **Status:** vigente | **Fonte:** Manual fictício StockGuard 1.0 (material didático)

**Palavras-chave:** segurança autorização autenticação token permissão acesso

## Política e orientações

O protótipo didático não implementa autenticação de usuários, mas esse fato deve ser declarado na documentação. Em produção, diferencie permissão de consulta, cadastro, movimentação e ajuste, implemente autorização e mantenha trilhas de auditoria.
Nunca interprete uma resposta da IA como permissão para mudar estoque. Apenas as rotas de negócio aplicam validações e escrevem no banco.
Exemplo: uma pergunta no Help sobre ajuste de saldo não deve executar ADJUST automaticamente.
