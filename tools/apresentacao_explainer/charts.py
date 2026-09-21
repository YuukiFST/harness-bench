"""Gráficos SVG inline do deck explicativo.

Cada função devolve uma string SVG com viewBox fixo; cores vêm de classes CSS
(`f-pi`, `f-oc`, `f-other`, `lbl`, `dim`), então o gráfico segue o tema claro/escuro.
Os números entram por parâmetro a partir de `content.py`; nenhum valor mora aqui.

Uso: `svg = frontier_scatter(FRONTIER)`; o build embute o retorno dentro de `<figure class="chart">`.
"""

from __future__ import annotations

import math
from typing import Sequence



def fmt(v: float, dec: int = 1) -> str:
    """Formata número em pt-BR: vírgula decimal, ponto de milhar."""
    s = f"{v:,.{dec}f}"
    return s.replace(",", " ").replace(".", ",").replace(" ", ".")


def fmt_int(v: int) -> str:
    return f"{v:,}".replace(",", ".")


def _cls(arm: str) -> str:
    return {"pi": "pi", "oc": "oc"}.get(arm, "other")


def frontier_scatter(rows: Sequence[tuple[str, float, float, str]]) -> str:
    """Dispersão custo por aprovação (x, log) vs taxa de aprovação (y) das 12 configurações."""
    w, h = 1200, 560
    ml, mr, mt, mb = 80, 40, 30, 70
    x0, x1 = math.log10(0.9), math.log10(24.0)
    y0, y1 = 45.0, 70.0
    pw, ph = w - ml - mr, h - mt - mb

    def sx(v: float) -> float:
        return ml + (math.log10(v) - x0) / (x1 - x0) * pw

    def sy(v: float) -> float:
        return mt + (1 - (v - y0) / (y1 - y0)) * ph

    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Dispersão: custo por tarefa aprovada contra taxa de aprovação de 12 configurações de harness sobre o mesmo modelo">']
    for gy in range(50, 71, 5):
        out.append(f'<line class="grid" x1="{ml}" y1="{sy(gy):.1f}" x2="{w-mr}" y2="{sy(gy):.1f}" stroke-width="1"/>')
        out.append(f'<text class="dim" x="{ml-12}" y="{sy(gy)+5:.1f}" text-anchor="end" font-size="16">{gy} %</text>')
    for gx in (1, 2, 3, 5, 10, 20):
        out.append(f'<line class="grid" x1="{sx(gx):.1f}" y1="{mt}" x2="{sx(gx):.1f}" y2="{h-mb}" stroke-width="1"/>')
        out.append(f'<text class="dim" x="{sx(gx):.1f}" y="{h-mb+26}" text-anchor="middle" font-size="16">US$ {gx}</text>')
    out.append(f'<line class="axis" x1="{ml}" y1="{h-mb}" x2="{w-mr}" y2="{h-mb}" stroke-width="1.5"/>')
    out.append(f'<line class="axis" x1="{ml}" y1="{mt}" x2="{ml}" y2="{h-mb}" stroke-width="1.5"/>')
    out.append(f'<text class="dim" x="{w-mr}" y="{h-8}" text-anchor="end" font-size="15">custo mediano por tarefa aprovada (US$, escala logarítmica)</text>')
    out.append(f'<text class="dim" x="{ml+6}" y="{mt-10}" font-size="15">taxa de aprovação</text>')
    # (dx, dy): dx negativo ancora o rótulo à esquerda do ponto; dy afasta pares na mesma linha
    offsets = {
        "Codex": (16, -4), "DSH Creator": (-16, 0), "Claude Code": (-18, 0), "Pi": (-18, 0),
        "DSH Standard": (16, -22), "DSH PTC": (16, 19), "Kimi Code": (-16, 0), "DSH Minimal": (16, -27),
        "Oh My Pi": (16, 22), "Exo Harness": (16, 0), "Hermes": (-16, 0), "OpenCode": (16, 0),
    }
    for name, pas, cost, arm in rows:
        cx, cy = sx(cost), sy(pas)
        r = 13 if arm in ("pi", "oc") else 9
        out.append(f'<circle class="f-{_cls(arm)}" cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" opacity="{1 if arm in ("pi","oc") else 0.75}"/>')
        dx, dy = offsets.get(name, (16, 0))
        anchor = "end" if dx < 0 else "start"
        weight = "600" if arm in ("pi", "oc") else "400"
        cls = "lbl" if arm in ("pi", "oc") else "dim"
        out.append(f'<text class="{cls}" x="{cx+dx:.1f}" y="{cy+dy+6:.1f}" text-anchor="{anchor}" font-size="17" font-weight="{weight}">{name} · {fmt(pas)} % · US$ {fmt(cost,2)}</text>')
    out.append("</svg>")
    return "".join(out)


