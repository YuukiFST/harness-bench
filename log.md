# Log

Append-only. One entry per operation. `grep "^## \[" log.md | tail -5` shows the last five.

## [2026-09-10] init | Omoikane instalado em harness-bench (template + Dominio PCC)

## [2026-09-10] ingest | 26 referencias do dist/projeto-pcc.docx (14 arXiv + Feevale em raw/sources, 23 wiki/sources, 8 conceitos, 7 entidades, 1 query)

## [2026-09-10] rule | Documentos do PCC seguem files/ (handouts vinculantes) e passam sempre pela skill no-ai-slop (AGENTS.md § Project documents)

## [2026-09-10] query | Harness e eficiencia do modelo: viabilidade do tema e o que agregam as fontes (Meta-Harness, Handbook, Alier, FrontierHarness site/repo, video Pi)

## [2026-09-10] query | Auditoria das referencias do PCC: 26/26 citacao-lista conferem, fatos batem, tema alinhado com 2 lacunas (Cursor, vagas)

## [2026-09-10] query | Checklist de prontidao dist/: 4 marcadores, cronograma, objetivos e slop bloqueiam; resto confere no XML

## [2026-09-10] fix | Data de entrega 10/09/2026 aplicada ao projeto-pcc.docx (cronograma AGOSTO-DEZEMBRO desde o inicio das aulas em 06/08, [A DEFINIR] resolvido; "mes 10"/09-10 foi engano do autor, revertido; restam [A VERIFICAR] + 2x[A MEDIR] das pilotos)

## [2026-09-10] fix | Cronograma refeito em 2 colunas (AGOSTO-SETEMBRO, pesquisa executada; §5 no passado; matriz completa externa pendente)

## [2026-09-10] fix | Proposta, nao relatorio: tabela de volta a 5 colunas SETEMBRO-JANEIRO com futuro, §5 restaurado, 3 marcadores virados em prosa futura

## [2026-09-10] note | Duas fases confirmadas: hoje só o documento do projeto; o prático da pesquisa para janeiro (matriz em DEZ–JAN, consistente com o cronograma)

## [2026-09-10] audit | Tarefa 1 nos dois dist/*.docx via word/document.xml: gate FALHA (projeto sem o dia da entrega — zero ocorrencias de "10 de setembro de 2026"/"10/09/2026"; frase atual so diz "setembro de 2026, mes de entrega"). Restante mecanico passa no XML. Sem commit, sem conversao (sem LibreOffice); checklist visual devolvido e operacao parada no gate.

## [2026-09-10] decision | Humano: manter so o mes (sem dia no .docx) e corrigir atividade p79 para tres secoes. Feito: cirurgia em word/document.xml da atividade com backup (so document.xml mudou, 18/18 demais partes identicas), prosa minima via no-ai-slop, re-extracao confere (106 paras, "seis secoes" 0, "tres secoes" 1, formato intacto, 17 refs). docs/research: 4x "10/09/2026" viraram "setembro de 2026"; entrada de log de 10/09 sobre a data fica como historico, superada por esta.

## [2026-09-11] query | auditoria-conteudo-referencias-pcc: 21 entradas lidas contra o corpo (12 CONCRETA, 6 DIVERGENTE, 1 FORA DO TEMA, 1 NÃO CITADA) + 6 citacoes orfas (ABNT x3, Gil, IFMT, Prodanov/Freitas removidas da lista entre HEAD e a versao de trabalho); `## Uso no PCC` atualizado em 21 wiki/sources; pendencias em _review.md

## [2026-09-11] ingest | Portaria CNPq 2.664/2026 (Politica de Integridade): raw/sources/portaria-cnpq-2664-2026.txt (texto oficial do CNPq); wiki/sources/portaria-cnpq-2664-2026.md; excecao de tema registrada em AGENTS.md (uma referencia sobre declaracao de IAG, so no paragrafo do *LLM Wiki*)

