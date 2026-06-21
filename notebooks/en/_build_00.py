#!/usr/bin/env python3
"""Notebook 00 (English) - overview of the FUSION Boot Camp 2026 series."""
from _nbutil import md, code, write_notebook

nb00 = [
    md(
        "# FUSION Boot Camp 2026 — Explanatory Notebook Series",
        "",
        "**29th International Conference on Information Fusion**  ",
        "Trondheim, Norway · June 22–26, 2026  ",
        "Coordinator: Dale Blair · Instructors: Blasch, Blair, Govaers, Meyer, Bar-Shalom, Varshney",
        "",
        "This notebook series documents and demonstrates in code the developments described in ",
        "`FUSION Boot Camp 2026.pdf`. The PDF itself contains two complete slide decks — the ",
        "introduction by Erik Blasch and the Estimation lecture by W. Dale Blair — together with ",
        "the agenda of the seven Boot Camp lectures.",
    ),
    md(
        "## Boot Camp agenda (22 June 2026)",
        "",
        "| # | Topic | Instructor |",
        "|---|-------|------------|",
        "| 1 | Introduction to Information Fusion | Erik Blasch |",
        "| 2 | Estimation in Information Fusion | Dale Blair |",
        "| 3 | Data Association | Florian Meyer |",
        "| 4 | Distributed Target Tracking | Felix Govaers |",
        "| 5 | Fusion and Association with Attributes/Classification | Yaakov Bar-Shalom |",
        "| 6 | Distributed Inference and Information Fusion | Pramod Varshney |",
        "| 7 | High-level Fusion | Erik Blasch |",
    ),
    md(
        "## Series structure",
        "",
        "| Notebook | Content | Based on |",
        "|----------|---------|----------|",
        "| `00_overview.ipynb` | Overview, agenda, index | — |",
        "| `01_introduction_to_information_fusion.ipynb` | Core concepts, history, JDL/DFIG model (levels 0–5), the Fusion equation, pros/cons, inference hierarchy | Blasch lecture |",
        "| `02_parameter_estimation.ipynb` | ML, MAP, MMSE, LSE, WLSE, Cramér–Rao bound, bias estimation | Blair lecture (part 1) |",
        "| `03_state_estimation_kalman_filter.ipynb` | Kalman filter derivation, predictor–corrector, process noise DWNA/CWNA, NCV model | Blair lecture (part 2) |",
        "| `04_target_tracking_maneuvering.ipynb` | NCV vs NCA, process-noise tuning, IMM, EKF, multiple sensors | Blair lecture (part 3) |",
        "| `05_data_association.ipynb` | Gating, GNN, PDA/JPDA, MHT | Meyer lecture* |",
        "| `06_distributed_target_tracking.ipynb` | Information filter, track-to-track, Covariance Intersection | Govaers lecture* |",
        "| `07_attributes_classification.ipynb` | Sequential Bayesian classification, confusion matrix, Dempster–Shafer | Bar-Shalom lecture* |",
        "| `08_distributed_inference.ipynb` | ROC, k-out-of-N rules, Chair–Varshney | Varshney lecture* |",
        "| `09_high_level_fusion.ipynb` | Levels L2–L5, situation/threat assessment, MOP/MOE, hard+soft | Blasch lecture (7)* |",
        "",
        "**Note (\\*):** Lectures 3–7 appear in the agenda but their slides are **not** included in the PDF. ",
        "Notebooks 05–09 are **companion notebooks** based on the canonical literature of the field ",
        "(Bar-Shalom, Blackman & Popoli, Varshney, Blasch) and on the context Blasch provides in the ",
        "introduction — not on original slides. Notebooks 01–04 are based directly on the two decks in the PDF.",
    ),
    md(
        "## Requirements",
        "",
        "```bash",
        "pip install numpy matplotlib",
        "```",
        "",
        "Each notebook is self-contained and runs top-to-bottom (Run All).",
    ),
    code(
        "# Environment check",
        "import sys",
        "import numpy as np",
        "import matplotlib",
        "print('Python', sys.version.split()[0])",
        "print('numpy', np.__version__)",
        "print('matplotlib', matplotlib.__version__)",
    ),
]

if __name__ == "__main__":
    write_notebook("00_overview.ipynb", nb00)
