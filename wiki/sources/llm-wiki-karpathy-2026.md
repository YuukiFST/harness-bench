---
title: LLM Wiki (Karpathy, 2026)
type: source
summary: Gist de Karpathy; padrao do LLM Wiki (fontes imutaveis, wiki pelo agente, index, log, lint) que este repo instancia
tags: [llm-wiki, metodo, karpathy, declaracao-de-uso, gist]
created: 2026-09-14
updated: 2026-09-15
dated: 2026-04-04
sources: []
---

# LLM Wiki (Karpathy, 2026)

## Identificacao

- Titulo: *LLM Wiki. A pattern for building personal knowledge bases using LLMs.*
- Autor: Andrej Karpathy. Gist publico no GitHub, arquivo `llm-wiki.md`.
- URL: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f (copia em `raw/sources/karpathy-2026-llm-wiki.md`, baixada em 2026-09-14).
- `dated` = data de criacao do gist mostrada pelo GitHub (4 abr. 2026); o gist nao traz data no texto. Documento de ideia, nao revisado por pares.

## Referencia ABNT (como citada no projeto)

KARPATHY, Andrej. LLM Wiki: a pattern for building personal knowledge bases using LLMs. 2026. Gist (GitHub). Disponivel em: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f. Acesso em: 14 set. 2026.

## O que o gist diz

- Problema: RAG redescobre o conhecimento a cada pergunta; nada se acumula. Proposta: o LLM "incrementally builds and maintains a persistent wiki", um conjunto de arquivos Markdown interligados entre o usuario e as fontes brutas.
- Tres camadas: **raw sources** ("These are immutable — the LLM reads from them but never modifies them"), **the wiki** (escrita e mantida pelo LLM), **the schema** (um `CLAUDE.md`/`AGENTS.md` com estrutura, convencoes e fluxos).
- Operacoes: **ingest** (ler a fonte, escrever a pagina de sintese, atualizar index, entidades e conceitos, registrar no log), **query** (responder lendo o index e as paginas; respostas boas viram paginas), **lint** (contradicoes, afirmacoes obsoletas, paginas orfas, conceitos sem pagina).
- `index.md` orientado a conteudo, atualizado a cada ingest; `log.md` cronologico e append-only, com prefixo `## [YYYY-MM-DD] ingest | Title` para ser parseavel.
- O documento se declara abstrato: "It describes the idea, not a specific implementation"; ferramenta, formato e diretorios ficam a cargo de cada instancia.

## O que este repositorio instancia

`AGENTS.md` deste repositorio segue o padrao ponto a ponto: `raw/sources/` imutavel, `wiki/` escrita pelo agente, `index.md` gerado, `log.md` com o prefixo do gist, `_review.md` como fila de revisao, `prompts/ingest.md`, `prompts/ask.md` e `prompts/lint.md` como as tres operacoes. A ferramenta usada foi o Claude Code.

## Uso no projeto

- §3 [58]: o paragrafo que declara o uso de IA (amparo: [[portaria-cnpq-2664-2026]]) cita este gist como origem do padrao *LLM Wiki* e o repositorio como sua instancia; desde 2026-09-15 o mesmo paragrafo declara tambem a skill [[helmsman-skill-yuukifst-2026]] para a especificacao do Finn.
- Fora do tema do *harness*; entra na lista por excecao autorizada pelo autor em 2026-09-14 (`AGENTS.md`, Project documents), pela mesma razao da Portaria: a declaracao de uso de IA precisa dizer qual metodo foi seguido.

## Contradictions

Nenhuma registrada.
