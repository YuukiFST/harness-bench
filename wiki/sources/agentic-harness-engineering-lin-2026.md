---
title: Agentic Harness Engineering (Lin et al., 2026)
type: source
summary: AHE evolui harnesses por observabilidade; 24,7 pp entre harnesses, Succ/Mtok no apendice
tags: [harness, succ-mtok, pass-at-1, observabilidade, terminal-bench]
created: 2026-09-10
updated: 2026-09-25
dated: 2026-05-18
sources: []
---

# Agentic Harness Engineering (Lin et al., 2026)

## Identificacao

- Titulo: *Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses*.
- Autores: Jiahang Lin, Shichun Liu, Chengjun Pan, Lizhi Lin, Shihan Dou, Zhiheng Xi, Xuanjing Huang, Hang Yan, Zhenhua Han, Tao Gui, Yu-Gang Jiang (Fudan, Peking, Shanghai Qiji).
- arXiv:2604.25850v4 [cs.CL], 18 maio 2026. 35 paginas no PDF.
- *Preprint*, nao revisado por pares.
- PDF: `raw/sources/2604.25850-lin-agentic-harness-engineering.pdf`. HTML: <https://arxiv.org/html/2604.25850v4>.
- Extraido com `bin/pdf-to-md.py` (PyMuPDF, duas colunas) e conferido contra o HTML v4. Tudo abaixo refere-se a **v4**.

## Referencia ABNT (como citada no projeto)

LIN, Jiahang; LIU, Shichun; PAN, Chengjun; LIN, Lizhi; DOU, Shihan; XI, Zhiheng; HUANG, Xuanjing; YAN, Hang; HAN, Zhenhua; GUI, Tao; JIANG, Yu-Gang. **Agentic harness engineering**: observability-driven automatic evolution of coding-agent harnesses. arXiv:2604.25850, 2026. *Preprint*, nao revisado por pares. Disponivel em: https://arxiv.org/abs/2604.25850. Acesso em: 28 ago. 2026.

## Resumo (abstract, verbatim EN)

> "Harnesses are now central to agent performance, mediating how models interact with tools and execution environments."

Metodo: loop fechado AHE com tres pilares de observabilidade — (1) observabilidade de componentes (cada componente editavel vira arquivo versionavel), (2) observabilidade de experiencia (milhoes de tokens de trajetoria destilados em corpus navegavel), (3) observabilidade de decisao (cada edicao declara predicao verificada no round seguinte). Dez iteracoes elevam pass@1 no Terminal-Bench 2 de 69,7% para 77,0%, superando o *harness* humano Codex-CLI (71,9%) e baselines auto-evolutivas ACE e TF-GRPO. O *harness* congelado transfere sem re-evolucao: no SWE-bench-verified lidera com 12% menos tokens que a semente, e no Terminal-Bench 2 ganha +5,1 a +10,1 pp em tres familias de modelos alternativas.

## Definicoes (verbatim EN, com traducao de trabalho)

- *Harness* (Secao 1): "the system prompt that shapes work style, the tools that expose the file system and shell, and the middleware that controls context, execution, and recovery. This collection of model-external, editable components is collectively referred to as the agent's *harness*." Traducao: *harness* = o conjunto de componentes externos ao modelo e editaveis.
- Tese (Secao 1): "Harness design materially shifts task completion on long-horizon coding benchmarks, even with the base model held fixed, making harness engineering a first-class lever for improving coding agents."
- Especificidade (Secao 1): "the optimal harness is model-specific: a harness tuned for one base model often underperforms on another and must be re-adapted as the base model changes."
- Sete componentes (Secao 3.1, NexAU): system prompt, tool description, tool implementation, middleware, skill, sub-agent configuration, long-term memory.
- Semente minima (Secao 3.1): "Our seed harness is deliberately minimal: a single shell-execution tool, no middleware, no skills, no sub-agents." Justificativa metodologica pronta para o *harness* zero deste projeto.

## Numeros aproveitaveis (denominador completo)

| Achado | Modelo | *Harness* | Benchmark | n | Data |
|---|---|---|---|---|---|
| 47,2% / 62,9% / 71,9% pass@1 (OpenCode / Terminus-2 / Codex) = 24,7 pp de dispersao | modelo nao declarado na Tabela 1 (§4.1 fixa GPT-5.4 so para os agentes do AHE) | 3 *harnesses* humanos | Terminal-Bench 2, 89 tarefas | k=2 | 2026 |
| 74,6%-75,6% acuracia empatada com 679/582/526/461 mil tokens por tarefa (~47% de variacao de custo) | mesmo modelo | ACE / TF-GRPO / NexAU0 / AHE | SWE-bench-verified, 500 tarefas | agregado | 2026 |
| 69,7% -> 77,0% em 10 iteracoes AHE | GPT-5.4 high | evolucao AHE | Terminal-Bench 2 | campanha unica | 2026 |
| +5,1 a +10,1 pp cross-family | 3 familias alternativas | *harness* congelado | Terminal-Bench 2 | transfer | 2026 |
| Falhas de infra contam 0 no pass@1 mas sao excluidas da media de tokens | — | convencao | Apendice A | — | — |

## Metrica Succ/Mtok

Definida na Eq. (2), Apendice A: `pass@1 x 10^6 / media de tokens por execucao`. Aparece so na Tabela 5 do apendice. E a metrica primaria adotada pelo projeto (custo por tarefa concluida).

## Limitacoes declaradas (verbatim)

- "This work studies a promising but high-variance setting, and the scope of our claims should be interpreted accordingly."
- Orcamento de passos e timeout ajustados ao GPT-5.4: numeros cross-model confundem portabilidade com acoplamento ao ponto de operacao.
- Sem desvio-padrao, sem barras de erro, k=2 por tarefa. O projeto faz melhor: n>=3 e dispersao reportada (source: [[adding-error-bars-miller-2024]]).
- Nao reporta dolares, wall-clock por execucao, contagem de turnos ou de chamadas de ferramenta.

## Uso no projeto

- Justificativa: dispersao de 24,7 pp entre *harnesses* humanos (Tabela 1); o artigo nao diz que o modelo e o mesmo nas tres linhas.
- Referencial: definicao operacional de *harness* e tese da alavanca de primeira classe.
- Material e metodo: Succ/Mtok como metrica primaria; semente minima como precedente do *harness* zero; convencao de contagem do Apendice A.
- Limitacoes: campanha unica sem variancia; efeito especifico do modelo.

### Auditoria de conteudo 2026-09-11

- Citada em: §2 [49]-[50], [52], [55].
- Afirmacao sustentada: definicao §1 verbatim; Tabela 1 (OpenCode 47,2% / Codex 71,9%, TB2, 89 tarefas; o artigo nao declara o modelo dos *harnesses* humanos, ver [[2026-09-25-verificacao-referencias-projeto]]); Succ/Mtok no Apendice A.
- Veredito: CONCRETA; 24,7 pp e diferenca calculada da Tabela 1, nao frase do artigo. Detalhe em [[2026-09-11-auditoria-conteudo-referencias]].

## Contradictions

- Nenhuma interna registrada. Para tensoes com outras fontes, ver [[binding-constraint-thesis]] e [[atribuicao-harness-vs-modelo]].
