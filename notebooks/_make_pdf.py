#!/usr/bin/env python3
"""Build a single combined PDF from the FUSION Boot Camp notebook series.

Strategy (no LaTeX / no Chromium — both unavailable here):
  1. Inject a setup cell that registers a Hebrew font with matplotlib and
     reorders Hebrew strings via the bidi algorithm, so plot labels render
     correctly RTL.
  2. Execute build-copies of each notebook (the committed notebooks are left
     untouched).
  3. Export each to an HTML body fragment and concatenate them into one HTML
     document with RTL-aware CSS, then render to PDF with WeasyPrint.
"""
import base64
import copy
import os
import re
from io import BytesIO

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import mathtext

_MATH_PARSER = mathtext.MathTextParser("agg")
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "FUSION_Boot_Camp_2026_notebooks.pdf")

NOTEBOOKS = [
    "00_overview.ipynb",
    "01_introduction_to_information_fusion.ipynb",
    "02_parameter_estimation.ipynb",
    "03_state_estimation_kalman_filter.ipynb",
    "04_target_tracking_maneuvering.ipynb",
    "05_data_association.ipynb",
    "06_distributed_target_tracking.ipynb",
    "07_attributes_classification.ipynb",
    "08_distributed_inference.ipynb",
    "09_high_level_fusion.ipynb",
]

# Setup cell prepended (at execution time) to every notebook copy.
SETUP_SRC = r"""
import re, matplotlib
import matplotlib.font_manager as fm
import matplotlib.text as _mtext
for _f in ['/usr/share/fonts/truetype/noto-hebrew/NotoSansHebrew-Regular.ttf',
           '/usr/share/fonts/truetype/noto-hebrew/NotoSansHebrew-Bold.ttf']:
    try: fm.fontManager.addfont(_f)
    except Exception: pass
matplotlib.rcParams['font.family'] = ['DejaVu Sans', 'Noto Sans Hebrew']
matplotlib.rcParams['axes.unicode_minus'] = False
try:
    from bidi import get_display          # python-bidi >= 0.6
except Exception:
    from bidi.algorithm import get_display # older
_HEB = re.compile('[֐-׿]')
_orig_set_text = _mtext.Text.set_text
def _bidi_set_text(self, s):
    try:
        if isinstance(s, str) and _HEB.search(s):
            s = get_display(s)
    except Exception:
        pass
    return _orig_set_text(self, s)
_mtext.Text.set_text = _bidi_set_text
"""

CSS = """
@page { size: A4; margin: 1.6cm 1.4cm; }
body { font-family: 'Noto Sans Hebrew','DejaVu Sans',sans-serif; font-size: 10.5pt;
       line-height: 1.5; color: #1a1a1a; }
/* Markdown -> RTL */
.jp-RenderedMarkdown, .jp-MarkdownCell { direction: rtl; text-align: right; }
.jp-RenderedMarkdown table { direction: rtl; margin: 0.4em 0; border-collapse: collapse; }
.jp-RenderedMarkdown th, .jp-RenderedMarkdown td { border: 1px solid #bbb; padding: 3px 7px; }
.jp-RenderedMarkdown h1 { font-size: 17pt; border-bottom: 2px solid #355; padding-bottom: 3px; color:#234; }
.jp-RenderedMarkdown h2 { font-size: 13.5pt; color:#345; margin-top: 0.8em; }
.jp-RenderedMarkdown h3 { font-size: 11.5pt; color:#456; }
/* Code + outputs stay LTR */
.jp-CodeCell, .jp-InputArea, .jp-OutputArea, pre, code { direction: ltr; text-align: left; }
.jp-InputArea pre, .highlight pre { background:#f5f5f5; border:1px solid #e0e0e0;
       border-radius:4px; padding:6px 9px; font-size:8.6pt; font-family:'DejaVu Sans Mono',monospace;
       white-space: pre-wrap; word-break: break-word; }
.jp-OutputArea pre { font-size:8.6pt; font-family:'DejaVu Sans Mono',monospace; white-space: pre-wrap; }
.jp-OutputArea img, img { max-width: 100%; height: auto; display:block; margin: 0.3em auto; }
.math-inline { vertical-align: middle; height: 1.05em; }
.math-display { display:block; margin: 0.6em auto; max-width:100%; max-height: 8.5em; }
.nb-sep { page-break-before: always; }
.jp-Cell { margin: 0.35em 0; }
/* hide noisy prompts */
.jp-InputPrompt, .jp-OutputPrompt { display:none; }
"""


