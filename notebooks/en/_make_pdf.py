#!/usr/bin/env python3
"""Build a single combined PDF from the English notebook series.

Reuses the LaTeX-math rendering helpers from the parent ../_make_pdf.py
(WeasyPrint cannot run MathJax, so math -> images; bmatrix composed via PIL),
but uses a left-to-right English layout and needs no Hebrew font / bidi.
"""
import copy
import importlib.util
import os

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "FUSION_Boot_Camp_2026_notebooks_EN.pdf")

# load the parent module to reuse its math-rendering helpers
_spec = importlib.util.spec_from_file_location("_mk_parent", os.path.join(PARENT, "_make_pdf.py"))
mk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mk)

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

CSS = """
@page { size: A4; margin: 1.6cm 1.4cm; }
body { font-family: 'DejaVu Sans',sans-serif; font-size: 10.5pt; line-height: 1.5; color: #1a1a1a; }
.jp-RenderedMarkdown table { margin: 0.4em 0; border-collapse: collapse; }
.jp-RenderedMarkdown th, .jp-RenderedMarkdown td { border: 1px solid #bbb; padding: 3px 7px; }
.jp-RenderedMarkdown h1 { font-size: 17pt; border-bottom: 2px solid #355; padding-bottom: 3px; color:#234; }
.jp-RenderedMarkdown h2 { font-size: 13.5pt; color:#345; margin-top: 0.8em; }
.jp-RenderedMarkdown h3 { font-size: 11.5pt; color:#456; }
.jp-InputArea pre, .highlight pre { background:#f5f5f5; border:1px solid #e0e0e0;
       border-radius:4px; padding:6px 9px; font-size:8.6pt; font-family:'DejaVu Sans Mono',monospace;
       white-space: pre-wrap; word-break: break-word; }
.jp-OutputArea pre { font-size:8.6pt; font-family:'DejaVu Sans Mono',monospace; white-space: pre-wrap; }
.jp-OutputArea img, img { max-width: 100%; height: auto; display:block; margin: 0.3em auto; }
.math-inline { vertical-align: middle; height: 1.05em; }
.math-display { display:block; margin: 0.6em auto; max-width:100%; max-height: 8.5em; }
.nb-sep { page-break-before: always; }
.jp-Cell { margin: 0.35em 0; }
.jp-InputPrompt, .jp-OutputPrompt { display:none; }
"""


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
        ep.preprocess(work, {"metadata": {"path": HERE}})
        for c in work.cells:
            if c.cell_type == "markdown":
                c.source = mk.render_math(c.source)
        body, _ = exporter.from_notebook_node(work)
        sep = "<div class='nb-sep'></div>" if i > 0 else ""
        fragments.append(sep + body)

    html = ("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
            "<style>" + CSS + "</style></head><body>" + "\n".join(fragments) +
            "</body></html>")
    HTML(string=html, base_url=HERE).write_pdf(OUT)
    print("\nWROTE", OUT, "(%.1f KB)" % (os.path.getsize(OUT) / 1024))


if __name__ == "__main__":
    build()
