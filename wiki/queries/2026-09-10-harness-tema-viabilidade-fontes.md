---
title: Harness e eficiencia do modelo viabilidade do tema e fontes
type: query
summary: Tema do harness e viavel e ja e o do PCC; fontes novas agregam metodo e numeros
tags: [harness, tema, viabilidade, custo, desenvolvedores]
created: 2026-09-10
updated: 2026-09-10
sources: [wiki/sources/scaffolding-matters-alier-forment-2026.md, wiki/sources/frontierharness-runta-2026.md, wiki/sources/meta-harness-lee-2026.md, wiki/sources/harness-handbook-wang-2026.md, wiki/sources/stop-comparing-harness-zhang-2026.md, wiki/sources/ai-agents-that-matter-kapoor-2024.md]
---

# Harness e eficiencia do modelo: viabilidade do tema e o que agregam as fontes — as of 2026-09-10

## Veredito

O tema e viavel e, no essencial, **ja e o tema do PCC**: *harness* como variavel independente, eficiencia como custo por tarefa concluida + taxa de sucesso, modelo mantido fixo. As fontes indicadas nao mudam o tema; elas o armam com definicao simples, numeros e metodo. Ver [[agent-harness]], [[succ-mtok]], [[binding-constraint-thesis]].

## O que cada fonte agrega

- **Alier Forment et al. (2608.08654)** (source: [[scaffolding-matters-alier-forment-2026]]): a evidencia central de H1. Mesmo modelo e mesma tarefa, 20x entre *scaffoldings* e 139x num modelo local de 27B, com conclusao verificada por estado do repositorio (nunca auto-relato). Da tambem o limite de resolucao (~2x) e as cinco regras de medida que o PCC adota.
- **Meta-Harness (2603.28052)** (source: [[meta-harness-lee-2026]]): a definicao formal mais curta para desenvolvedor — programa com estado que decide o contexto do modelo a cada passo — e a prova de que *harness* se otimiza como codigo (+7,7 pp com 4x menos tokens). Sustenta o "como funciona" e o "por que importa no bolso".
- **Harness Handbook (2607.13285)** (source: [[harness-handbook-wang-2026]]): mostra que o *harness* e distribuido por arquivos e estagios (por isso um *fork* muda custo sem mudar o modelo) e da o protocolo BGPD para auditar o diff pi/oh-my-pi de H2.
- **FrontierHarness blog + site + repo**: o precedente mais proximo do recorte "desenvolvedor escolhe ferramenta". Mesmo Kimi K3, 9 *harnesses* reais (Codex, Claude Code, Pi, OpenCode, oh-my-pi entre eles): pass 50,0-66,7%, custo por pass $1,05-$18,34 (source: [[frontierharness-runta-2026]]). O repo (`frontier-harness-eval/eval`, 44 commits) publica tarefas, `eval-data.json` e skill de reproducao, com invariantes de comparabilidade (checkpoint dourado, 1 restore por tarefa, `infra_invalid` marcado, custo por `effective_cost_per_pass`).
- **Video Pi em 22 min** (Sean's AI Stories): so titulo e canal verificaveis; conteudo e data nao verificados. Serve como material ilustrativo do modelo de extensao do Pi (skills, extensoes, pacotes, bash), nao como evidencia. Nao citar numeros dele.

## Analogia do carro

HB20 na areia vs asfalto traduz bem a intuicao (mesmo motor, terreno/harness distinto, desempenho distinto) e cabe na motivacao da justificativa. Mas analogia nao e evidencia: no texto ela apresenta, os numeros decidem. Ver [[atribuicao-harness-vs-modelo]].

## Lacunas e cuidados

- **Cursor nao aparece em nenhum *benchmark* da wiki** (so como adaptador do executor Pier). A frase "vagas pedem Claude Code, Codex ou Cursor" e afirmacao do autor, sem fonte: usar como motivacao de contexto, nao como fato citado — ou levantar 20-30 anuncios como mini-survey.
- **Divergencia site vs blog FrontierHarness**: o site traz tabela extra ("median cost per successful task", $0,06-$0,29) incompativel a primeira vista com o blog ($1,05-$18,34 por pass). Nao citar a tabela do site ate reconciliar contra `results/eval-data.json` (registrado em `_review.md`).
- Versoes dos *harnesses* do FrontierHarness (Pi v0.84.2, oh-my-pi v17.4.0, OpenCode v1.18.19, Claude Code v2.1.237, Codex v0.148.0) fixam precedente de versionamento que o PCC deve copiar.
