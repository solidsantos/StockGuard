# SG-POL-06 — Ajuste de inventário

**Versão:** 1.0 | **Status:** vigente | **Fonte:** Manual fictício StockGuard 1.0 (material didático)

**Palavras-chave:** ajuste contagem divergencia correção movimento ADJUST saldo

## Política e orientações

Quando a contagem física divergir do cadastro, um ajuste ADJUST define o saldo final contado. Diferentemente de IN ou OUT, a quantidade do ajuste representa o novo saldo absoluto e pode ser zero. O motivo é obrigatório para permitir auditoria posterior.
Não use ajuste para esconder perdas ou cancelar histórico: conserve todas as movimentações. A atividade não contempla autorização de gestor no ajuste, mas um sistema produtivo deveria restringir essa operação a perfis específicos.
Exemplo: sistema mostra 10, contagem física confirma 8; ADJUST quantity=8 registra anterior 10, posterior 8.
