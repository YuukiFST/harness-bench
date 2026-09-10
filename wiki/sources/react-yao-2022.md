---
title: ReAct (Yao et al., 2022)
type: source
summary: Laco pensamento-acao-observacao; +34 pp ALFWorld e +10 pp WebShop few-shot
tags: [react, loop, controle, baseline, interpretabilidade]
created: 2026-09-10
updated: 2026-09-10
dated: 2023-03-10
sources: []
---

# ReAct (Yao et al., 2022)

## Identificacao

- Titulo: *ReAct: Synergizing Reasoning and Acting in Language Models*.
- Autores: Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao (Princeton, Google).
- arXiv:2210.03629v3 [cs.CL], 10 mar 2023. Publicado na **ICLR 2023**.
- PDF: `raw/sources/2210.03629-yao-react.pdf`.

## Referencia ABNT (como citada no PCC)

YAO, Shunyu; ZHAO, Jeffrey; YU, Dian; DU, Nan; SHAFRAN, Izhak; NARASIMHAN, Karthik; CAO, Yuan. **ReAct**: synergizing reasoning and acting in language models. arXiv:2210.03629, 2022. Trabalho apresentado na International Conference on Learning Representations (ICLR), 2023. Disponivel em: https://arxiv.org/abs/2210.03629. Acesso em: 28 ago. 2026.

## Ideia (verbatim, Secao 2)

> "we augment the agent's action space to A^ = A union L, where L is the space of language."

Pensamento (thought) nao afeta o ambiente (sem observacao); acao busca informacao externa. Raciocinar para agir + agir para raciocinar, intercalados. Em decisao, pensamentos esparsos onde o modelo decidir. Acoes QA: `search[entity]`, `lookup[string]`, `finish[answer]`.

## Numeros

- HotpotQA (EM) / FEVER (acc), PaLM-540B: ReAct 27,4/60,9 vs CoT 29,4/56,3; combos ReAct->CoT-SC 35,1/62,0 (melhor, com 3-5 amostras vs 21 do CoT-SC). Auditoria: falsos-positivos 6% vs 14% CoT.
- ALFWorld (134 jogos): ReAct 71% vs Act 45% vs BUTLER 37% (**+34 pp absolutos**), com 1-2 exemplos vs 10^5 trajetorias de imitacao.
- WebShop (500): ReAct 40,0% vs Act 30,1% (**+10 pp**) vs IL+RL 28,7%.

## Limitacoes

Gargalo de demonstracoes (contexto de in-context learning); runs principais em PaLM-540B nao-publico; intercalacao reduz flexibilidade (loops); riscos de acao no ambiente.

## Uso no PCC

- Laco de controle cientifico: pensamento-acao-observacao com LM congelado = logica exata de *harness* fixo / ACI variavel; baseline a ablar.
- Prova de que desenho de interface supera escala de treino com modelo fixo (precedente de H1).
- Taxonomia de falhas + fallback ReAct->CoT-SC como modelo de medicao (groundedness, recuperacao, custo por trajetoria de sucesso).
