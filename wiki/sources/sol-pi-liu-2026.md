---
title: SoL-Pi (Liu et al., 2026)
type: source
summary: Auto-pesquisa no harness sobre o Pi; 4 mecanismos cortam 44,7-49,0% dos tokens e ~1/3 do custo no EdgeBench
tags: [harness, pi, auto-pesquisa, tokens, custo, edgebench, compactacao]
created: 2026-09-23
updated: 2026-09-23
dated: 2026-09-17
sources: []
---

# SoL-Pi (Liu et al., 2026)

## Identificacao

- Titulo: *SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent Harness*.
- Autores (14): Haozhe Liu, Tian Ye, Sensen Gao, Qihang Cao, Yitong Li, Mingchen Zhuge, Duomin Wang, Ruihua Zhang, Ping Luo, Jiawang Bian, Lei Zhu, Ligeng Zhu, Enze Xie, Song Han (NVIDIA, NTU, MIT). Codigo: https://github.com/NVlabs/SoL-Pi; blogue: https://nvlabs.github.io/SoL-Pi/ (links do PDF).
- arXiv:2609.20519v1 [cs.AI], 17 set. 2026. PDF: `raw/sources/2609.20519-liu-sol-pi.pdf` (baixado em 23 set. 2026, lido com `pdftotext`).
- *Preprint*, nao revisado por pares.
- Data: `dated` usa a submissao ao arXiv (17 set. 2026, carimbo lateral do PDF). O cabecalho do PDF traz "2026-08-17", a mesma data da tabela de precos usada nos custos.

## Escopo que a fonte declara

Sistema de auto-pesquisa inspirado em RSI (*recursive self-improvement*) que otimiza o *harness* para eficiencia de tokens com o modelo fixo. A busca parte do Pi e retem quatro mecanismos; a avaliacao final e em benchmark separado da busca. Os autores chamam a transferencia entre modelos de "preliminary evidence" e dizem que as contagens de busca nao estabelecem lei de escala.

## Metodo

- Busca: ~150 direcoes propostas (152 no texto, em seis familias: contexto, progresso, ferramentas, delegacao, *prompt* e politica, melhoria e avaliacao), 535 ambientes executaveis (495 de pares *issue*-PR do GitHub + 40 sinteticos com verificador no estilo Terminal-Bench 2), mais de 3.000 execucoes e mais de 60.000 interacoes agente-ambiente. Modelo de busca: GPT-5.6 Sol.
- Selecao em dois portoes fixados antes da busca e fora do controle do agente otimizador: toda metrica de capacidade dentro da tolerancia declarada e ganho em ao menos uma metrica de eficiencia.
- Avaliacao: EdgeBench (51 das 134 tarefas sao publicas; 11 usadas para aceitar candidatos congelados, 40 para a avaliacao final), isolado da busca. *Harness* congelado antes; resultado held-out nunca volta para a busca.
- Metricas: *score* medio, trafego de tokens registrado (bilhoes; *input*, leitura e escrita de *cache*, *output*) e custo de API; eficiencia = custo de API por ponto de *score*. Precos de API de 17 ago. 2026.
- O texto nao informa quantas execucoes por configuracao nem intervalo de confianca no EdgeBench.

## Os quatro mecanismos (extensoes do Pi)

1. *Action Fusion*: junta uma edicao de arquivo e o comando seguinte (teste, *build*) numa so requisicao; tira uma ida e volta ao modelo (3 chamadas viram 2).
2. *Online Context Compact*: decide compactar ao fim de cada passo do plano, quando a economia projetada de *input* supera o custo de reescrever o *cache* de *prompt*; usa a compactacao nativa do Pi.
3. *ObservationPack*: saidas de ferramenta acima de 10 KiB vao inteiras nas duas proximas requisicoes; da terceira em diante viram *handle* estavel + trecho de 1 KB, com recuperacao exata sob demanda.
4. *Evidence-Preserving Reducer*: *logs* de *build* e teste a partir de 4 KiB sao resumidos por um modelo barato (GPT-5.6 Luna) num recibo checado por verificador deterministico (schema, *hash*, *exit status*, citacoes exatas, tamanho); se falhar, volta o *log* original.

## Numeros (modelo, *harness*, benchmark, data)

EdgeBench, GPT-5.6 Sol (backend da busca), Tabela 1:

