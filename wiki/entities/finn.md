---
title: Finn
type: entity
summary: SaaS de financeiro por voz do autor; referencia construida pelo autor, depois reconstruida do zero por OpenCode e Pi
tags: [finn, especificacao, saas, unidades, bracos]
created: 2026-09-14
updated: 2026-09-24
sources: [wiki/sources/frontierharness-runta-2026.md, wiki/sources/helmsman-skill-yuukifst-2026.md, wiki/sources/effective-harnesses-young-2025.md]
---

# Finn

SaaS universal de financeiro por voz: a empresa cliente fala com o proprio financeiro por voz (WhatsApp, PWA, web, Android) e recebe lancamento, relatorio e aviso no celular. Repositorio `github.com/YuukiFST/Finn` (referencia YuukiFST, 2026b desde 2026-09-15; era 2026a). Especificado antes do experimento em 21 issues fechadas sob o mapa #1, mapeadas com a skill Helmsman do autor (source: [[helmsman-skill-yuukifst-2026]]): issues #2-#10 = decisoes do dono; #11-#22 = decisoes tecnicas com locks, das quais #11-#13 foram pesquisadas por subagentes.

## Decisoes fixas (issues #1-#22)

- Custo zero por padrao: Whisper local (large-v3-turbo + VAD + prompt do tenant) + palavras-chave; IA por API atras de flag por tenant, desligada por padrao (#4, #12, #13, #17).
- Multi-tenant em banco unico, `tenant_id` em tudo, roteamento pelo remetente (#15); matriz papel x acao x recurso com deny-escrita por padrao, gate no tRPC apos parse da intencao, negacao com motivo (#3, #16).
- Pipeline unico em 7 passos: audio, texto, intencao (keywords + Zod), gate, executar/negar, resposta via push (#14); toda escrita confirma antes de valer, leitura direta (#5, #20).
- Log minimo sempre + historico curto TTL 30 d, sem audio (#6, #21); agendador com fila, retry e centro de avisos, push-first (#7, #18); relatorio unico com 3 saidas (voz resumida, PDF, painel com DRE) (#8, #19); funil nao-cliente, PIX + boleto com webhook, lock um-app-por-numero (#9, #22); WhatsApp cobrado por entrega pos 01-10-2026 (#11).
- Pilha fixada pelo dono: TanStack Start, TypeScript, React, tRPC, Drizzle ORM, PostgreSQL, Better Auth, Zod, Vitest, pnpm.

## No projeto

Produto do experimento. Desde 2026-09-24 o autor constroi primeiro um Finn de referencia, seguindo as *issues* #1-#22, ate ficar como quer, com o fim de cada etapa marcado por *tag* no git. Da referencia sai a especificacao congelada: `spec.md` (produto, pilha, travas, contrato de interface dos testes) e `features.json` (uma funcionalidade por entrada, com sua unidade, no formato de lista de funcionalidades de [[effective-harnesses-young-2025]], sem o campo `passes`). Cada etapa vira uma unidade, ao menos seis; as 9 unidades tiradas dos *tickets* #14-#22 (desenho de 2026-09-14) sairam. [[opencode]] e [[pi-coding-agent]] recebem os mesmos bytes e constroem o Finn do zero, unidade a unidade, num unico espaco de trabalho; o codigo da referencia nunca entra nele. Testes de aceitacao do autor por unidade, held-out, decidem o escore e precisam passar na referencia, na *tag* da unidade, antes do congelamento. Ver [[desenho-experimental-harness-fixo]]. Os dois bracos aparecem no FrontierHarness sobre o mesmo modelo (source: [[frontierharness-runta-2026]]).

## Contradictions

Nenhuma registrada.
