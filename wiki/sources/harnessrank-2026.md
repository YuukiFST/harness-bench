---
title: HarnessRank (2026)
type: source
summary: Ranking de harnesses com modelo fixo; timeout e resultado, tokens sem cache
tags: [harness, ranking, metodologia, terminal-bench, tokens]
created: 2026-09-10
updated: 2026-09-11
dated: 2026-08-28
sources: []
---

# HarnessRank (2026)

## Identificacao

- *HarnessRank: coding-agent harness rankings*. https://harnessrank.net/. Acesso em 28 ago 2026 (conteudo corrente, sem linhas publicadas ainda).
- Pratica publicada (site), nao revisada por pares.

## Referencia ABNT (como citada no PCC)

HARNESSRANK. **HarnessRank**: coding-agent harness rankings. 2026. Disponivel em: https://harnessrank.net/. Acesso em: 28 ago. 2026.

## Metodologia (verbatim na essencia)

- "We run several of them on the same benchmark with the same model, so each score reflects the harness, not the model behind it." Benchmark atual: terminal-bench-2.1.
- Escore = fracao de tarefas resolvidas, media de varias runs, com ± de variacao. Custo/tokens ao lado como contexto, nunca mudando a ordem.
- So contam runs completas e limpas; quebra de maquina/setup, interrupcao e sem pass/fail claro sao descartadas (nao refletem o *harness*).
- **Timeout e resultado, nao repeticao**: sem pass no verificador, conta como falha.
- Eficiencia por **tokens sem cache** por tarefa (input fresco + output / tarefas; leituras de cache excluidas — contar cache mediria contexto repetido).
- Custo so quando emitido pelo *harness*/provedor; sem estimativa propria (senao N/A). Velocidade fora do ranking (maquina + capacidade do provedor nao sao *harness*).

## Uso no PCC

- Precedente de pratica para H1 com modelo fixo + dispersao reportada.
- Regras adotaveis: timeout-como-resultado, descarte documentado (vs falha), tokens sem cache como eficiencia, custo reportado-nao-estimado.

### Auditoria de conteudo 2026-09-11

- Citada em: §2 [52].
- Afirmacao sustentada: "ordena por custo".
- Veredito: DIVERGENTE: ordena por taxa de aprovacao; custo/tokens nao afetam a ordem; sem linhas publicadas. Detalhe em [[2026-09-11-auditoria-conteudo-referencias-pcc]].

