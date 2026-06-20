# FUSION Boot Camp 2026 — Notebook Series

מחברות Jupyter המתעדות ומדגימות בקוד את הפיתוחים שתוארו ב-`FUSION Boot Camp 2026.pdf`
(29th International Conference on Information Fusion, Trondheim, Norway, June 2026).

ה-PDF מכיל שני מערכי שקופיות מלאים — המבוא של **Erik Blasch** ושיעור האמידה של
**W. Dale Blair** — וכן את לוח הזמנים של שבע הרצאות ה-Boot Camp.

## המחברות

| מחברת | נושא | מקור |
|-------|------|------|
| `00_overview.ipynb` | סקירה, לוח זמנים, אינדקס | — |
| `01_introduction_to_information_fusion.ipynb` | מושגי יסוד, היסטוריה, JDL/DFIG (L0–L5), משוואת ה-Fusion, יתרונות/חסרונות | Blasch |
| `02_parameter_estimation.ipynb` | ML, MAP, MMSE, LSE/WLSE, חסם Cramér–Rao, אמידת הטיה | Blair (א') |
| `03_state_estimation_kalman_filter.ipynb` | גזירת מסנן קלמן, predictor–corrector, רעש תהליך DWNA/CWNA, מודל NCV | Blair (ב') |
| `04_target_tracking_maneuvering.ipynb` | NCV מול NCA, IMM, ריבוי חיישנים, EKF | Blair (ג') |

ההרצאות 3–7 (Data Association, Distributed Target Tracking, Attributes/Classification,
Distributed Inference, High-level Fusion) מופיעות בלוח הזמנים אך שקופיותיהן אינן כלולות ב-PDF.

## הרצה

```bash
pip install numpy matplotlib
jupyter notebook   # או: jupyter lab
```

כל מחברת עצמאית וניתנת להרצה מלאה (Run All). הפלטים (גרפים) שמורים במחברות.

## רגנרציה

המחברות נוצרות אוטומטית מסקריפטים:

```bash
python3 _build_notebooks.py   # 00
python3 _build_01.py          # 01
python3 _build_02.py          # 02
python3 _build_03.py          # 03
python3 _build_04.py          # 04
```

(`_nbutil.py` מכיל פונקציות עזר משותפות.)
