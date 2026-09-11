---
title: Harness Handbook (Wang et al., 2026)
type: source
summary: Localizacao de comportamento em harnesses; +10 a +19 pp de win-rate com menos tokens
tags: [harness, localizacao, navegabilidade, tokens, codex, terminus]
created: 2026-09-10
updated: 2026-09-11
dated: 2026-07-14
sources: []
---

# Harness Handbook (Wang et al., 2026)

## Identificacao

- Titulo: *Harness Handbook: Making Evolving Agent Harnesses Readable, Navigable, and Editable*.
- Autores: Ruhan Wang, Yucheng Shi, Zongxia Li *et al.* (10 total, Tencent HY LLM Frontier + universidades).
- arXiv:2607.13285v1 [cs.AI], 14 jul 2026. 29 paginas.
- *Preprint*, nao revisado por pares.
- PDF: `raw/sources/2607.13285-wang-harness-handbook.pdf`.

## Referencia ABNT (como citada no PCC)

WANG, Ruhan *et al.* Harness Handbook: making evolving agent harnesses readable, navigable, and editable. arXiv:2607.13285, 2026. *Preprint*, nao revisado por pares. Disponivel em: https://arxiv.org/abs/2607.13285. Acesso em: 9 set. 2026.

## Ideia (abstract, sem rotulo no artigo)

O *harness* coordena prompts, estado, ferramentas e execucao (verbatim Secao 1): "The harness therefore determines how model capabilities are translated into system behavior." Como *harnesses* de producao sao grandes e acoplados, localizar onde editar (behavior localization) e o gargalo. Solucao: Handbook (representacao L1-L3 + registradores, via analise estatica + LLM) + BGPD (Behavior-Guided Progressive Disclosure, do geral ao detalhe com verificacao contra o fonte vivo).

## Numeros (mesmo planner/modelo, 30 pedidos por *harness*, 3 juizes)

- Win-rate: Codex **38,3% vs 28,3% (+10,0 pp)**; Terminus-2 **45,6% vs 26,7% (+18,9 pp)**.
- Tokens do planner **menores**: Codex 0,102M -> 0,089M (-12,7%); Terminus-2 0,058M -> 0,053M (-8,6%).
- F1 de localizacao +5,0 a +18,8 nas 24 comparacoes; planejador fraco (DeepSeek-V4-Pro) chega a 84,7-89,3% F1.
- Escala: Terminus-2 Python 6 arquivos vs Codex Rust 2.267 arquivos / 34.363 funcoes — ganhos nos dois extremos.

## Limitacoes

So 2 *harnesses*, 60 pedidos, 1 modelo planejador; qualidade de plano por juizes LLM, **sem execucao** ("Do NOT grade the final code diff or execution correctness").

## Uso no PCC

- Referencial: definicao de *harness* como runtime; evidencia de que internos de *harness* sao distribuidos por arquivos/estagios/estado.
- Material e metodo: protocolo BGPD como auditoria do diff pi vs oh-my-pi (enumerar todos os sites de leitura/escrita dos registradores mudados).
- Lacuna que o PCC preenche: executar *fork* vs original com modelo fixo e precificar tarefas concluidas (este artigo nao executa).

### Auditoria de conteudo 2026-09-11

- Citada em: §2 [49].
- Afirmacao sustentada: "constructs prompts, manages state, invokes tools, and coordinates execution" (Abstract).
- Veredito: CONCRETA; parafrase. Detalhe em [[2026-09-11-auditoria-conteudo-referencias-pcc]].

## Contradictions

- Padrao de verificacao oposto ao de [[scaffolding-matters-alier-forment-2026]] (juizes LLM sem execucao vs inspecao de estado): para H1/H2 vale o padrao oraculo. Ver [[adequacao-oraculo]].