## [2026-09-11] fix | Auditoria de conteudo aplicada ao dist/projeto-pcc.docx: [26] [52] [53] [55] [57] [60] corrigidos (razoes calculadas marcadas, Lee trocado por TerminalBench-2 Tabela 7, Zhang com qualificadores, HarnessRank por taxa de aprovacao, Runta 67,8% = celula mediana do Claude Code, Prodanov/Freitas por natureza e abordagem, DeepSWE 668 vs 32,8 linhas); seis entradas recolocadas na lista; Liu 2023 e Bogdanov 2026 removidos; paragrafo do *LLM Wiki* inserido em §3 [58] com (Brasil, 2026); fechamento citacao-lista conferido nos dois sentidos (25 entradas, 25 citadas); `## Resolucao` na query da auditoria; pendencias YuukiFST (repositorio privado) e nome da ferramenta em _review.md

## [2026-09-14] redesign | Experimento passa a construir o Finn (github.com/YuukiFST/Finn, issues #1-#22) com OpenCode e pi, ticket a ticket, e comparar tokens: dist/projeto-pcc.docx reescrito via tools/pcc_edits_2026-09-14.py (titulo, §1-§5, 24 referencias: saem Datacurve/Pier, Huang/DeepSWE, Jimenez/SWE-bench; entram OpenCode repo 2026a, Finn 2026a; Zen 2026b, harness-bench 2026b); dist/apresentacao-pcc.html via tools/slides_edits_2026-09-14.py (15 slides, Camada 1 pi vs OpenCode 5,3x, matriz 2x9x2, Wilcoxon 9 pares MDE 0,76σ, notas); CONTEXT.md e docs/spec/11-experimental-protocol.md reescritos; retirados docs/spec/12, 14, docs/research/05, 07, wiki/entities harness-zero, oh-my-pi, cline, datacurve, OmpArm do layer1; wiki/entities/finn.md criado; concepts desenho-experimental, atribuicao, adequacao-oraculo e sources deepswe/pier/swe-bench/pi/zen atualizados; deck/ (Vite) espelhado via tools/deck_edits_2026-09-14.py e reconstruido em dist/apresentacao-pcc/

## [2026-09-14] note | Ferramenta do LLM Wiki: todas as operacoes registradas neste log ate 2026-09-14 (init, ingest, query, fix, audit, redesign) foram executadas com o Claude Code, como declara o §3 [58] do projeto-pcc.docx (Portaria CNPq 2.664/2026, Art. 9º, I, c); os prompts em prompts/ tambem sao carregaveis no OpenCode, mas nenhuma operacao foi feita nele

## [2026-09-14] fix | Fila _review.md zerada: Zhang/HAL/DeepSWE conferidos nos PDFs (secoes "Verificacao no PDF"; HAL corrigido, par "Sonnet 4.5 68->34" nao existe no v1; 69,7->77,0 reatribuido a Lin/AHE em binding-constraint-thesis); Gil 2022 e NBR 6023:2025, 10520:2023, 15287:2025 conferidos em catalogo/folha de rosto com paginas novas em wiki/sources; letras 2025a/2025b mantidas (NBR 6023 §9.1: numerais em ordem crescente); rotulos de [57] seguem Prodanov/Freitas; C1 sem posicao antes de H1; FrontierHarness com origem de cada numero (blog/repo/site); video "Learn Pi" e "vagas pedem" retirados da wiki; Camada 1 nao volta ao docx como estudo piloto; objetivos especificos ficam com 2-3 linhas; tools/build_pcc.py aposentado em tools/legacy/; queries 2026-09-10/11 e docs/research/estrutura marcadas como historico; layer1/tests 37 passed em venv local; docx sem alteracao

## [2026-09-14] ingest | LLM Wiki (Karpathy, 2026)

Gist de Karpathy, origem do padrao que este repositorio instancia. Criada `wiki/sources/llm-wiki-karpathy-2026.md`; atualizada `wiki/sources/portaria-cnpq-2664-2026.md` (link). PCC: [58] cita Karpathy (2026) e a lista ganha a entrada [177]; excecao registrada em `AGENTS.md`. Slides: painel de H1/H2 troca a Camada 1 (medicao propria) por FrontierHarness (Runta, 2026) e Earendil (2026), fontes externas; classificacao atribui o *LLM Wiki* a Karpathy (2026). Script: `tools/slides_edits_2026-09-14d.py`.