def hbars(
    rows: Sequence[tuple[str, float, str]],
    unit: str,
    dec: int = 1,
    vmax: float | None = None,
    aria: str = "",
    log: bool = False,
    height_per_row: int = 58,
) -> str:
    """Barras horizontais: (rótulo, valor, braço). `log` usa escala log10 para razões grandes."""
    w = 1200
    label_w = int(max(len(r[0]) for r in rows) * 11.6) + 12  # mono 19px ≈ 11,6 px por caractere
    ml, mr = label_w + 20, 220
    h = 40 + height_per_row * len(rows)
    pw = w - ml - mr
    vmax = vmax or max(v for _, v, _ in rows)
    vmin = min(v for _, v, _ in rows)

    def sx(v: float) -> float:
        if log:
            lo = math.floor(math.log10(vmin))
            return (math.log10(v) - lo) / (math.log10(vmax) - lo) * pw
        return v / vmax * pw

    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">']
    if log:
        lo = math.floor(math.log10(vmin))
        hi = math.ceil(math.log10(vmax))
        for e in range(lo, hi + 1):
            gx = ml + sx(10**e) if 10**e >= vmin else None
            if gx is None or gx > ml + pw:
                continue
            out.append(f'<line class="grid" x1="{gx:.1f}" y1="20" x2="{gx:.1f}" y2="{h-20}" stroke-width="1"/>')
            out.append(f'<text class="dim" x="{gx:.1f}" y="{h-4}" text-anchor="middle" font-size="14">{fmt_int(10**e)}</text>')
    for i, (label, v, arm) in enumerate(rows):
        y = 30 + i * height_per_row
        bh = height_per_row - 20
        bw = sx(v)
        out.append(f'<text class="lbl" x="{ml-16}" y="{y+bh/2+6}" text-anchor="end" font-size="19" font-weight="{600 if arm in ("pi","oc") else 400}">{label}</text>')
        out.append(f'<rect class="f-{_cls(arm)}" x="{ml}" y="{y}" width="{bw:.1f}" height="{bh}" rx="4" opacity="{1 if arm in ("pi","oc") else 0.7}"/>')
        val = fmt_int(int(round(v))) if dec == 0 else fmt(v, dec)
        out.append(f'<text class="lbl" x="{ml+bw+12:.1f}" y="{y+bh/2+6}" font-size="19" font-weight="600">{val}{unit}</text>')
    out.append("</svg>")
    return "".join(out)


def vbars(rows: Sequence[tuple[str, float, str]], unit: str, vmax: float, aria: str, sub: Sequence[str] | None = None) -> str:
    """Barras verticais com valor no topo; `sub` é uma linha extra sob cada rótulo."""
    w, h = 900, 520
    ml, mr, mt, mb = 40, 20, 50, 90 if sub else 60
    pw, ph = w - ml - mr, h - mt - mb
    n = len(rows)
    slot = pw / n
    bw = slot * 0.56
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">']
    for g in range(0, int(vmax) + 1, 20):
        gy = mt + ph - g / vmax * ph
        out.append(f'<line class="grid" x1="{ml}" y1="{gy:.1f}" x2="{w-mr}" y2="{gy:.1f}" stroke-width="1"/>')
    for i, (label, v, arm) in enumerate(rows):
        x = ml + slot * i + (slot - bw) / 2
        bh = v / vmax * ph
        y = mt + ph - bh
        out.append(f'<rect class="f-{_cls(arm)}" x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="6" opacity="{1 if arm in ("pi","oc") else 0.8}"/>')
        out.append(f'<text class="lbl" x="{x+bw/2:.1f}" y="{y-12:.1f}" text-anchor="middle" font-size="26" font-weight="600">{fmt(v)}{unit}</text>')
        out.append(f'<text class="lbl" x="{x+bw/2:.1f}" y="{mt+ph+30}" text-anchor="middle" font-size="20">{label}</text>')
        if sub:
            out.append(f'<text class="dim" x="{x+bw/2:.1f}" y="{mt+ph+56}" text-anchor="middle" font-size="15">{sub[i]}</text>')
    out.append(f'<line class="axis" x1="{ml}" y1="{mt+ph}" x2="{w-mr}" y2="{mt+ph}" stroke-width="1.5"/>')
    out.append("</svg>")
    return "".join(out)


