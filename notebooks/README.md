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
| `05_data_association.ipynb` | Gating, GNN, PDA/JPDA, MHT | Meyer\* |
| `06_distributed_target_tracking.ipynb` | מסנן מידע, track-to-track, Covariance Intersection | Govaers\* |
| `07_attributes_classification.ipynb` | סיווג בייסיאני, מטריצת בלבול, Dempster–Shafer | Bar-Shalom\* |
| `08_distributed_inference.ipynb` | ROC, k-out-of-N, Chair–Varshney | Varshney\* |
| `09_high_level_fusion.ipynb` | L2–L5, הערכת מצב/איום, MOP/MOE | Blasch (7)\* |

\* ההרצאות 3–7 (Data Association, Distributed Target Tracking, Attributes/Classification,
Distributed Inference, High-level Fusion) מופיעות בלוח הזמנים אך שקופיותיהן **אינן** כלולות ב-PDF.
מחברות 05–09 הן **מחברות מלוות** המבוססות על הספרות הקנונית בתחום, לא על שקופיות מקוריות.

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
for n in 01 02 03 04 05 06 07 08 09; do python3 _build_$n.py; done
```

(`_nbutil.py` מכיל פונקציות עזר משותפות.)

## ייצוא ל-PDF

`FUSION_Boot_Camp_2026_notebooks.pdf` הוא ייצוא משולב של כל עשר המחברות (50 עמ').
הוא נבנה ע"י `_make_pdf.py`, שמריץ את המחברות וממיר ל-PDF עם תמיכה מלאה בעברית:

```bash
pip install nbconvert weasyprint python-bidi pymupdf
# נדרש פונט עברי (למשל Noto Sans Hebrew) מותקן במערכת
python3 _make_pdf.py
```

הסקריפט מטפל ב: כיוון RTL לטקסט עברי (LTR לקוד), סידור עברית נכון בגרפים (bidi),
ורינדור נוסחאות LaTeX לתמונות (כולל מטריצות) — כיוון ש-WeasyPrint אינו מריץ MathJax.