## [2026-09-14] redesign | Construcao integral a partir de uma especificacao unica

O autor pediu que a comparacao fosse por tokens gastos para construir o SaaS, nao por *ticket* concluido, com o pi recriando o produto a partir de uma especificacao gerada pelo OpenCode. Adotado com correcao: a especificacao e escrita pelo autor antes, a partir das *issues* do Finn, congelada, e os dois bracos a recebem identica e constroem do zero, unidade a unidade (9 unidades = os 9 *tickets* tecnicos), num unico espaco de trabalho; oraculo mantido (testes de aceitacao held-out por unidade); metrica primaria tokens por construcao ao lado da fracao aprovada, Wilcoxon pareado por unidade. Motivo da correcao: entrada desigual (OpenCode via *issues*, pi via documento destilado de sistema pronto) tornaria a diferenca inatribuivel ao *harness*. Atualizados: `CONTEXT.md`, `AGENTS.md`, `docs/spec/11-experimental-protocol.md` (`tools/protocol_edits_2026-09-14.py`), `dist/projeto-pcc.docx` (`tools/pcc_edits_2026-09-14c.py`, 20 paragrafos), os dois decks (`tools/slides_edits_2026-09-14e.py`), `wiki/concepts/desenho-experimental-harness-fixo.md`, `wiki/concepts/atribuicao-harness-vs-modelo.md`, `wiki/concepts/adequacao-oraculo.md`, `wiki/entities/finn.md`, `wiki/entities/opencode.md`, `wiki/entities/pi-coding-agent.md`.

## [2026-09-14] fix | Referencias fora do tema removidas do projeto

O autor decidiu que a lista de referencias so contem fontes sobre o *harness*. Removidas de `dist/projeto-pcc.docx` (via `tools/docx_prose.py apply`): ABNT NBR 10520, 6023 e 15287; IFMT (2022); Gil (2022); Prodanov e Freitas (2013). Paragrafo [47] perde "(IFMT, 2022) e as da ABNT (...)" e a chamada da nota de rodape; [57] perde "(Gil, 2022; Prodanov; Freitas, 2013)". Lista passa de 26 para 20 entradas; citacao e lista conferidas nos dois sentidos. Regra registrada em `AGENTS.md` (Project documents). Pendente: espelhar em `deck/src/content.ts` (REFS), slide 10 do deck e `dist/roteiro-apresentacao.html`; decisao do autor sobre Brasil (2026) e Karpathy (2026).

## [2026-09-14] fix | Auditoria de coerencia docx x deck x roteiro

Auditoria slide a slide (17) com `CONTEXT.md`, `docs/spec/11` e o dump do docx como fonte. Numeros proprios (layer1/data) e externos (Runta, Earendil, Lin, Lee, Zhang, Kapoor, Alier Forment) conferidos nas fontes: sem divergencia numerica. Decisoes do autor em `docs/research/decisoes-auditoria-2026-09-14.html`: folha de rosto [11] passa a "projeto de pesquisa ... disciplina de Metodologia Cientifica" (nao e PCC); barra oh-my-pi do slide 2 fica (linha do FrontierHarness, nao braco); slide 16 lista as mesmas 20 referencias do projeto (entram HarnessRank e Opencode Zen 2026b; slide 15 cita o gateway); `dist/apresentacao-pcc.html` (legado, 16 slides, ainda com Gil/Prodanov) removido, fica no git. Demais correcoes: [47] "suite de tarefas" vira "produto e especificacao"; 21 issues do Finn sao #2-#22 sob o mapa #1 (slide 5, nota 5, roteiro); finalidade do Claude Code alinhada ao [58] (slide 10, roteiro); nota 10 perde Gil/Prodanov; rodape do slide 10 cita YuukiFST 2026b; "cobertura antes de repeticoes" vira "reduzir cobertura antes de reduzir repeticoes" e a resposta da cota segue a escada do protocolo, nunca n < 3 (slide 14, roteiro); pares de Wilcoxon sao k = 9 (nota 13, roteiro); cartao inicial do slide 9 igual ao content.ts; comentarios HTML renumerados; roteiro corrige a lista de slides com autor na tela e a resposta sobre o proxy ([63]). Scripts: `tools/pcc_edits_2026-09-14d.py`, `tools/slides_edits_2026-09-14g.py`, `tools/roteiro_edits_2026-09-14b.py`; deck reconstruido, 20 referencias cabem no slide 16 sem estouro (Chrome 1920x1080). Nao conferido: numero da "Tabela 7" de Lee et al. (a wiki confirma 76,4/74,7 e Opus 4.6, nao a tabela).

