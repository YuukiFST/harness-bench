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
