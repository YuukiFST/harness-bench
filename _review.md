# Review queue

The agent writes here what it cannot decide alone. Resolve an item by editing the page it points to and deleting the bullet.

## [2026-09-10] ingest | referencias do dist

- `wiki/sources/stop-comparing-harness-zhang-2026.md`: valores por harness (69,7%->77,0%, 9,5 pp, gaps 34/34/48 pp) sem n runs/data no texto extraido — herdado de `docs/research/03` como NAO VERIFICADO; fechar lendo o PDF em `raw/sources/2605.23950-zhang-stop-comparing.pdf`.
- `wiki/sources/holistic-agent-leaderboard-kapoor-2025.md`: gaps 34/34/48 pp e correlacoes sem n detalhado na extracao; confirmar no PDF em `raw/sources/2510.11977-kapoor-holistic-agent-leaderboard.pdf` (caveat single-run do proprio artigo).
- `wiki/concepts/atribuicao-harness-vs-modelo.md` (C1): DeepSWE "modelo dirige" (via Merrill 2026) vs Zhang/HAL "harness domina" — registrada como tensao com leitura, sem vencedor. Confirmar com orientador qual posicao o PCC adota apos H1.
- `wiki/sources/metodologia-prodanov-freitas-2013.md`: `dated: unknown` (so o ano 2013 e conhecido); ordem impressa Lakatos/Marconi em obra homonima (*Metodologia do trabalho cientifico*, 9. ed.) diverge entre editor e varejo — conferir na capa fisica antes de citar.
- `docs/research/estrutura-do-projeto-e-revisao-do-pcc.md` Secao 3.7: `tools/build_pcc.py` parado em cc15d7b; rodar sobrescreve `dist/projeto-pcc.docx` (fonte da verdade). Reconciliar ou aposentar o gerador.
- Proposta, nao relatorio: futuro no texto e correto. Marcadores zerados (3 viraram prosa futura, `[A DEFINIR]` virou data); cronograma em 5 colunas SETEMBRO-JANEIRO. Nada mais trava a entrega por aqui.

## [2026-09-10] query | harness-tema-viabilidade-fontes