## [2026-09-15] ingest | Helmsman (skill, YuukiFST, 2026)

- Criada: wiki/sources/helmsman-skill-yuukifst-2026.md (raw/sources/helmsman-skill-yuukifst-2026.md, copia de main em 2026-09-15).
- Atualizadas: wiki/entities/finn.md (mapa #1 mapeado com Helmsman; #11-#13 por subagentes; letra ABNT 2026b), wiki/sources/llm-wiki-karpathy-2026.md (§3 [58] declara os dois metodos).
- dist/projeto-de-pesquisa.docx §3 [58] reescrito; nova entrada YUUKIFST 2026a (agent-dotfiles); Finn 2026b, harness-bench 2026c.

## [2026-09-15] rule | Projeto de pesquisa, nunca "PCC"

- Renomeados: dist/projeto-pcc.docx -> dist/projeto-de-pesquisa.docx; dist/apresentacao-pcc/ -> dist/apresentacao/; docs/research/estrutura-do-projeto-e-revisao-do-pcc.md -> estrutura-do-projeto-e-revisao.md; tools/legacy/build_pcc.py -> build_projeto.py; wiki/queries/2026-09-10-auditoria-referencias-pcc -> 2026-09-10-auditoria-referencias; wiki/queries/2026-09-11-auditoria-conteudo-referencias-pcc -> 2026-09-11-auditoria-conteudo-referencias.
- "PCC" substituido por "projeto" em todas as paginas de wiki/ e docs/research/ (a citacao literal do titulo da norma IFMT 2022 permanece). Entradas anteriores deste log ficam como estavam.

## [2026-09-15] build | Deck explicativo (cópia visual da apresentação)

- Deck Vite em deck/ e seu build em dist/apresentacao/ seguem intactos (backup local do build, fora do repositório).
- Novo deck de arquivo único em dist/apresentacao-explainer/index.html, gerado por `python tools/apresentacao_explainer/build.py` (slides.py, content.py, charts.py, styles.css, engine.js, fontes OFL embutidas). Método: skill visual-explainer (nicobailon), modo slide deck: 34 slides em 100dvh, paleta e fontes próprias (Fraunces, IBM Plex Sans/Mono), tema claro/escuro, notas do apresentador (N), sumário (O), verificação de estouro por slide.
- Gráficos das fontes do projeto, com denominador: FrontierHarness 12 configurações (dispersão custo × aprovação), Camada 1 (bytes por requisição, layer1/data), Lin 2026 Tabela 1 e SWE-bench tokens, HAL Tabela A19 (haltere), Alier Forment 2026 (tokens por run), regras de medição (HarnessRank, Runta, Lee 2026). Nenhum número novo; todos vêm do .docx ou de wiki/sources.
- HarnessRank (2026): já estava em 6 REFERÊNCIAS [169] e citado em §2 [52]; site relido em 15 set. 2026, ainda sem linhas publicadas; entra no deck como precedente de método (slide 20) e na lista de referências.

## [2026-09-15] edit | Deck explicativo na ordem do projeto e novo subtítulo do projeto

- `tools/apresentacao_explainer/slides.py`: `all_slides()` reordenado para seguir as seções do docx (1 Introdução, 2 Referencial teórico, 3 Material e método, 4–6 Orçamento, cronograma e referências). Definição e componentes do *harness* passam para a seção 2 [49][50]; Camada 1 vai para a seção 3, depois das duas camadas [59]; classificação [57] e uso de IA [58] abrem a seção 3. Notas de fala que diziam "slide seguinte/anterior" corrigidas. Deck regenerado: 33 slides.
- Título do projeto: o subtítulo nomeava o método (OpenCode, pi, SaaS, "sob um mesmo modelo") em vez de delimitar o tema. Novo subtítulo espelha o parágrafo de tema [29]: "EFEITO SOBRE TOKENS E TAXA DE SUCESSO DE AGENTES DE CODIFICAÇÃO NA CONSTRUÇÃO DE UM MESMO PRODUTO COM O MODELO DE LINGUAGEM FIXO". Aplicado em [5] e [10] do docx (`tools/docx_edits_2026-09-15b.py`) e na abertura do roteiro (`tools/roteiro_edits_2026-09-15b.py`). Capas dos dois decks mostram só o título principal e não mudaram.
- Objetivo geral [33] e H1 [45] reescritos na mesma lógica (`tools/docx_edits_2026-09-15c.py`): primeiro a diferença atribuível ao *harness* com o modelo fixo e o mesmo produto, depois OpenCode, pi e Finn como braços e produto que a instanciam. Roteiro (cartões de objetivo geral e H1) e deck explicativo (notas do problema, subtítulo de objetivos, cartão H1) seguem a nova redação; `deck/` não citava essas frases.

## [2026-09-23] ingest | HarnessTax (Pan et al., 2026)

- Fonte: https://harnesstax.github.io/ (texto do JSON `data/blog/harness-x-model.0af74054a7.json`, HTML removido) salvo em `raw/sources/harnesstax-pan-2026.md`, coletado em 2026-09-23. Blogue de pesquisa, nao revisado por pares.
- Criada: wiki/sources/harnesstax-pan-2026.md.
- Atualizadas: wiki/entities/pi-coding-agent.md, wiki/concepts/binding-constraint-thesis.md, wiki/concepts/especificidade-modelo-inversao.md, wiki/concepts/medicao-custo-proxy-vs-relato.md, _review.md.

## [2026-09-23] ingest | SoL-Pi (Liu et al., 2026)

- Fonte: arXiv:2609.20519v1 (17 set. 2026), PDF em `raw/sources/2609.20519-liu-sol-pi.pdf`, lido com `pdftotext`. *Preprint*, nao revisado por pares.
- Criada: wiki/sources/sol-pi-liu-2026.md.
- Atualizadas: wiki/entities/pi-coding-agent.md, wiki/entities/opencode.md, wiki/concepts/binding-constraint-thesis.md, wiki/concepts/especificidade-modelo-inversao.md, wiki/concepts/medicao-custo-proxy-vs-relato.md, _review.md.

## [2026-09-23] edit | Projeto de pesquisa enxuto com HarnessTax e SoL-Pi

- `dist/projeto-de-pesquisa.docx` reescrito por `tools/docx_edits_2026-09-23.py` (reproduz o arquivo a partir de 89fccf9): 12 para 9 páginas no Word, 21 para 15 referências.
- Justificativa passa a se apoiar em [[harnesstax-pan-2026]]; a primeira pendência do referencial opõe carga fixa (Pan) e conversa ([[sol-pi-liu-2026]]), o que H2 decide.
- H1 reescrita para cobrir a taxa de sucesso e ser refutável: o *harness* muda mais o custo do que o sucesso.
- Limitações ganham a dependência entre unidades sob o teste de Wilcoxon e a troca de modelo no nível gratuito.
- *et al.* em itálico no texto, títulos em negrito em todas as referências, *et al.* nas referências com quatro ou mais autores.
- Deck e roteiro ainda não acompanham esta versão.

## [2026-09-23] edit | Deck explicativo e roteiro alinhados ao docx de 2026-09-23

- `dist/apresentacao-explainer/index.html` regenerado de `tools/apresentacao_explainer/` (issue #80): 33 para 27 slides, todo número com o parágrafo `[n]` do dump atual.
- Saíram os slides que só existiam por fontes removidas do docx (FrontierHarness, referencial 2022–2025 e 2026, HAL, Alier Forment, regras de medição) e os que dependiam de números fora do docx (componentes com bytes, Camada 1 medida).
- Entraram a justificativa com [[harnesstax-pan-2026]], a divergência sobre o sucesso (Lin, Zhang, Pan) e as duas pendências do referencial, com [[sol-pi-liu-2026]].
- `dist/roteiro-apresentacao.html` gerado por `tools/roteiro_2026-09-23.py`, derivado do roteiro de 2026-09-18.
- A seção 6 do docx tem 14 entradas, não 15 como diz a entrada anterior; deck e roteiro seguem o docx.
- `deck/` (Vite, 18 slides) aposentado pelo autor em 2026-09-23: não foi editado e não acompanha o docx.

## [2026-09-23] edit | Deck explicativo no palco fixo 1920×1080 e revisão contra o docx

- `tools/apresentacao_explainer/` passa ao palco fixo do frontend-slides (`viewport-base.css`, um slide ativo, escala única); saem o scroll e os `clamp()` dentro dos slides.
- Visual: cabeço corrido e fólio, índice nas divisórias, fluxo do Finn em linha, fita das nove unidades, orçamento como livro-razão da Tabela 1, cronograma com barras contínuas.
- Correções de conteúdo: o passo "gate" não era a U4 e não usa mais a cor do OpenCode; `spec.md` não existe no projeto; a classificação perdeu duas glosas que o [73] não dá; o subtítulo das referências não afirma mais que todas tratam do *harness*.
- Mesma ordem e mesmo total (27), então `dist/roteiro-apresentacao.html` continua alinhado.

## [2026-09-23] edit | Cronograma do deck: matriz e análise em outubro

- Pedido do autor: a execução da matriz de experimentos e a análise dos resultados passam para outubro de 2026 no slide Cronograma de `dist/apresentacao-explainer/index.html`.
- Dezembro e janeiro ficaram vazios, então o calendário do slide vai de agosto a novembro de 2026; o divisor da seção 4 acompanha.
- `dist/roteiro-apresentacao.html` regenerado com a mesma fala.
- A Tabela 2 de `dist/projeto-de-pesquisa.docx` ainda diz dez–jan para a matriz e jan para a análise: deck e docx divergem até o docx ser editado.

## [2026-09-23] edit | Tabela 2 do projeto: matriz e análise em outubro

- `dist/projeto-de-pesquisa.docx` editado por `tools/docx_edits_2026-09-23b.py`: execução da matriz e análise dos resultados passam para outubro; as colunas de dezembro e janeiro, vazias, saem, como no modelo do curso, que lista só meses com trabalho.
- A largura das duas colunas vai para os quatro meses; a tabela mantém a largura total. Word: 9 páginas, sumário inalterado.
- A tabela perdeu 22 parágrafos no dump, então a seção 6 passa de [181]–[194] para [159]–[172]; deck e roteiro citam os números novos.
- Deck e docx voltam a concordar sobre o cronograma.

## [2026-09-23] edit | Tabela 2 do projeto dentro da mancha de texto

- `tools/docx_edits_2026-09-23c.py`: a Tabela 2 tinha 10021 twips e passava das duas margens; agora usa os 9071 da mancha, como a Tabela 1.
- Nessa largura SETEMBRO e NOVEMBRO quebravam linha, então o recuo lateral das células desta tabela cai para 2,85 pt e a coluna de fases cede o que o rótulo mais longo não usa.
- Oito dos 17 X não tinham tamanho e saíam no corpo do texto; agora todos em 9 pt, como o resto da tabela.
- Word: 9 páginas, nenhuma célula quebra linha.

## [2026-09-24] ingest | Effective harnesses for long-running agents (Young, 2025)

- Criada: [[effective-harnesses-young-2025]] (texto em `raw/sources/effective-harnesses-young-2025.md`).
- Atualizadas: [[finn]], [[desenho-experimental-harness-fixo]], [[adequacao-oraculo]].
- Nenhuma contradicao registrada.

## [2026-09-24] edit | Finn de referencia substitui as nove unidades

- Pedido do autor: o Finn sera construido primeiro pelo proprio autor, ate ficar como ele quer, e depois reconstruido do zero pelos dois *harnesses*; as nove unidades tiradas das *issues* #14-#22 saem.
- Desenho: o fim de cada etapa da referencia vira *tag* git e uma unidade (ao menos seis, piso do Wilcoxon bilateral). Da referencia saem `spec.md` (produto, pilha, travas, contrato de interface) e `features.json` (formato de [[effective-harnesses-young-2025]], sem `passes`). Os testes de aceitacao precisam passar na referencia, na *tag* de cada unidade, antes do congelamento. Detalhe em `docs/spec/11-experimental-protocol.md` §1.1.
- A objecao de 2026-09-14 (entrada desigual quando o OpenCode gerava a especificacao para o pi) nao se aplica: a referencia e do autor e os dois bracos recebem o mesmo documento.
- `dist/projeto-de-pesquisa.docx`: o autor substituiu o arquivo pela versao atualizada dele (sem a entrada BRASIL, Tabela 2 de agosto a janeiro); `tools/docx_edits_2026-09-24.py` roda sobre essa versao: [53], [59], [74], [77], [78], [86], a linha [123] da Tabela 2 que vira "FINN DE REFERÊNCIA, PROXY E TESTES" e a entrada YOUNG depois de PAN. O autor liberou passar do limite de paginas por referencias; Word: 9 paginas, sumario inalterado.
- Pendencias do texto do autor, nao alteradas: [74] cita Brasil (2026) sem entrada na secao 6, e YuukiFST (2026b), o Finn, tem entrada sem citacao.
- `CONTEXT.md` ganha *reference build* e redefine especificacao e unidade; `AGENTS.md` (Domain) registra a mudanca.

## [2026-09-24] edit | Citacoes e lista fechadas no docx do autor

- `tools/docx_edits_2026-09-24b.py`: [74] deixa de citar Brasil (2026), que o autor tirou da lista por estar fora do tema; a declaracao de uso de IA fica, sem a norma. [77] volta a citar YuukiFST (2026b) e [76] volta a citar YuukiFST (2026c): o autor tinha tirado as citacoes e mantido as entradas, e entrada sem citacao quebra a regra da Aula 3.
- Correcoes de digitacao na revisao do autor: [43] (italico quebrado em *coding agent*, "muda influencia", "nesse *benchmark*" sem antecedente), [48] ("porem", "ao inves de", espaco antes de "?"), [69] ("pi" onde o resto diz "PI").
- 14 citacoes, 14 entradas. Word: 10 paginas; as referencias passam para a pagina seguinte, o que o autor liberou, e o sumario marca 6 REFERENCIAS na pagina 6.
- `AGENTS.md`: excecao da Portaria revogada; orcamento de paginas registra a pagina a mais de referencias.

## [2026-09-24] edit | Pi, nao PI

- Pedido do autor: o *harness* se escreve "Pi" na prosa, como no titulo da propria fonte (Earendil, 2026). `tools/docx_edits_2026-09-24c.py` troca a palavra isolada "PI"/"pi" por "Pi" em [43]-[76]; API, SoL-Pi e a URL de [181] ficam. Word: 10 paginas, sem mudanca de layout.
- `CONTEXT.md` e `AGENTS.md` seguem; `pi` fica so como comando da CLI.
- Wiki: "pi" vira "Pi" na prosa de 10 paginas; ficam codigo, wikilinks, URLs, caminhos, nomes hifenizados (oh-my-pi, pi-mono, SoL-Pi) e citacoes literais das fontes ("design philosophy behind pi", Alier Forment 2026). Entradas antigas deste log nao foram reescritas.
- Deck explicativo e roteiro realinhados ao docx final (versao do autor + 24, 24b): Pi, sem Portaria, 14 referencias com YOUNG, orcamento e cronograma de agosto a janeiro, indices [n] do dump atual.

## [2026-09-24] edit | Tabelas e termos do docx do autor

- `tools/docx_edits_2026-09-24d.py`, a pedido do autor: "Fonte: elaborado pelo autor (2026)." volta embaixo das Tabelas 1 e 2 ([99], [157]); a Tabela 2 perde dezembro e janeiro, vazios, e volta a caber na mancha (9071 twips, recuo 2,85 pt, X em 9 pt), como em 23b e 23c; [66], [67] e [75] passam a "*system prompt*", como o [62]; [96] perde o espaco final.
- Word: 9 paginas, 6 REFERENCIAS de volta na pagina 5 do sumario, nenhuma celula da Tabela 2 quebra linha.
- A secao 6 passa a [158]–[172]; deck e roteiro sao realinhados aos novos indices.

## [2026-09-24] edit | Medicao de tokens pelo gateway e cronograma ate outubro

- `tools/docx_edits_2026-09-24e.py`, a pedido do autor: [80] a contagem principal passa a ser o `usage` que o *gateway* devolve em cada resposta, lido no *proxy*, com o *cache* a parte; a recontagem por um tokenizador so separa a carga fixa de H2, medida em cada requisicao ([80], [83]) em vez de Camada 1 vezes passos. [83] Wilcoxon so sobre tokens e Succ/Mtok; resultado principal = razao entre as medianas de tokens por construcao; fracao de testes relatada sem teste. [61] e [75] acompanham.
- Tabela 2: "Finn de referencia, *proxy* e testes" so em outubro; a coluna NOVEMBRO sai.
- Word: 9 paginas, 6 REFERENCIAS na mesma posicao (p. 8, linha 33).
- `docs/spec/11-experimental-protocol.md` §2.1, §2.2 e §7 e [[medicao-custo-proxy-vs-relato]] atualizados; deck e roteiro realinhados.

## [2026-09-24] edit | Revisao do projeto, deck e roteiro contra fontes e apostilas

- Apostilas lidas (template, Aula 3, Aula 5). `tools/docx_edits_2026-09-24f.py`: titulo em negrito com *HARNESS* em italico ([9], [22], template); "Cuiaba – MT" ([18], [31], Aula 3: cidade e estado); citacoes diretas com pagina, Ning p. 7 e p. 66, Lin p. 1 ([65], [66], [69], Aula 5); problema sem "influenciar no" nem repeticao ([48]).
- Conferencia citacao por citacao nas fontes brutas: [67] ganha Earendil (2026) e Opencode (2026a) e perde "um *prompt* maior", sem fonte; [68] Zhang fala de variacao, em tarefas longas, e o 2,0x de Pan e media; [69] Pan diz que o imposto "pode comecar" na primeira requisicao, e Liu mudou quatro mecanismos, com a leitura delegada; [71] "*harness* que nao e o do fornecedor do modelo"; [73] "nao se encontrou"; [83] Miller recomenda o pareamento, sem dizer que a dificuldade e a maior fonte de variacao.
- Mapa citacao → trecho → prova: [[2026-09-24-mapa-citacoes-projeto]]. 14 citacoes, 14 entradas.
- Humanizer nos trechos novos. Word: 9 paginas, sumario inalterado (6 REFERENCIAS na p. 5).
- Deck (`tools/apresentacao_explainer/`) e roteiro (`tools/roteiro_2026-09-24.py`) realinhados: indices [101]–[146], [147]–[161], [159], [160]; "ao menos tres" construcoes; slide 15 sem "o agente especifica"; Q&A do roteiro sem o erro "outros dois bracos" e sem a frase de fecho; mesmas mudancas de texto do docx. Slides 9, 10, 11, 15, 21 e 26 conferidos por captura, sem transbordo.
- Pendencias em `_review.md`: regra de refutacao de H1, repositorios privados, deck antigo em `dist/apresentacao/`.

## [2026-09-24] edit | Pendencias da revisao resolvidas; Zen gratuito fechado para o Pi

- Decisao do autor: seguir a recomendacao. H1 [61] usa as medianas por celula da fracao final, como `docs/spec/11-experimental-protocol.md`; Word: 9 paginas, sumario inalterado. Deck e roteiro acompanham.
- `deck/` e `dist/apresentacao/` removidos; `AGENTS.md` e `tools/apresentacao_explainer/build.py` apontam para o deck vigente.
- Repositorios Finn e harness-bench seguem privados ate ficarem prontos.
- Achado novo: o Zen recusa `hy3-free` ("not supported") e restringe o nivel gratuito a clientes OpenCode ("free tier can only be used from within OpenCode"). O braco Pi fica sem modelo e [76], [79], [91] ficam falsos ate o autor escolher outro caminho. Registrado em `_review.md`.
