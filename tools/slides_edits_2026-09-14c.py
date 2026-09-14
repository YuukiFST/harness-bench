"""Third pass on the deck (2026-09-14): introduce Finn before it is named.

The author noted that slide 4 names Finn in the general objective before the
audience has seen what Finn is. Slide 4 now uses the .docx wording ("o mesmo
SaaS", [33]); a new slide "Finn: o produto" follows it with the product in one
picture (the 7-step voice pipeline, issue #14) and the 9 tickets that become
the suite. Facts from wiki/entities/finn.md (issues #1-#22).

Same mechanics as tools/slides_edits_2026-09-14b.py.

Usage:
    python tools/slides_edits_2026-09-14c.py
    cd deck && npx prettier --write index.html src && npm run build
"""

from pathlib import Path

_src = Path("tools/deck_edits_2026-09-14.py").read_text(encoding="utf-8")
_ns: dict = {}
exec(compile(_src.split("# --- index.html")[0], "deck_edits_helpers", "exec"), _ns)
apply = _ns["apply"]

OLD_OBJ = "medir a diferença de tokens e de sucesso entre OpenCode e pi construindo o Finn, <em>ticket</em> a <em>ticket</em>;"
NEW_OBJ = "medir a diferença de tokens e de sucesso entre OpenCode e pi construindo o mesmo SaaS, <em>ticket</em> a <em>ticket</em>;"

STEPS = ["áudio", "texto", "intenção", "gate", "executar", "resposta"]
STEP_SUB = ["WhatsApp ou app", "Whisper local", "palavras-chave", "papel × ação", "ou negar", "push"]
TICKETS = ["T1 tenant", "T2 governança", "T3 flags", "T4 pipeline de voz", "T5 confirmação", "T6 log", "T7 relatório", "T8 agendador", "T9 cobrança"]


def pipeline_svg() -> str:
    w, h = 1000, 170
    n = len(STEPS)
    bw, bh = 140, 84
    gap = (w - n * bw) / (n - 1)
    out = [f'<svg viewBox="0 0 {w} {h}" style="width:100%;height:{h}px" aria-label="pipeline de voz do Finn em seis passos">']
    out.append('<defs><marker id="finarr" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10z" fill="#f5b638"/></marker></defs>')
    y = 20
    for i, (s, sub) in enumerate(zip(STEPS, STEP_SUB)):
        x = i * (bw + gap)
        hi = i == 3
        out.append(f'<rect x="{x:.0f}" y="{y}" width="{bw}" height="{bh}" rx="14" fill="#121923" stroke="{"#f5b638" if hi else "#3b7bd6"}" stroke-width="3"/>')
        out.append(f'<text x="{x + bw / 2:.0f}" y="{y + 38}" text-anchor="middle" fill="#fff" font-size="26" font-weight="700">{i + 1}</text>')
        out.append(f'<text x="{x + bw / 2:.0f}" y="{y + 68}" text-anchor="middle" fill="#e8edf2" font-size="22">{s}</text>')
        out.append(f'<text x="{x + bw / 2:.0f}" y="{y + bh + 34}" text-anchor="middle" fill="#8b98a8" font-size="17">{sub}</text>')
        if i < n - 1:
            out.append(f'<line x1="{x + bw + 6:.0f}" y1="{y + bh / 2}" x2="{x + bw + gap - 8:.0f}" y2="{y + bh / 2}" stroke="#f5b638" stroke-width="3" marker-end="url(#finarr)"/>')
    out.append("</svg>")
    return "".join(out)


CHIPS = "".join(
    f'<span style="display:inline-block;padding:6px 20px;margin:0 10px 8px 0;border:2px solid {"#f5b638" if t.startswith("T4") else "#3b7bd6"};border-radius:999px;font-size:23px">{t}</span>'
    for t in TICKETS
)

