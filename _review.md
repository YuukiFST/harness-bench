# Review queue

The agent writes here what it cannot decide alone. Resolve an item by editing the page it points to and deleting the bullet.

## [2026-09-25] query | Verificacao de uso real das referencias (resolvido)

Todas as 14 entradas sao usadas e sustentadas na obra; evidencia e correcoes em [[2026-09-25-verificacao-referencias-projeto]].

- [68] "sobre o GPT-5.4" saiu do docx, do deck e do roteiro: Lin *et al.* (2026) nao declara o modelo dos *harnesses* humanos da Tabela 1.
- Finn: repositorio privado por decisao do autor (AGENTS.md, 2026-09-25); nao e pendencia.
- Deck e roteiro realinhados ao docx de 9c0fe11 e as correcoes de 2026-09-25 (`tools/roteiro_2026-09-25.py`).

## [2026-09-23] ingest | HarnessTax (Pan et al., 2026) e SoL-Pi (Liu et al., 2026)

- Efeito do *harness* no acerto: [[harnesstax-pan-2026]] (+-2% SWE-bench Lite, ~+-5% Terminal-Bench 2.0, 7 modelos x Claude Code/Codex/Pi, 3 execucoes) vs [[stop-comparing-harness-zhang-2026]] (HV/MV 7,80x), [[agentic-harness-engineering-lin-2026]] (OpenCode 47,2% vs Codex 71,9%, Terminal-Bench 2, modelo nao declarado na Tabela 1), [[holistic-agent-leaderboard-kapoor-2025]] (30-48 pp) e [[sol-pi-liu-2026]] (EdgeBench, GPT-5.6 Sol: Codex 34,7 vs Pi 44,8). Decidir como o projeto enuncia H1 diante das duas leituras. Ver `wiki/concepts/binding-constraint-thesis.md`, Contradictions.
- Custo do Claude Code: interacao com modelo nao nativo ([[frontierharness-runta-2026]], Kimi K3) vs caro tambem com modelos Anthropic ([[harnesstax-pan-2026]], Fable 5 $1,33 vs $0,67 no Pi; [[sol-pi-liu-2026]], Opus 5 $2.535 vs $1.741). Ver `wiki/concepts/especificidade-modelo-inversao.md`, Contradictions.
- Portabilidade do *harness* entre modelos: [[agentic-harness-engineering-lin-2026]] ("often underperforms on another") vs [[sol-pi-liu-2026]] ("strong cross-model generalization", 1 modelo de transferencia, sem IC). Ver `wiki/concepts/especificidade-modelo-inversao.md`, Contradictions.
- Regra de custo: [[harnessrank-2026]] (custo reportado, tokens sem *cache*) vs [[harnesstax-pan-2026]] e [[sol-pi-liu-2026]] (custo estimado por tabela de precos; SoL-Pi inclui leitura de *cache*). Decidir qual regra o *proxy* do projeto reporta como primaria. Ver `wiki/concepts/medicao-custo-proxy-vs-relato.md`, Contradictions.
- Contradicao interna de [[sol-pi-liu-2026]]: resumo diz "comparable to Pi", corpo mostra 93,7% e 94,3% do *score* do Pi no EdgeBench e 15 vs 18 tarefas no Terminal-Bench 4, sem IC. A economia por hora ($8,75-$13,50; $4,36-$5,71) so aparece no resumo, sem derivacao. Ver `wiki/sources/sol-pi-liu-2026.md`, Contradictions.

## [2026-09-24] probe | Zen gratuito recusa chamada anonima; hy3-free fora da lista

- Teste em 2026-09-24 com `curl` anonimo (sem chave, sem cabecalho de cliente) contra `https://opencode.ai/zen/v1/chat/completions`: `mimo-v2.5-free` responde `FreeTierError` "OpenCode's free tier can only be used from within OpenCode"; `hy3-free` responde `ModelError` "not supported" e nao aparece em `/zen/v1/models`.
- Correcao do autor: o Pi usa os modelos gratuitos do Zen normalmente. O provedor embutido `opencode` do Pi envia `x-opencode-client: pi` e `x-opencode-session` (`docs/research/10-pi-measurement-surface.md:726`), e o Zen aceita. A conclusao anterior desta entrada ("o Pi nao pode usar o nivel gratuito") estava errada.
- O que ainda precisa de verificacao, sem decidir por interpretacao: (1) o braco Pi passa por um provedor proprio apontado para o *proxy*, que `docs/research/10-pi-measurement-surface.md:730` manda nao chamar de `opencode`; se o Zen passou a exigir o cabecalho de cliente, o *proxy* precisa repassar o que o Pi envia, e a regra de :730 se inverte. Testar com o Pi real atras do *proxy*. (2) `hy3-free`: conferir no `/model` do Pi se ainda existe com outro id; se saiu, escolher outro modelo de robustez (`docs/research/11-second-free-model.md` nomeia `nemotron-3-ultra-free` como reserva).

## [2026-09-24] edit | Revisao do projeto contra fontes e apostilas (resolvido)

- H1 [61]: a regra de sucesso passa a ser a da spec (medianas por celula da fracao final de testes aprovados), em `tools/docx_edits_2026-09-24f.py`.
- Repositorios Finn e harness-bench: privados por decisao do autor ate ficarem prontos; as entradas ficam.
- [76]: citacoes mantidas como identificacao dos bracos, sem novas entradas (tema e orcamento de paginas); os fatos estao nas documentacoes, ver [[2026-09-24-mapa-citacoes-projeto]].
- Deck antigo `deck/` e `dist/apresentacao/` removidos (ficam no historico git); `AGENTS.md` aponta para `tools/apresentacao_explainer/`.
- Slide 26 fica com as 14 referencias num slide: nao transborda.
