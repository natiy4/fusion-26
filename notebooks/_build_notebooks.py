#!/usr/bin/env python3
"""Build notebook 00 (overview) of the FUSION Boot Camp 2026 series.

Run all generators with:  python3 _build_all.py
"""
from _nbutil import md, code, write_notebook

nb00 = [
    md(
        "# FUSION Boot Camp 2026 — סדרת מחברות הסבר",
        "",
        "**29th International Conference on Information Fusion**  ",
        "Trondheim, Norway · June 22–26, 2026  ",
        "מתאם: Dale Blair · מרצים: Blasch, Blair, Govaers, Meyer, Bar-Shalom, Varshney",
        "",
        "סדרת מחברות זו מתעדת ומדגימה בקוד את הפיתוחים (developments) שתוארו בקובץ ",
        "`FUSION Boot Camp 2026.pdf`. הקובץ עצמו מכיל שני מערכי שקופיות מלאים — המבוא של ",
        "Erik Blasch ושיעור האמידה (Estimation) של W. Dale Blair — וכן את לוח הזמנים של ",
        "שבע ההרצאות של ה-Boot Camp.",
    ),
    md(
        "## לוח הזמנים של ה-Boot Camp (22 ביוני 2026)",
        "",
        "| # | נושא | מרצה |",
        "|---|------|------|",
        "| 1 | Introduction to Information Fusion | Erik Blasch |",
        "| 2 | Estimation in Information Fusion | Dale Blair |",
        "| 3 | Data Association | Florian Meyer |",
        "| 4 | Distributed Target Tracking | Felix Govaers |",
        "| 5 | Fusion and Association with Attributes/Classification | Yaakov Bar-Shalom |",
        "| 6 | Distributed Inference and Information Fusion | Pramod Varshney |",
        "| 7 | High-level Fusion | Erik Blasch |",
    ),
    md(
        "## מבנה הסדרה",
        "",
        "| מחברת | תוכן | מבוסס על |",
        "|-------|------|----------|",
        "| `00_overview.ipynb` | סקירה כללית, לוח זמנים, אינדקס | — |",
        "| `01_introduction_to_information_fusion.ipynb` | מושגי יסוד, היסטוריה, מודל JDL/DFIG (רמות 0–5), משוואת ה-Fusion, יתרונות/חסרונות, היררכיית ההיסק | הרצאת Blasch |",
        "| `02_parameter_estimation.ipynb` | ML, MAP, MMSE, LSE, WLSE, חסם Cramér–Rao, אמידת הטיה (bias) | הרצאת Blair (חלק א') |",
        "| `03_state_estimation_kalman_filter.ipynb` | גזירת מסנן קלמן, predictor–corrector, רעש תהליך DWNA/CWNA, מודל NCV | הרצאת Blair (חלק ב') |",
        "| `04_target_tracking_maneuvering.ipynb` | NCV מול NCA, בחירת שונות רעש התהליך, IMM, EKF, ריבוי חיישנים | הרצאת Blair (חלק ג') |",
        "| `05_data_association.ipynb` | Gating, GNN, PDA/JPDA, MHT | הרצאת Meyer* |",
        "| `06_distributed_target_tracking.ipynb` | מסנן מידע, track-to-track, Covariance Intersection | הרצאת Govaers* |",
        "| `07_attributes_classification.ipynb` | סיווג בייסיאני רצוף, מטריצת בלבול, Dempster–Shafer | הרצאת Bar-Shalom* |",
        "| `08_distributed_inference.ipynb` | ROC, כללי k-out-of-N, Chair–Varshney | הרצאת Varshney* |",
        "| `09_high_level_fusion.ipynb` | רמות L2–L5, הערכת מצב/איום, MOP/MOE, hard+soft | הרצאת Blasch (7)* |",
        "",
        "**הערה (\\*):** ההרצאות 3–7 מופיעות בלוח הזמנים אך השקופיות שלהן **אינן** כלולות ב-PDF. ",
        "מחברות 05–09 הן **מחברות מלוות** המבוססות על הספרות הקנונית של התחום ",
        "(Bar-Shalom, Blackman & Popoli, Varshney, Blasch) ועל ההקשר שמספק Blasch במבוא — ",
        "ולא על שקופיות מקוריות. מחברות 01–04 מבוססות ישירות על שני המערכים שב-PDF.",
    ),
    md(
        "## דרישות הרצה",
        "",
        "```bash",
        "pip install numpy matplotlib",
        "```",
        "",
        "כל מחברת עצמאית וניתנת להרצה מתחילתה לסופה (Run All).",
    ),
    code(
        "# בדיקת סביבה",
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