def dumbbell(rows: Sequence[tuple[str, float, float]], left: str, right: str, aria: str) -> str:
    """Haltere: mesmo modelo, dois scaffolds; (modelo, valor esquerdo, valor direito) em %."""
    w = 1200
    rh = 74
    h = 60 + rh * len(rows)
    ml, mr = 300, 60
    pw = w - ml - mr

    def sx(v: float) -> float:
        return ml + v / 60 * pw

    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">']
    for g in range(0, 61, 10):
        out.append(f'<line class="grid" x1="{sx(g):.1f}" y1="30" x2="{sx(g):.1f}" y2="{h-30}" stroke-width="1"/>')
        out.append(f'<text class="dim" x="{sx(g):.1f}" y="{h-8}" text-anchor="middle" font-size="15">{g} %</text>')
    out.append(f'<circle class="f-acc" cx="{ml}" cy="16" r="7"/><text class="lbl" x="{ml+14}" y="21" font-size="16">{left}</text>')
    out.append(f'<circle class="f-bad" cx="{ml+260}" cy="16" r="7"/><text class="lbl" x="{ml+274}" y="21" font-size="16">{right}</text>')
    for i, (model, a, b) in enumerate(rows):
        y = 60 + i * rh
        out.append(f'<text class="lbl" x="{ml-20}" y="{y+7}" text-anchor="end" font-size="19">{model}</text>')
        out.append(f'<line class="s-other" x1="{sx(b):.1f}" y1="{y}" x2="{sx(a):.1f}" y2="{y}" stroke-width="6" stroke-linecap="round" opacity="0.5"/>')
        out.append(f'<circle class="f-acc" cx="{sx(a):.1f}" cy="{y}" r="12"/>')
        out.append(f'<circle class="f-bad" cx="{sx(b):.1f}" cy="{y}" r="12"/>')
        out.append(f'<text class="lbl" x="{sx(a)+18:.1f}" y="{y+7}" font-size="18" font-weight="600">{fmt(a)} %</text>')
        if sx(b) - ml < 130:  # valor baixo demais para caber à esquerda do ponto: vai por baixo
            out.append(f'<text class="lbl" x="{sx(b):.1f}" y="{y+36}" text-anchor="middle" font-size="18" font-weight="600">{fmt(b)} %</text>')
        else:
            out.append(f'<text class="lbl" x="{sx(b)-18:.1f}" y="{y+7}" text-anchor="end" font-size="18" font-weight="600">{fmt(b)} %</text>')
        out.append(f'<text class="f-bad" x="{(sx(a)+sx(b))/2:.1f}" y="{y-18}" text-anchor="middle" font-size="16" font-weight="600">−{fmt(a-b,0)} pp</text>')
    out.append("</svg>")
    return "".join(out)


