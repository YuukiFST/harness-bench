"""Gráficos SVG inline do deck explicativo.

Cada função devolve uma string SVG com viewBox fixo; cores vêm de classes CSS
(`f-pi`, `f-oc`, `f-other`, `lbl`, `dim`), então o gráfico segue o tema claro/escuro.
Os números entram por parâmetro a partir de `content.py`; nenhum valor mora aqui.

Uso: `svg = pair_bars(HARNESSTAX)`; o build embute o retorno dentro de `<figure class="chart">`.
"""

from __future__ import annotations

from typing import Sequence



def fmt(v: float, dec: int = 1) -> str:
    """Formata número em pt-BR: vírgula decimal, ponto de milhar."""
    s = f"{v:,.{dec}f}"
    return s.replace(",", " ").replace(".", ",").replace(" ", ".")


def _cls(arm: str) -> str:
    return {"pi": "pi", "oc": "oc"}.get(arm, "other")


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


def pair_bars(rows: Sequence[tuple[str, float, float, str]], footer: str, note: str) -> str:
    """Dois painéis, sucesso (%) e US$ por tentativa; (harness, sucesso, custo, braço) por linha."""
    w, h = 900, 420
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Sucesso e custo por tentativa do mesmo modelo em dois harnesses">']
    panels = [("taxa de sucesso", 1, 100.0, " %", 1), ("US$ por tentativa", 2, 1.6, "", 2)]
    for p, (title, col, vmax, unit, dec) in enumerate(panels):
        px = 40 + p * 440
        out.append(f'<text class="dim" x="{px}" y="30" font-size="17" letter-spacing="1">{title.upper()}</text>')
        for j, row in enumerate(rows):
            lab, v, arm = row[0], row[col], row[3]
            y = 70 + j * 120
            bw = v / vmax * 300
            out.append(f'<text class="lbl" x="{px}" y="{y+20}" font-size="20" font-weight="600">{lab}</text>')
            out.append(f'<rect class="f-{_cls(arm)}" x="{px}" y="{y+34}" width="{bw:.1f}" height="44" rx="5"/>')
            val = ("US$ " if p == 1 else "") + fmt(v, dec) + unit
            out.append(f'<text class="lbl" x="{px+bw+12:.1f}" y="{y+64}" font-size="24" font-weight="600">{val}</text>')
    out.append(f'<text class="f-acc" x="450" y="365" text-anchor="middle" font-size="22" font-weight="600">{footer}</text>')
    out.append(f'<text class="dim" x="450" y="396" text-anchor="middle" font-size="16">{note}</text>')
    out.append("</svg>")
    return "".join(out)


def harness_anatomy() -> str:
    """Anel do harness ao redor do modelo, com o proxy externo abaixo."""
    w, h = 900, 760
    cx, cy = 450, 330
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Anatomia do harness: modelo no centro; system prompt, ferramentas e middleware ao redor; proxy externo fora">']
    out.append(f'<circle class="s-acc" cx="{cx}" cy="{cy}" r="250" fill="none" stroke-width="2" stroke-dasharray="8 8" opacity="0.6"/>')
    out.append(f'<text class="f-acc" x="{cx}" y="{cy-268}" text-anchor="middle" font-size="16" letter-spacing="3" font-weight="600">HARNESS · EXTERNO AO MODELO · EDITÁVEL</text>')
    out.append(f'<circle class="f-acc" cx="{cx}" cy="{cy}" r="92" opacity="0.95"/>')
    out.append(f'<text x="{cx}" y="{cy-8}" text-anchor="middle" font-size="20" font-weight="600" fill="var(--bg)">MODELO</text>')
    out.append(f'<text x="{cx}" y="{cy+18}" text-anchor="middle" font-size="15" fill="var(--bg)">sem estado · fixo</text>')
    # Os três componentes que Lin et al. (2026, p. 1) nomeiam no projeto [66].
    nodes = [
        ("System prompt", "molda o estilo de trabalho", -1, -1),
        ("Ferramentas", "expõem o sistema de arquivos e o shell", 1, -1),
        ("Middleware", "controla contexto, execução e recuperação", 0, 1),
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
    out.append(f'<text class="dim" x="{cx}" y="{py+20}" text-anchor="middle" font-size="14">fora do <tspan font-style="italic">harness</tspan> · conta igual para os dois <tspan font-style="italic">coding agents</tspan></text>')
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
    box(40, 190, 320, 120, "Harness", ["OpenCode ou Pi", "versão fixada [76]"])
    arrow(360, 250, 556, 250, "requisição HTTP")
    out.append('<rect x="560" y="160" width="360" height="200" rx="12" fill="var(--pi-dim)" stroke="var(--pi)" stroke-width="2"/>')
    out.append('<text class="f-pi" x="740" y="210" text-anchor="middle" font-size="24" font-weight="600">Proxy reverso</text>')
    for i, s in enumerate(["guarda requisições, latência e tokens", "tokens: usage do gateway", "harness: só verificação cruzada", 'fora do <tspan font-style="italic">harness</tspan>']):
        out.append(f'<text class="dim" x="740" y="{246+i*24}" text-anchor="middle" font-size="15">{s}</text>')
    arrow(920, 220, 1076, 110, "Camada 1")
    arrow(920, 300, 1076, 400, "Camada 2")
    box(1080, 40, 400, 130, "Endpoint simulado", ["esquemas, system prompt, tokens", "carga fixa sem tarefa"])
    box(1080, 350, 400, 130, "Modelo real via gateway", ["construção do produto", "ao menos 3 construções por célula"])
    out.append('<text class="dim" x="1280" y="200" text-anchor="middle" font-size="15">o que cada requisição carrega</text>')
    out.append('<text class="dim" x="1280" y="510" text-anchor="middle" font-size="15">tokens por construção ao lado do sucesso (H1)</text>')
    out.append("</svg>")
    return "".join(out)


def title_decor() -> str:
    """Marca da capa: anéis concêntricos = camadas do harness em torno do modelo."""
    out = ['<svg viewBox="0 0 520 520" aria-hidden="true">']
    for i, r in enumerate((60, 110, 160, 210, 250)):
        op = 0.9 - i * 0.16
        dash = "" if i == 0 else f' stroke-dasharray="{6+i*4} {8+i*3}"'
        out.append(f'<circle class="ring" cx="260" cy="260" r="{r}" fill="none" stroke="var(--accent)" stroke-width="{3 if i==0 else 1.5}" opacity="{op:.2f}"{dash}/>')
    out.append('<circle cx="260" cy="260" r="34" fill="var(--accent)"/>')
    out.append('<circle cx="260" cy="510" r="7" fill="var(--pi)"/>')
    out.append('<line x1="260" y1="294" x2="260" y2="503" stroke="var(--pi)" stroke-width="2" stroke-dasharray="3 6" opacity="0.8"/>')
    out.append("</svg>")
    return "".join(out)