FINN_SLIDE = f"""<!-- 5 FINN -->
<section class="slide" id="s-finn" data-title="Finn: o produto">
  <h2>Finn: o produto que os dois <em>harnesses</em> vão construir<small>um SaaS de verdade, não um <em>benchmark</em> de tarefas soltas</small></h2>
  <div class="row" style="flex:none;gap:40px">
    <div class="col" style="flex:0 0 600px;display:flex;flex-direction:column;gap:20px;font-size:25px">
      <div class="card frag" style="padding:24px 30px"><b class="acc">O que é</b> · financeiro por voz para pequenas empresas: o dono fala pelo WhatsApp ou pelo app e recebe lançamento, relatório e aviso no celular. Multiempresa em um banco só.</div>
      <div class="card frag" style="padding:24px 30px"><b class="acc">Já decidido antes do experimento</b> · 21 <em>issues</em> fechadas pelo autor (#1–#22) fixam produto e pilha: TypeScript, TanStack Start, tRPC, Drizzle, PostgreSQL, Vitest. Os agentes não escolhem nada disso.</div>
    </div>
    <div class="col card frag" style="display:flex;flex-direction:column;justify-content:center;gap:18px;font-size:23px"><div class="mute">Um só <em>pipeline</em>, sete passos na <em>issue</em> #14 (executar e negar juntos aqui); toda escrita confirma antes de valer (#5, #20).</div>{pipeline_svg()}<div class="mute">Custo zero por padrão: Whisper local; IA por API atrás de <em>flag</em> por empresa, desligada (#4, #12, #17).</div></div>
  </div>
  <div class="card frag hi" style="margin-top:24px;padding:22px 30px;font-size:26px"><b class="acc">A suíte</b> · as 9 <em>issues</em> técnicas (#14–#22) viram os 9 <em>tickets</em> do experimento; cada um tem testes de aceitação escritos pelo autor.<div style="margin-top:16px">{CHIPS}</div></div>
  <div class="denom">Finn (YuukiFST, 2026a): github.com/YuukiFST/Finn. Decisões de produto nas <em>issues</em> #2–#10; decisões técnicas em #11–#22. Em âmbar, o <em>ticket</em> do <em>pipeline</em> desenhado acima.</div>
</section>

<!-- 6 COMO O PROJETO FUNCIONA -->"""

FINN_NOTE = (
    "`<b>Finn (YuukiFST, 2026a) [61].</b> Apresentar o produto antes de usá-lo como suíte: SaaS de financeiro por voz "
    "para pequenas empresas, do próprio autor, especificado em 21 issues fechadas antes do experimento (#1 mapa; #2–#10 "
    "decisões de produto; #11–#22 decisões técnicas). Pipeline de sete passos da issue #14: áudio, texto, intenção, "
    "gate de permissão, executar ou negar, resposta por push; o desenho junta os dois últimos. Os 9 tickets técnicos "
    "(#14–#22) são as tarefas; os agentes recebem o mesmo estado de referência e o mesmo prompt, e o escore é a fração "
    "dos testes de aceitação do autor. Ponto a dizer: é um produto de verdade, com pilha fixa, não uma suíte de tarefas "
    "isoladas como as das comparações publicadas.`,\n"
)

apply(
    Path("dist/apresentacao-pcc.html"),
    [
        (OLD_OBJ, NEW_OBJ),
        ("<!-- 5 COMO O PROJETO FUNCIONA -->", FINN_SLIDE),
        ("`<b>Como o projeto funciona [27]", FINN_NOTE + "`<b>Como o projeto funciona [27]"),
    ],
    tolerant=False,
)
apply(
    Path("deck/index.html"),
    [
        (OLD_OBJ, NEW_OBJ),
        ("<!-- 5 COMO O PROJETO FUNCIONA -->", FINN_SLIDE.replace('class="card frag"', 'class="card frag glass"').replace('class="card frag hi"', 'class="card frag hi glass"')),
    ],
    tolerant=True,
)
apply(
    Path("deck/src/notes.ts"),
    [("  `<b>Como o projeto funciona [27]", "  " + FINN_NOTE + "  `<b>Como o projeto funciona [27]")],
    tolerant=False,
)
apply(
    Path("deck/README.md"),
    [("ordem dos 16 slides", "ordem dos 17 slides"), ("percorrer os 16 slides", "percorrer os 17 slides")],
    tolerant=False,
)
