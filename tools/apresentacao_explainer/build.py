"""Gera dist/apresentacao-explainer/index.html: deck explicativo, arquivo único, sem rede.

Uso:
    python tools/apresentacao_explainer/build.py
Depois abrir dist/apresentacao-explainer/index.html (setas navegam; N notas; O sumário; ? ajuda).

Estrutura: styles.css + engine.js + fontes OFL em base64 embutidos; slides em slides.py;
gráficos SVG em charts.py; dados em content.py. O deck original (deck/ → dist/apresentacao/)
fica intacto; este é o experimento visual pedido em 2026-09-15.
"""

from __future__ import annotations

import base64
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / "dist" / "apresentacao-explainer" / "index.html"

sys.path.insert(0, str(HERE))
from slides import all_slides  # noqa: E402

FONTS = [
    ("Fraunces", "normal", "300 700", "fraunces.woff2"),
    ("Fraunces", "italic", "300 700", "fraunces-italic.woff2"),
    ("IBM Plex Sans", "normal", "400 600", "plex-sans.woff2"),
    ("IBM Plex Mono", "normal", "400", "plex-mono-400.woff2"),
    ("IBM Plex Mono", "normal", "500", "plex-mono-500.woff2"),
    ("IBM Plex Mono", "normal", "600", "plex-mono-600.woff2"),
]

FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
    "%3Crect width='64' height='64' rx='14' fill='%23f3efe6'/%3E"
    "%3Ccircle cx='32' cy='32' r='22' fill='none' stroke='%2313606a' stroke-width='3' stroke-dasharray='6 5'/%3E"
    "%3Ccircle cx='32' cy='32' r='9' fill='%2313606a'/%3E%3C/svg%3E"
)


def font_faces() -> str:
    faces = []
    for family, style, weight, fname in FONTS:
        data = base64.b64encode((HERE / "fonts" / fname).read_bytes()).decode("ascii")
        faces.append(
            f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{weight};font-display:swap;"
            f"src:url(data:font/woff2;base64,{data}) format('woff2');}}"
        )
    return "\n".join(faces)


def build() -> Path:
    css = (HERE / "styles.css").read_text(encoding="utf-8")
    js = (HERE / "engine.js").read_text(encoding="utf-8")
    slides = all_slides()
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Como o harness altera o custo e o desempenho do modelo — deck explicativo</title>
<link rel="icon" href="{FAVICON}">
<!-- Gerado por tools/apresentacao_explainer/build.py. Não editar à mão: edite slides.py, content.py, charts.py ou styles.css e rode o build. -->
<!-- Fontes: Fraunces, IBM Plex Sans, IBM Plex Mono (SIL OFL), embutidas em base64; sem CDN. -->
<script>document.documentElement.classList.add('js');</script>
<style>
{font_faces()}
{css}
</style>
</head>
<body>
<div class="deck">
{slides}
</div>
<script>
{js}
</script>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    return OUT


if __name__ == "__main__":
    path = build()
    n = path.read_text(encoding="utf-8").count('<section class="slide')
    print(f"{path.relative_to(ROOT)}: {path.stat().st_size // 1024} KB, {n} slides")