- Tabela "median cost per successful task" do site frontierharness.org ($0,06-$0,29) vs blog e repo ($1,05-$18,34 por pass): reconciliar contra `results/eval-data.json` antes de citar; ate la, citar blog + repo.
- Video "Learn Pi in 22 Min" (Sean's AI Stories): conteudo e data nao verificados (sem transcricao acessivel); uso restrito a ilustracao, sem numeros citados.
- Alegacao "vagas pedem Claude Code/Codex/Cursor": sem fonte na wiki; manter como motivacao ou levantar mini-survey de anuncios.

## [2026-09-11] edit | projeto-pcc.docx futuro e destinatario empresarial

- "Resultados preliminares do instrumento (Camada 1)" e a Tabela 1 (11,4x, 64.945 vs 5.676 bytes, 28 ago. 2026) sairam do `dist/projeto-pcc.docx` a pedido do autor: projeto de pesquisa descreve o que sera feito. Confirmar com a orientadora se um piloto ja medido pode voltar como "estudo piloto"; os dados seguem em `layer1/data/` e `docs/spec/41-layer1-request-shape.md`.
- Nova referencia Bogdanov (2026), JetBrains Developer Ecosystem Survey 2026 (>15.000 devs, maio-jul. 2026: Claude Code 39%, Codex 16%, Cursor 12% no trabalho), citada na justificativa. Fonte ainda nao ingerida na wiki (`raw/inbox/`); a alegacao "vagas pedem Claude Code/Codex/Cursor" continua sem fonte e ficou fora do texto.
- Objetivos especificos seguem com 2-3 linhas cada (revisao Secao 3.2); nao tocados nesta edicao.

## [2026-09-11] query | auditoria-conteudo-referencias-pcc

- Bogdanov (2026) [26]: FORA DO TEMA. Post da JetBrains trata so de adocao (39% "around", 16%/12% na janela maio-jul. 2026); nada sobre *harness* ou custo. Regra de `AGENTS.md` exclui adocao de mercado. Manter ou remover?
- Liu et al. (2023) [165]: NÃO CITADA. Entrada sem citacao no corpo apos a remocao da Tabela da Camada 1; obra fora do tema. Retirar da lista?
- HarnessRank [52]: DIVERGENTE. Site ordena por taxa de aprovacao; custo e tokens "don't affect ranking"; sem linhas publicadas. Corrigir "ordena por custo".
- Runta [55]: DIVERGENTE. 67,8% e a mediana por celula do proprio Claude Code, nao mediana entre *harnesses*. [26]/[52]: 17x e 5,3x sao razoes calculadas pelo autor (post diz 5,6x vs DSH Creator); faixa 50,0-66,7% e sobre 12 configuracoes.
- Lee et al. (2026) [53]: DIVERGENTE. 7,7 pontos / 4x menos tokens e em classificacao de texto *online* (vs ACE), nao em agente de codificacao.
- Zhang et al. (2026) [52]: DIVERGENTE. Tese formal condicionada a "comparable frontier models", "often comparable to or larger than", "may dominate"; projeto afirma sem qualificador.
- YuukiFST (2026) [59]/[173]: DIVERGENTE. Repositorio privado (gh: `"visibility":"PRIVATE"`, README 404); entrada declara "Acesso em: 28 ago. 2026". Tornar publico ou retirar.
- Citacoes orfas (entradas removidas entre HEAD e a versao de trabalho, ainda citadas em [47] e [57]): ABNT NBR 6023, NBR 10520, NBR 15287, GIL 2022, IFMT 2022, PRODANOV; FREITAS 2013. Recolocar (texto em `git show HEAD:dist/projeto-pcc.docx` [183]-[185], [188], [191], [201]).
- ABNT (3 normas) e Gil (2022): NÃO VERIFICADA, sem copia local em `raw/` ou `files/`. Prodanov/Freitas lido: "finalidade" e "quali-quantitativa" nao sao rotulos do livro (usa "natureza"; quanti e quali como alternativas).
- Ressalvas que nao derrubam: Lin 24,7 pp e calculo da Tabela 1 (71,9 - 47,2); DeepSWE "ordem de grandeza ante SWE-bench" e inferencia (668 vs 32,8 linhas); Earendil omite "in some cases"; Apache-2.0 do DeepSWE so no repositorio, nao no artigo.

## [2026-09-11] fix | resolucao-auditoria-conteudo-pcc

- YuukiFST (2026) [59]/[177]: entrada mantida; o repositorio segue privado. **Tornar publico antes da entrega** ou trocar a entrada por "em elaboracao". Visibilidade nao alterada pelo agente.
- §3 [58] nomeia "Claude Code" como ferramenta do *LLM Wiki* (Portaria CNPq 2.664/2026, Art. 9º, I, c pede ferramenta e finalidade). `log.md` registra as operacoes mas nao o nome da ferramenta em cada sessao; confirmar o nome (ou acrescentar OpenCode) antes da entrega.
- [57] usa os eixos do livro de Prodanov e Freitas ("natureza"; quantitativo e qualitativo). O handout `files/Estrutura do projeto de pesquisa-aula3.pdf` usa "finalidade" e "quali-quantitativa". Se a orientadora exigir os rotulos do handout, voltar a eles e citar Gil (2022) como fonte dos rotulos, apos ler o livro.
- Bogdanov (2026) removido da lista e de [26] por estar fora do tema. Para manter, acrescentar linha de excecao em `AGENTS.md` e ingerir o post.
- Gil (2022) e as tres normas ABNT continuam NÃO VERIFICADAS (sem copia local); entradas recolocadas com o texto de `HEAD`.
- ABNT 2025a/2025b: letras seguem HEAD; por titulo (NBR 6023 'projeto de pesquisa' antes de 'referencias'?) a NBR 15287 seria 2025a. Conferir com a NBR 6023:2025 antes de trocar, pois [47] e a nota de rodape citam as letras.
