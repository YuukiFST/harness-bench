"""Wiki edits for the construction design (2026-09-14).

Concept and entity pages move from "ticket by ticket from author-written
reference states" to "one construction per arm from one frozen specification,
nine units". Exact-string replacements; each must match once. Appends the
redesign entry to log.md.

Usage:
    python tools/wiki_edits_2026-09-14.py
    python bin/wiki-index.py && python bin/wiki-lint.py
"""

import re
from pathlib import Path


def edit(f: str, pairs: list[tuple[str, str]]) -> None:
    p = Path(f)
    t = p.read_text(encoding="utf-8")
    for o, n in pairs:
        if t.count(o) != 1:
            raise SystemExit(f"{f}: expected 1 match, found {t.count(o)}:\n{o[:80]}")
        t = t.replace(o, n)
    t = re.sub(r"^updated: .*$", "updated: 2026-09-14", t, count=1, flags=re.M)
    p.write_text(t, encoding="utf-8")
    print(f, len(pairs))


edit("wiki/concepts/desenho-experimental-harness-fixo.md", [
    ("summary: Dois bracos constroem o mesmo SaaS ticket a ticket; n>=3, Wilcoxon sobre tokens e Succ-Mtok",
     "summary: Dois bracos constroem o mesmo SaaS do zero, da mesma especificacao; tokens por construcao, pareado por unidade"),
    ("tags: [metodo, pareado, wilcoxon, celula, ticket, run, finn]",
     "tags: [metodo, pareado, wilcoxon, celula, unidade, construcao, finn]"),
    ("Vocabulario (autoridade: `CONTEXT.md`): braco, nivel, *ticket*, estado de referencia, run, celula (braco, *ticket*, nivel) com n runs, passo (round-trip no proxy), carga fixa, run nao concluida / descartada / adulterada, oraculo, teste de aceitacao (held-out).",
     "Vocabulario (autoridade: `CONTEXT.md`): braco, nivel, especificacao, unidade, espaco de trabalho inicial, construcao (a run), celula (braco, nivel) com n construcoes, passo (round-trip no proxy), carga fixa, unidade nao concluida / adulterada, construcao descartada, oraculo, teste de aceitacao (held-out)."),
    ("Desenho vigente desde 2026-09-14: os dois bracos, [[opencode]] e [[pi-coding-agent]], constroem o mesmo produto, o [[finn]], sobre o mesmo modelo. O desenho anterior (harness zero como controle, par pi / oh-my-pi, 8 tarefas do DeepSWE) foi retirado; ver `log.md` 2026-09-14.",
     "Desenho vigente desde 2026-09-14: os dois bracos, [[opencode]] e [[pi-coding-agent]], constroem o mesmo produto, o [[finn]], do zero, a partir da mesma especificacao congelada, sobre o mesmo modelo; compara-se o total de tokens por construcao. Desenhos anteriores retirados no mesmo dia: harness zero como controle, par pi / oh-my-pi e 8 tarefas do DeepSWE (manha); *tickets* isolados partindo de estados de referencia escritos pelo autor (tarde). A proposta do autor de deixar o OpenCode construir e gerar a especificacao para o pi foi descartada por entrada desigual (o pi receberia um documento destilado de um sistema pronto); ver `log.md` 2026-09-14."),
    ("## Suite\n", "## Especificacao e construcao\n"),
    ("- 9 *tickets* tecnicos do Finn (#15 tenant, #16 governanca, #17 flags, #14 pipeline de voz, #20 confirmacao, #21 log, #19 relatorio, #18 agendador, #22 cobranca), cada um um prompt identico para os dois bracos com a decisao, os locks e a pilha fixada pelo dono.\n- Cada *ticket* parte de um estado de referencia escrito pelo autor apos o *ticket* anterior, congelado por SHA-256; o que o agente produziu nao entra no seguinte. Toda celula e independente e os dois bracos partem dos mesmos bytes.\n- Escore: fracao dos testes de aceitacao do autor, escritos antes da execucao e held-out (nunca a suite do agente; ver [[adequacao-oraculo]]). *Ticket* concluido = todos passam.",
     "- Especificacao unica, escrita pelo autor a partir das *issues* fechadas do Finn antes de qualquer execucao e congelada por SHA-256: produto, pilha, restricoes gerais e 9 unidades em ordem de dependencia (#15 tenant, #16 governanca, #17 flags, #14 pipeline de voz, #20 confirmacao, #21 log, #19 relatorio, #18 agendador, #22 cobranca). Os testes de aceitacao nao estao nela.\n- Construcao: espaco de trabalho inicial so com a especificacao e a pilha; o executor invoca o *harness* uma vez por unidade, em ordem, com prompt identico para os dois bracos; o que o agente construiu numa unidade e o ponto de partida da seguinte (conversa nao carrega, codigo sim). O autor nao escreve codigo depois do inicio. Entrada identica para os dois bracos e o que torna a diferenca de tokens atribuivel ao *harness*.\n- Escore: fracao dos testes de aceitacao do autor, escritos antes da execucao e held-out (nunca a suite do agente; ver [[adequacao-oraculo]]), rodados sobre uma copia do espaco ao fim de cada unidade. Unidade concluida = todos os seus testes passam; construcao concluida = todos de todas as unidades passam ao fim."),
    ("- Cada celula n>=3 apos descartes (reamostragem; source: [[adding-error-bars-miller-2024]]); cobertura antes de repeticoes se a cota apertar.",
     "- Celula = (braco, nivel), n>=3 construcoes apos descartes (reamostragem; source: [[adding-error-bars-miller-2024]]); cobertura antes de repeticoes se a cota apertar (truncar apos a unidade 6 so no nivel de robustez; nunca pular unidades do meio)."),
    ("- Comparacao pareada por *ticket*: Wilcoxon bilateral α=0,05 sobre tokens por *ticket* concluido (metrica primaria) e sobre [[succ-mtok]] (nao-parametrico p/ 9 pares; dificuldade do *ticket* e o maior confundidor). MDE ~0,76σ com n=3 e 9 *tickets* (2,80·σ·sqrt(2/27)). Predicoes pre-registradas por nivel; nulo de H2 e reportavel.",
     "- Metrica primaria: tokens por construcao, sempre ao lado da fracao final de testes aprovados (braco que falha barato nao pode parecer o mais barato). Comparacao inferencial pareada por unidade: Wilcoxon bilateral α=0,05 sobre tokens por unidade e sobre [[succ-mtok]] por unidade (nao-parametrico p/ 9 pares; dificuldade da unidade e o maior confundidor). Unidades nao sao independentes (a seguinte parte do que o mesmo braco construiu); a dependencia de trajetoria e custo do *harness*, reportada por unidade. MDE ~0,76σ com n=3 e 9 unidades (2,80·σ·sqrt(2/27)). Predicoes pre-registradas por nivel; nulo de H2 e reportavel."),
    ("- H2: tokens de cada run decompostos em carga fixa (Camada 1 x passos) e conversa; parcela reportada por *ticket*. Ver [[atribuicao-harness-vs-modelo]].",
     "- H2: tokens de cada unidade decompostos em carga fixa (Camada 1 x passos) e conversa; parcela reportada por unidade e por construcao. Ver [[atribuicao-harness-vs-modelo]]."),
    ("- Limite unico: relogio de parede 3x a maior mediana dos dois bracos nos *tickets*-piloto;",
     "- Limite unico: relogio de parede por unidade, 3x a maior mediana dos dois bracos nas unidades-piloto;"),
    ("## Classes de run\n\nNao concluida = resultado (entra com a fracao aprovada; estouro do relogio conta como resultado). Descartada = medicao inconfiavel (sem reparo/repeticao, registrada).",
     "## Classes\n\nPor unidade. Nao concluida = resultado (entra com a fracao aprovada e a construcao segue; estouro do relogio conta como resultado). Descartada = medicao inconfiavel numa unidade descarta a construcao (sem reparo/repeticao, registrada)."),
])
edit("wiki/concepts/atribuicao-harness-vs-modelo.md", [
    ("construindo o mesmo produto ([[finn]]) *ticket* a *ticket*.",
     "construindo o mesmo produto ([[finn]]) do zero, a partir da mesma especificacao, unidade a unidade."),
])
edit("wiki/concepts/adequacao-oraculo.md", [
    ("testes de aceitacao Vitest escritos pelo autor por *ticket* do [[finn]], antes da execucao, mantidos fora do espaco de trabalho (held-out);",
     "testes de aceitacao Vitest escritos pelo autor por unidade da especificacao do [[finn]], antes da execucao, mantidos fora do espaco de trabalho (held-out) e rodados sobre uma copia dele ao fim de cada unidade;"),
])
edit("wiki/entities/finn.md", [
    ("summary: SaaS de financeiro por voz do autor; suite do experimento, 9 tickets tecnicos construidos por OpenCode e pi",
     "summary: SaaS de financeiro por voz do autor; produto do experimento, construido do zero por OpenCode e pi da mesma especificacao"),
    ("tags: [finn, suite, saas, tickets, bracos]", "tags: [finn, especificacao, saas, unidades, bracos]"),
    ("Suite do experimento: os 9 *tickets* tecnicos (#14-#22) viram tarefas, cada uma um prompt identico para [[opencode]] e [[pi-coding-agent]] a partir de um estado de referencia escrito pelo autor. Testes de aceitacao do autor por *ticket*, held-out, decidem o escore.",
     "Produto do experimento: os 9 *tickets* tecnicos (#14-#22) viram as 9 unidades de uma especificacao unica, escrita pelo autor e congelada; [[opencode]] e [[pi-coding-agent]] recebem os mesmos bytes e constroem o Finn do zero, unidade a unidade, num unico espaco de trabalho. Testes de aceitacao do autor por unidade, held-out, decidem o escore."),
])
edit("wiki/entities/opencode.md", [
    ("constroi o [[finn]] *ticket* a *ticket* via `opencode run --pure --format json`",
     "constroi o [[finn]] do zero, da mesma especificacao, unidade a unidade, via `opencode run --pure --format json`"),
])
edit("wiki/entities/pi-coding-agent.md", [
    ("constroi o [[finn]] *ticket* a *ticket* via `pi --mode json`",
     "constroi o [[finn]] do zero, da mesma especificacao, unidade a unidade, via `pi --mode json`"),
])

