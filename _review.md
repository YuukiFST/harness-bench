# Review queue

The agent writes here what it cannot decide alone. Resolve an item by editing the page it points to and deleting the bullet.

## [2026-09-23] ingest | HarnessTax (Pan et al., 2026) e SoL-Pi (Liu et al., 2026)

- Efeito do *harness* no acerto: [[harnesstax-pan-2026]] (+-2% SWE-bench Lite, ~+-5% Terminal-Bench 2.0, 7 modelos x Claude Code/Codex/Pi, 3 execucoes) vs [[stop-comparing-harness-zhang-2026]] (HV/MV 7,80x), [[agentic-harness-engineering-lin-2026]] (OpenCode 47,2% vs Codex 71,9%, Terminal-Bench 2, GPT-5.4), [[holistic-agent-leaderboard-kapoor-2025]] (30-48 pp) e [[sol-pi-liu-2026]] (EdgeBench, GPT-5.6 Sol: Codex 34,7 vs Pi 44,8). Decidir como o projeto enuncia H1 diante das duas leituras. Ver `wiki/concepts/binding-constraint-thesis.md`, Contradictions.
- Custo do Claude Code: interacao com modelo nao nativo ([[frontierharness-runta-2026]], Kimi K3) vs caro tambem com modelos Anthropic ([[harnesstax-pan-2026]], Fable 5 $1,33 vs $0,67 no Pi; [[sol-pi-liu-2026]], Opus 5 $2.535 vs $1.741). Ver `wiki/concepts/especificidade-modelo-inversao.md`, Contradictions.
- Portabilidade do *harness* entre modelos: [[agentic-harness-engineering-lin-2026]] ("often underperforms on another") vs [[sol-pi-liu-2026]] ("strong cross-model generalization", 1 modelo de transferencia, sem IC). Ver `wiki/concepts/especificidade-modelo-inversao.md`, Contradictions.
- Regra de custo: [[harnessrank-2026]] (custo reportado, tokens sem *cache*) vs [[harnesstax-pan-2026]] e [[sol-pi-liu-2026]] (custo estimado por tabela de precos; SoL-Pi inclui leitura de *cache*). Decidir qual regra o *proxy* do projeto reporta como primaria. Ver `wiki/concepts/medicao-custo-proxy-vs-relato.md`, Contradictions.
- Contradicao interna de [[sol-pi-liu-2026]]: resumo diz "comparable to Pi", corpo mostra 93,7% e 94,3% do *score* do Pi no EdgeBench e 15 vs 18 tarefas no Terminal-Bench 4, sem IC. A economia por hora ($8,75-$13,50; $4,36-$5,71) so aparece no resumo, sem derivacao. Ver `wiki/sources/sol-pi-liu-2026.md`, Contradictions.
