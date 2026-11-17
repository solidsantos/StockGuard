# SG-POL-11 — Devoluções de material

**Versão:** 1.0 | **Status:** vigente | **Fonte:** Manual fictício StockGuard 1.0 (material didático)

**Palavras-chave:** devolução retorno entrada avaria produto

## Política e orientações

Uma devolução de unidade utilizável deve ser registrada como entrada IN com motivo adequado. Materiais danificados ou em quarentena não devem voltar ao saldo disponível antes da inspeção. O modelo da aula não possui status de quarentena, portanto oriente o registro administrativo fora da API até confirmação do estado físico.
Evite usar ADJUST para mascarar devoluções: o tipo IN preserva o significado operacional do evento.
Exemplo: colaborador devolve três adaptadores em bom estado; registrar IN quantidade=3 e motivo "devolução conferida".