def pair_bars(pi: tuple[float, float], oc: tuple[float, float]) -> str:
    """H1: dois painéis pequenos, aprovação e US$ por aprovada, pi contra OpenCode."""
    w, h = 900, 420
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="pi contra OpenCode no FrontierHarness: aprovação e custo por tarefa aprovada">']
    panels = [("taxa de aprovação", pi[0], oc[0], 70.0, " %", 1), ("US$ por tarefa aprovada", pi[1], oc[1], 4.0, "", 2)]
    for p, (title, a, b, vmax, unit, dec) in enumerate(panels):
        px = 40 + p * 440
        out.append(f'<text class="dim" x="{px}" y="30" font-size="17" letter-spacing="1">{title.upper()}</text>')
        for j, (lab, v, arm) in enumerate((("pi", a, "pi"), ("OpenCode", b, "oc"))):
            y = 70 + j * 120
            bw = v / vmax * 300
            out.append(f'<text class="lbl" x="{px}" y="{y+20}" font-size="20" font-weight="600">{lab}</text>')
            out.append(f'<rect class="f-{arm}" x="{px}" y="{y+34}" width="{bw:.1f}" height="44" rx="5"/>')
            val = ("US$ " if p == 1 else "") + fmt(v, dec) + unit
            out.append(f'<text class="lbl" x="{px+bw+12:.1f}" y="{y+64}" font-size="24" font-weight="600">{val}</text>')
    out.append('<text class="f-acc" x="450" y="365" text-anchor="middle" font-size="22" font-weight="600">OpenCode paga 1,33× por tarefa aprovada e aprova 10 pp a menos</text>')
    out.append('<text class="dim" x="450" y="396" text-anchor="middle" font-size="16">cálculo do autor sobre a tabela do post · Kimi K3 · 30 tarefas · 1 tentativa por célula</text>')
    out.append("</svg>")
    return "".join(out)


def harness_anatomy() -> str:
    """Anel do harness ao redor do modelo, com o proxy externo abaixo."""
    w, h = 900, 760
    cx, cy = 450, 330
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Anatomia do harness: modelo no centro; prompt de sistema, ferramentas, middleware de contexto e laço de execução ao redor; proxy externo fora">']
    out.append(f'<circle class="s-acc" cx="{cx}" cy="{cy}" r="250" fill="none" stroke-width="2" stroke-dasharray="8 8" opacity="0.6"/>')
    out.append(f'<text class="f-acc" x="{cx}" y="{cy-268}" text-anchor="middle" font-size="16" letter-spacing="3" font-weight="600">HARNESS · EXTERNO AO MODELO · EDITÁVEL</text>')
    out.append(f'<circle class="f-acc" cx="{cx}" cy="{cy}" r="92" opacity="0.95"/>')
    out.append(f'<text x="{cx}" y="{cy-8}" text-anchor="middle" font-size="20" font-weight="600" fill="var(--bg)">MODELO</text>')
    out.append(f'<text x="{cx}" y="{cy+18}" text-anchor="middle" font-size="15" fill="var(--bg)">sem estado · fixo</text>')
    nodes = [
        ("Prompt de sistema", "molda o estilo de trabalho", -1, -1),
        ("Ferramentas", "arquivos e shell; esquemas por requisição", 1, -1),
        ("Middleware de contexto", "compactação, memória, permissões", -1, 1),
        ("Laço de execução", "monta prompt, chama ferramenta, repete", 1, 1),
    ]
    for name, desc, sx_, sy_ in nodes:
        nx, ny = cx + sx_ * 235, cy + sy_ * 150
        out.append(f'<line class="s-acc" x1="{cx + sx_*92*0.72:.0f}" y1="{cy + sy_*92*0.7:.0f}" x2="{nx - sx_*120:.0f}" y2="{ny - sy_*34:.0f}" stroke-width="2" opacity="0.5"/>')
        out.append(f'<rect class="surface" x="{nx-175}" y="{ny-46}" width="350" height="92" rx="12" stroke-width="1.5"/>')
        out.append(f'<text class="lbl" x="{nx}" y="{ny-8}" text-anchor="middle" font-size="21" font-weight="600">{name}</text>')
        out.append(f'<text class="dim" x="{nx}" y="{ny+20}" text-anchor="middle" font-size="13">{desc}</text>')
    py = 690
    out.append(f'<line class="s-other" x1="{cx}" y1="{cy+250}" x2="{cx}" y2="{py-44}" stroke-width="2" stroke-dasharray="4 6"/>')
    out.append(f'<rect x="{cx-280}" y="{py-44}" width="560" height="88" rx="12" fill="var(--pi-dim)" stroke="var(--pi)" stroke-width="1.5"/>')
    out.append(f'<text class="f-pi" x="{cx}" y="{py-8}" text-anchor="middle" font-size="21" font-weight="600">Proxy externo (instrumento)</text>')
    out.append(f'<text class="dim" x="{cx}" y="{py+20}" text-anchor="middle" font-size="14">fora do harness · conta requisições, tokens e latência dos dois braços</text>')
    out.append("</svg>")
    return "".join(out)