LOG_ENTRY = (
    "\n## [2026-09-14] redesign | Construcao integral a partir de uma especificacao unica\n\n"
    "O autor pediu que a comparacao fosse por tokens gastos para construir o SaaS, nao por *ticket* concluido, com o pi recriando o produto a partir de uma "
    "especificacao gerada pelo OpenCode. Adotado com correcao: a especificacao e escrita pelo autor antes, a partir das *issues* do Finn, congelada, e os "
    "dois bracos a recebem identica e constroem do zero, unidade a unidade (9 unidades = os 9 *tickets* tecnicos), num unico espaco de trabalho; oraculo "
    "mantido (testes de aceitacao held-out por unidade); metrica primaria tokens por construcao ao lado da fracao aprovada, Wilcoxon pareado por unidade. "
    "Motivo da correcao: entrada desigual (OpenCode via *issues*, pi via documento destilado de sistema pronto) tornaria a diferenca inatribuivel ao *harness*. "
    "Atualizados: `CONTEXT.md`, `AGENTS.md`, `docs/spec/11-experimental-protocol.md` (`tools/protocol_edits_2026-09-14.py`), `dist/projeto-pcc.docx` "
    "(`tools/pcc_edits_2026-09-14c.py`, 20 paragrafos), os dois decks (`tools/slides_edits_2026-09-14e.py`), `wiki/concepts/desenho-experimental-harness-fixo.md`, "
    "`wiki/concepts/atribuicao-harness-vs-modelo.md`, `wiki/concepts/adequacao-oraculo.md`, `wiki/entities/finn.md`, `wiki/entities/opencode.md`, `wiki/entities/pi-coding-agent.md`.\n"
)
log = Path("log.md")
text = log.read_text(encoding="utf-8")
if "Construcao integral a partir de uma especificacao unica" not in text:
    log.write_text(text + LOG_ENTRY, encoding="utf-8")
    print("log.md appended")