| *Harness* | Tokens (B) | Custo ($) | *Score* medio | $/*score* |
|---|---|---|---|---|
| Codex | 3,0537 | 1.787 | 34,738 | 1,0086 |
| OpenSquilla | 1,3353 | 1.243 | 24,506 | 0,9945 |
| Oh-My-Pi | 2,2235 | 1.832 | 26,921 | 1,3347 |
| OpenCode | 2,5668 | 3.422 | 29,552 | 2,2704 |
| Oh-My-Opencode | 2,5825 | 2.678 | 38,523 | 1,3633 |
| Pi | 2,1538 | 1.339 | 44,833 | 0,5855 |
| SoL-Pi [Efficiency] | 1,0990 | 894 | 42,003 | 0,4174 |
| SoL-Pi [Performance] | 2,0224 | 1.271 | 47,208 | 0,5280 |

- SoL-Pi [Efficiency] (os quatro mecanismos): 49,0% menos tokens que o Pi, 93,7% do *score* do Pi (42,0 vs 44,8), custo 33,2% menor. [Performance] (so *ObservationPack* no GPT-5.6 Sol): *score* 44,8 -> 47,2 (+5,3%), -6,1% de tokens.
- Transferencia para Opus 5 sem nova busca (Tabela 2): Claude Code 2,0045 B / $2.535 / 43,689; Pi 2,3697 B / $1.741 / 44,756; SoL-Pi [Efficiency] 1,3101 B / $1.158 / 42,224 (94,3% do *score* do Pi, -44,7% de tokens, -33,5% de custo); [Performance] (*Action Fusion*) 2,1016 B / $1.605 / 50,482.
- Figura 1(b): SoL-Pi corta o custo de API em 50,0% frente ao Codex (GPT-5.6 Sol) e 54,3% frente ao Claude Code (Opus 5).
- Economia por hora (so no resumo, sem derivacao no corpo): $8,75-$13,50 frente ao Codex e ao Claude Code nativos, $4,36-$5,71 frente ao Pi.
- Terminal-Bench 4, 63 tarefas so CPU: Codex e Pi resolvem 18, SoL-Pi 15; SoL-Pi custa 26,3% menos que o Pi ($211,12 vs $286,45) e 11,6% menos por tarefa resolvida ($14,07 vs $15,91).
- IMO 2026 em Lean 4, GPT-5.6 Sol xhigh, 6 problemas: SoL-Pi resolve 3 por $62,69; custo por problema $20,90 vs $22,89 (Codex) e $25,32 (Pi).
- Enxame de otimizacao de *kernel*, uma execucao de 2 h cada: SoL-Pi 1.127 ciclos a $60,11; agente unico 1.333 a $39,20; enxame Pi 1.366 a $82,12.
- *Cache*: com GPT-5.6 Sol a pilha completa reduz leitura de *cache* de 2,1326 B para 1,0605 B e aumenta a escrita de 0,0141 B para 0,0316 B; o custo total cai de $1.339 para $894. Os autores concluem que se deve avaliar o custo total da tarefa, nao so o reaproveitamento de *cache*.
- Os mecanismos disparam menos no Opus 5, o que os autores atribuem a busca feita so com trajetorias do GPT-5.6 Sol.

## Limitacoes declaradas

Harness treinado com trajetorias de um so modelo; custo alto do laco completo impede comparar amplitude e profundidade de busca sob orcamento fixo; "recursive efficient improvement" e visao de longo prazo, nao efeito demonstrado.

## O que acrescenta a wiki

- Mesmo modelo, mesmo benchmark: o *harness* move o *score* do EdgeBench de 24,5 (OpenSquilla) a 44,8 (Pi) e o custo de $1.243 a $3.422 com GPT-5.6 Sol. OpenCode, braco do projeto, tem o pior $/*score* da tabela.
- Mostra que, mesmo no *harness* minimo ([[pi-coding-agent]]), metade do trafego de tokens pode ser cortada mudando so o *harness*, com perda de ~6% do *score*.
- Mede trafego com leitura de *cache* incluida e custo por tabela de precos (ver [[medicao-custo-proxy-vs-relato]]).

## Paginas afetadas

[[pi-coding-agent]], [[opencode]], [[binding-constraint-thesis]], [[especificidade-modelo-inversao]], [[medicao-custo-proxy-vs-relato]].

## Contradictions

- "Comparable to Pi" (resumo) vs os numeros do proprio texto: a pilha completa fica em 93,7% (GPT-5.6 Sol) e 94,3% (Opus 5) do *score* do Pi, e no Terminal-Bench 4 resolve 15 tarefas contra 18 do Pi. O resumo nao cita a perda; o corpo da os numeros sem IC. Registrado em `_review.md`.