def layers_flow() -> str:
    """Camada 1 (endpoint simulado) e Camada 2 (modelo real) passando pelo mesmo proxy."""
    w, h = 1500, 520
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Duas camadas de medição: o harness fala com um proxy; na Camada 1 o proxy responde por um endpoint simulado, na Camada 2 encaminha ao modelo real">']

    def box(x: float, y: float, bw: float, bh: float, title: str, subs: list[str], cls: str = "surface", tcls: str = "lbl") -> None:
        out.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{bw}" height="{bh}" rx="12" stroke-width="1.5"/>')
        ty = y + 40
        out.append(f'<text class="{tcls}" x="{x+bw/2}" y="{ty}" text-anchor="middle" font-size="22" font-weight="600">{title}</text>')
        for i, s in enumerate(subs):
            out.append(f'<text class="dim" x="{x+bw/2}" y="{ty+28+i*22}" text-anchor="middle" font-size="15">{s}</text>')

    def arrow(x1: float, y1: float, x2: float, y2: float, label: str = "") -> None:
        out.append(f'<line class="s-acc" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-width="2.5" marker-end="url(#arr)"/>')
        if label:
            out.append(f'<text class="f-acc" x="{(x1+x2)/2}" y="{(y1+y2)/2-12}" text-anchor="middle" font-size="15" font-weight="600">{label}</text>')

    out.append('<defs><marker id="arr" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10z" fill="var(--accent)"/></marker></defs>')
    out.append('<text class="f-pi" x="200" y="170" text-anchor="middle" font-size="15" font-weight="600">mesmo executor, prompt e especificação</text>')
    box(40, 190, 320, 120, "Harness", ["OpenCode ou pi, sem interface", "URL base OpenAI-compatível"])
    arrow(360, 250, 556, 250, "requisição HTTP")
    out.append('<rect x="560" y="160" width="360" height="200" rx="12" fill="var(--pi-dim)" stroke="var(--pi)" stroke-width="2"/>')
    out.append('<text class="f-pi" x="740" y="210" text-anchor="middle" font-size="24" font-weight="600">Proxy reverso</text>')
    for i, s in enumerate(["conta bytes, tokens e latência", "um tokenizador para os dois braços", "força o relatório de uso", "instrumento do projeto, fora do harness"]):
        out.append(f'<text class="dim" x="740" y="{246+i*24}" text-anchor="middle" font-size="15">{s}</text>')
    arrow(920, 220, 1076, 110, "Camada 1")
    arrow(920, 300, 1076, 400, "Camada 2")
    box(1080, 40, 400, 130, "Endpoint simulado", ["determinístico · sem cota", "carga fixa por requisição (H2)"])
    box(1080, 350, 400, 130, "Modelo real via gateway", ["estocástico · consome cota", "n ≥ 3 construções por célula"])
    out.append('<text class="dim" x="1280" y="200" text-anchor="middle" font-size="15">esquemas, bytes de prompt, tokens por passo</text>')
    out.append('<text class="dim" x="1280" y="510" text-anchor="middle" font-size="15">tokens por construção ao lado do sucesso (H1)</text>')
    out.append("</svg>")
    return "".join(out)


def title_decor() -> str:
    """Marca da capa: anéis concêntricos = camadas do harness em torno do modelo."""
    out = ['<svg viewBox="0 0 520 520" aria-hidden="true">']
    for i, r in enumerate((60, 110, 160, 210, 250)):
        op = 0.9 - i * 0.16
        dash = "" if i == 0 else f' stroke-dasharray="{6+i*4} {8+i*3}"'
        out.append(f'<circle cx="260" cy="260" r="{r}" fill="none" stroke="var(--accent)" stroke-width="{3 if i==0 else 1.5}" opacity="{op:.2f}"{dash}/>')
    out.append('<circle cx="260" cy="260" r="34" fill="var(--accent)"/>')
    out.append('<circle cx="260" cy="510" r="7" fill="var(--pi)"/>')
    out.append('<line x1="260" y1="294" x2="260" y2="503" stroke="var(--pi)" stroke-width="2" stroke-dasharray="3 6" opacity="0.8"/>')
    out.append("</svg>")
    return "".join(out)
