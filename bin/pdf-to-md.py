"""PDF -> Markdown extractor for the harness-bench knowledge base.

Usage:
    & "$env:TEMP\\pdfenv\\Scripts\\python.exe" bin/pdf-to-md.py <input.pdf> <output.md>

What it does (and does not do):
- Two-column aware: blocks are grouped into left/right columns by x position,
  each column sorted top-to-bottom, left column first. Single-column pages
  fall through to plain top-to-bottom order.
- Headings are inferred from font size: the largest size on the first two
  pages becomes `#`, the next distinct sizes become `##` / `###`.
  This is heuristic; the wiki source page curates the final section map.
- Tables found by PyMuPDF (`find_tables`) are emitted as GitHub tables.
- De-hyphenates line-break splits (`experi-\\nment` -> `experiment`).
- Does NOT OCR scans (all arXiv PDFs here have a text layer) and does NOT
  extract figures as images; figure captions are kept as `> Figure:` quotes.
- Page boundaries are marked as `<!-- pN -->` so a reader can cite depth.

The output is an intermediate artifact: the wiki page under `wiki/sources/`
is what future agents read. Keep the extractor deterministic (no LLM).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def dehyphen(text: str) -> str:
    return re.sub(r"(\w)-\n(\w)", r"\1\2", text)


def main() -> None:
    import pymupdf

    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    doc = pymupdf.open(src)
    # Font-size census on first pages to pick heading thresholds.
    sizes: dict[float, int] = {}
    for page in doc[: min(3, len(doc))]:
        for b in page.get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    s = round(span["size"], 1)
                    sizes[s] = sizes.get(s, 0) + len(span["text"])
    ranked = sorted(sizes, reverse=True)
    h1 = ranked[0] if ranked else 99.0
    h2 = ranked[1] if len(ranked) > 1 else h1
    h3 = ranked[2] if len(ranked) > 2 else h2
    body_size = max(sizes, key=lambda s: sizes[s]) if sizes else 10.0

    out: list[str] = []
    out.append(f"<!-- extracted from {src.name}, {len(doc)} pages, body~{body_size}pt -->")
    for pno, page in enumerate(doc, start=1):
        out.append(f"\n<!-- p{pno} -->\n")
        w = page.rect.width
        blocks = [b for b in page.get_text("dict")["blocks"] if b.get("lines")]
        # Column split: median of block x0 decides; single column when spread is narrow.
        x0s = sorted(b["bbox"][0] for b in blocks)
        two_col = len(x0s) > 4 and (x0s[-1] - x0s[0] > w * 0.45)
        if two_col:
            left = [b for b in blocks if b["bbox"][0] < w / 2]
            right = [b for b in blocks if b["bbox"][0] >= w / 2]
            left.sort(key=lambda b: b["bbox"][1])
            right.sort(key=lambda b: b["bbox"][1])
            ordered = left + right
        else:
            ordered = sorted(blocks, key=lambda b: (round(b["bbox"][1]), b["bbox"][0]))
        for b in ordered:
            paras: list[str] = []
            maxsize = 0.0
            for line in b["lines"]:
                parts = []
                for span in line["spans"]:
                    maxsize = max(maxsize, round(span["size"], 1))
                    parts.append(span["text"])
                paras.append("".join(parts))
            text = "\n".join(paras).strip()
            if not text:
                continue
            if len(text) < 60 and maxsize >= h2 and re.search(r"[A-Za-z]", text):
                if maxsize >= h1 - 0.1:
                    out.append(f"\n# {text}\n")
                elif maxsize >= h2 - 0.1:
                    out.append(f"\n## {text}\n")
                elif maxsize >= h3 - 0.1:
                    out.append(f"\n### {text}\n")
                else:
                    out.append(text + "\n")
            elif re.match(r"(?i)^(figure|fig\.?|table)\s+\d+", text):
                out.append(f"\n> {text}\n")
            elif re.match(r"^references\s*$", text, re.I) and len(text) < 20:
                out.append("\n## References\n")
            else:
                out.append(dehyphen(text) + "\n")
        # Tables after text so they stay on their page.
        try:
            for tab in page.find_tables():
                rows = tab.extract()
                if not rows or not any(any(c for c in r) for r in rows):
                    continue
                header = [(c or "").strip().replace("\n", " ") for c in rows[0]]
                out.append("\n| " + " | ".join(header) + " |")
                out.append("| " + " | ".join(["---"] * len(header)) + " |")
                for r in rows[1:]:
                    cells = [(c or "").strip().replace("\n", " ") for c in r]
                    out.append("| " + " | ".join(cells) + " |")
                out.append("")
        except Exception as exc:  # tables are bonus, never fatal
            out.append(f"\n<!-- table extraction skipped on p{pno}: {exc} -->\n")

    dst.write_text("\n".join(out), encoding="utf-8")
    print(f"{dst}: {len(doc)} pages")


if __name__ == "__main__":
    main()
