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