def _sanitize(tex):
    """Map common LaTeX commands unsupported by mathtext to supported ones."""
    tex = " ".join(tex.split())
    tex = re.sub(r"\\operatorname\{([^}]*)\}", r"\\mathrm{\1}", tex)
    tex = re.sub(r"\\(qquad)", r"\\quad\\quad", tex)
    tex = tex.replace("\\mid", "|").replace("\\!", "").replace("\\:", "\\,")
    tex = tex.replace("\\Longrightarrow", "\\Rightarrow")
    tex = tex.replace("\\varnothing", "\\emptyset")
    tex = re.sub(r"\\ge(?![a-zA-Z])", r"\\geq", tex)
    tex = re.sub(r"\\le(?![a-zA-Z])", r"\\leq", tex)
    tex = re.sub(r"\\gtrless(?![a-zA-Z])", r"\\lessgtr", tex)
    tex = re.sub(r"\\[td]frac", r"\\frac", tex)
    tex = re.sub(r"\\frac\s*([0-9A-Za-z])\s*([0-9A-Za-z])", r"\\frac{\1}{\2}", tex)
    tex = re.sub(r"\\sqrt\s*([0-9A-Za-z])(?![A-Za-z])", r"\\sqrt{\1}", tex)
    tex = re.sub(r"\\(Bigg|bigg|Big|big)([\[\]()|])", r"\2", tex)
    return tex


def _can_parse(tex):
    """True if matplotlib mathtext can actually parse the snippet.
    (mathtext renders unparseable input as literal text instead of raising
    during savefig, so we must validate up front.)"""
    try:
        _MATH_PARSER.parse(f"${tex.strip()}$")
        return True
    except Exception:
        return False


def _math_png(tex, fontsize):
    """Render a mathtext-parseable LaTeX snippet to a transparent PNG."""
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, f"${tex.strip()}$", fontsize=fontsize, color="#111")
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight",
                pad_inches=0.03, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()


def _img_tag(b64, cls):
    return f"<img class='{cls}' src='data:image/png;base64,{b64}'/>"


def _png_bytes(tex, fontsize):
    """Render a parseable snippet to a transparent PNG (raw bytes)."""
    return base64.b64decode(_math_png(tex, fontsize))


def _pil(tex, fontsize):
    """Render a snippet (matrix-free) to a PIL RGBA image."""
    from PIL import Image
    tex = _sanitize(tex)
    if not _can_parse(tex):
        tex = tex.replace("\\", "")  # last-resort: strip commands so it at least shows
        tex = tex if _can_parse(tex) else "?"
    return Image.open(BytesIO(_png_bytes(tex, fontsize))).convert("RGBA")


def _matrix_pil(rows, fontsize):
    """Compose a bracketed matrix as a single PIL image."""
    from PIL import Image, ImageDraw
    cells = [[_pil(c, fontsize) for c in row] for row in rows]
    ncol = max(len(r) for r in cells)
    colw = [max(cells[r][c].width for r in range(len(cells)) if c < len(cells[r]))
            for c in range(ncol)]
    rowh = [max(im.height for im in row) for row in cells]
    padx, pady = 14, 10
    gridw = sum(colw) + padx * (ncol + 1)
    gridh = sum(rowh) + pady * (len(rows) + 1)
    bar = 6  # bracket width
    W = gridw + 2 * bar + 8
    canvas = Image.new("RGBA", (W, gridh), (0, 0, 0, 0))
    y = pady
    for r, row in enumerate(cells):
        x = bar + 8
        for c in range(ncol):
            if c < len(row):
                im = row[c]
                ox = x + (colw[c] - im.width) // 2
                oy = y + (rowh[r] - im.height) // 2
                canvas.alpha_composite(im, (ox, oy))
            x += colw[c] + padx
        y += rowh[r] + pady
    d = ImageDraw.Draw(canvas)
    lw = 2
    for bx0, tick in [(bar + 2, 1), (W - bar - 2, -1)]:
        d.line([(bx0, 1), (bx0, gridh - 2)], fill=(17, 17, 17, 255), width=lw)
        d.line([(bx0, 1), (bx0 + tick * 6, 1)], fill=(17, 17, 17, 255), width=lw)
        d.line([(bx0, gridh - 2), (bx0 + tick * 6, gridh - 2)], fill=(17, 17, 17, 255), width=lw)
    return canvas


