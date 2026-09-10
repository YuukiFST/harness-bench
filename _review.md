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
