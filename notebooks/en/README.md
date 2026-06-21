# FUSION Boot Camp 2026 — Notebook Series (English)

English version of the Jupyter notebooks documenting and demonstrating in code the developments
described in `FUSION Boot Camp 2026.pdf` (29th International Conference on Information Fusion,
Trondheim, Norway, June 2026).

The PDF itself contains two complete slide decks — the introduction by **Erik Blasch** and the
Estimation lecture by **W. Dale Blair** — plus the agenda of the seven Boot Camp lectures.

> The Hebrew version of this series lives in the parent directory (`../`).

## The notebooks

| Notebook | Topic | Source |
|----------|-------|--------|
| `00_overview.ipynb` | Overview, agenda, index | — |
| `01_introduction_to_information_fusion.ipynb` | Core concepts, history, JDL/DFIG (L0–L5), the Fusion equation, pros/cons | Blasch |
| `02_parameter_estimation.ipynb` | ML, MAP, MMSE, LSE/WLSE, Cramér–Rao bound, bias estimation | Blair (1) |
| `03_state_estimation_kalman_filter.ipynb` | Kalman filter derivation, predictor–corrector, process noise DWNA/CWNA, NCV model | Blair (2) |
| `04_target_tracking_maneuvering.ipynb` | NCV vs NCA, IMM, multiple sensors, EKF | Blair (3) |
| `05_data_association.ipynb` | Gating, GNN, PDA/JPDA, MHT | Meyer\* |
| `06_distributed_target_tracking.ipynb` | Information filter, track-to-track, Covariance Intersection | Govaers\* |
| `07_attributes_classification.ipynb` | Sequential Bayesian classification, confusion matrix, Dempster–Shafer | Bar-Shalom\* |
| `08_distributed_inference.ipynb` | ROC, k-out-of-N rules, Chair–Varshney | Varshney\* |
| `09_high_level_fusion.ipynb` | L2–L5, situation/threat assessment, MOP/MOE | Blasch (7)\* |

\* Lectures 3–7 (Data Association, Distributed Target Tracking, Attributes/Classification,
Distributed Inference, High-level Fusion) appear in the agenda but their slides are **not** included
in the PDF. Notebooks 05–09 are **companion notebooks** based on the canonical literature of the field,
not on original slides. Notebooks 01–04 are based directly on the two decks in the PDF.

## Running

```bash
pip install numpy matplotlib
jupyter notebook   # or: jupyter lab
```

Each notebook is self-contained and runs top-to-bottom (Run All). Plots are saved in the notebooks.

## Regeneration

```bash
for n in 00 01 02 03 04 05 06 07 08 09; do python3 _build_$n.py; done
```

(`_nbutil.py` holds shared helpers.)

## PDF export

`FUSION_Boot_Camp_2026_notebooks_EN.pdf` is a combined export of all ten notebooks. It is built by
`_make_pdf.py`, which executes the notebooks and renders to PDF via WeasyPrint. Because WeasyPrint
cannot run MathJax, LaTeX math is rendered to images (matrices composed via PIL).

```bash
pip install nbconvert weasyprint pymupdf
python3 _make_pdf.py
```
