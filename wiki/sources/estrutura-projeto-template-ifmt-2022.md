---
title: Estrutura do Projeto e Template PCC (IFMT, 2022)
type: source
summary: Sumario fixo 1-6, blocos da introducao e teto de 12 linhas da justificativa
tags: [abnt, estrutura, template, nbr-15287, justificativa]
created: 2026-09-10
updated: 2026-09-10
dated: unknown
sources: []
---

# Estrutura do Projeto e Template PCC (IFMT, 2022)

## Identificacao

- Fontes: `files/Estrutura do projeto de pesquisa-aula3.pdf` (Aula 3, 8 paginas), `files/Template projeto novo3.pdf` (gabarito, 10 paginas). Departamento de Area de Informatica, Campus Octayde Jorge da Silva, 2022. Extracoes em `$TEMP/extract/aula3.md` e `template.md` via `bin/pdf-to-md.py`.
- Material institucional de ensino (nao norma ABNT em si).

## Referencia ABNT (como citada no PCC)

INSTITUTO FEDERAL DE EDUCACAO, CIENCIA E TECNOLOGIA DE MATO GROSSO. **Normas basicas e padroes para a elaboracao do Projeto de Conclusao de Curso (PCC)**. Cuiaba: Campus Octayde Jorge da Silva, Departamento de Area de Informatica, 2022.

## Estrutura exigida

Sumario fixo: 1 Introducao, 2 Referencial Teorico, 3 Material e Metodo, 4 Orcamento, 5 Cronograma, 6 Referencias. Introducao em blocos: Justificativa (2-3 paragrafos, **max 12 linhas**, com atualidade + interesse + contribuicao social e academica), Tema (1), Problema (1), Objetivo geral (1), Especificos (topicos, 1 linha cada), Metodologia (1 breve), Hipotese (encerra), Organizacao (ultimo).

## Divergencias conhecidas (ver `docs/research/estrutura-do-projeto-e-revisao-do-pcc.md`)

- NBR 15287:2025 tornou a capa opcional e a folha de rosto obrigatoria; o template (2022) mostra o inverso — o PCC traz ambos.
- Objetivos especificos do PCC tem 2-3 linhas (gabarito pede 1) — pendente.
- Marcadores `[A MEDIR/A VERIFICAR/A DEFINIR]` pendentes; cronograma em meses relativos (data nao confirmada).
- `tools/build_pcc.py` desatualizado (parado em cc15d7b): rodar sobrescreve o `.docx` — fonte da verdade e o `.docx`.