def _compose_equation(tex, fontsize):
    """Compose a display equation containing bmatrix into ONE PIL->base64 image."""
    from PIL import Image
    toks, pos = [], 0
    for m in re.finditer(r"\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}", tex, re.DOTALL):
        pre = tex[pos:m.start()].strip()
        if pre:
            toks.append(_pil(pre, fontsize))
        body = [[c for c in row.split("&")] for row in re.split(r"\\\\", m.group(1)) if row.strip()]
        toks.append(_matrix_pil(body, fontsize - 1))
        pos = m.end()
    tail = tex[pos:].strip()
    if tail:
        toks.append(_pil(tail, fontsize))
    gap = 8
    H = max(im.height for im in toks)
    W = sum(im.width for im in toks) + gap * (len(toks) - 1)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x = 0
    for im in toks:
        canvas.alpha_composite(im, (x, (H - im.height) // 2))
        x += im.width + gap
    buf = BytesIO()
    canvas.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def render_math(md_src):
    """Replace $$...$$ and $...$ in markdown with rendered math.
    Pure mathtext where possible; bmatrix equations composed via PIL."""
    def render(tex, display):
        tex = _sanitize(tex)  # single-line + map unsupported commands
        if _can_parse(tex):
            return _img_tag(_math_png(tex, 16 if display else 12),
                            "math-display" if display else "math-inline")
        if "bmatrix" in tex:
            b64 = _compose_equation(tex, 18 if display else 13)
            return _img_tag(b64, "math-display" if display else "math-inline")
        return f"<code>{tex.strip()}</code>"
    md_src = re.sub(r"\$\$(.+?)\$\$",
                    lambda m: "\n\n" + render(m.group(1), True) + "\n\n",
                    md_src, flags=re.DOTALL)
    md_src = re.sub(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)",
                    lambda m: render(m.group(1), False), md_src)
    return md_src


def build():
    exporter = HTMLExporter(template_name="basic")
    exporter.exclude_input_prompt = True
    exporter.exclude_output_prompt = True
    ep = ExecutePreprocessor(timeout=240, kernel_name="python3")

    fragments = []
    for i, name in enumerate(NOTEBOOKS):
        print("processing", name)
        nb = nbformat.read(os.path.join(HERE, name), as_version=4)
        work = copy.deepcopy(nb)
        work.cells.insert(0, nbformat.v4.new_code_cell(SETUP_SRC))
        ep.preprocess(work, {"metadata": {"path": HERE}})
        # drop the injected setup cell so it doesn't show in the PDF
        work.cells.pop(0)
        # render LaTeX math to images (weasyprint cannot run MathJax)
        for c in work.cells:
            if c.cell_type == "markdown":
                c.source = render_math(c.source)
        body, _ = exporter.from_notebook_node(work)
        sep = "<div class='nb-sep'></div>" if i > 0 else ""
        fragments.append(sep + body)

    html = ("<!DOCTYPE html><html lang='he' dir='rtl'><head><meta charset='utf-8'>"
            "<style>" + CSS + "</style></head><body>" + "\n".join(fragments) +
            "</body></html>")
    tmp_html = os.path.join(HERE, "_combined.html")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html)
    HTML(string=html, base_url=HERE).write_pdf(OUT)
    os.remove(tmp_html)
    print("\nWROTE", OUT, "(%.1f KB)" % (os.path.getsize(OUT) / 1024))


if __name__ == "__main__":
    build()
