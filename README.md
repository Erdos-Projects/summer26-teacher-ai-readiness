# summer26-teacher-ai-readiness

**Predicting Teachers' Use of AI in Teaching**

An Erdos Institute Summer 2026 data-science group project. Using the TALIS 2024
teacher questionnaire, we build and interpret a model of how much teachers use
artificial intelligence in their teaching, and identify which teacher
characteristics and attitudes drive that use.

---

## Research questions

1. **Which factors best predict teachers' use of AI in teaching?**
2. **What are the most important predictors?**

The first asks whether AI use is predictable from teacher attitudes,
professional learning, and background. The second turns the model into an
answer — ranking predictors by importance so the result is interpretable, not
just a black-box score.

---

## Data


## Data

This project uses the OECD TALIS 2024 teacher and principal files.
The raw files are too large for GitHub. Two options:

1. **Download from source (OECD):** https://www.oecd.org/en/data/datasets/talis-2024-database.html
   Place the teacher (`*tgintt4.csv`) and principal (`*pgintt4.csv`) files in `Data/`,
   then run `Model_v5.ipynb` cell 0 to build `teacher_principal_named_columns.csv`.

2. **Prebuilt merged file (our copy):** [Google Drive link]
   Place in `Data/output/` and skip the build step.


[TALIS 2024](https://www.oecd.org/en/about/programmes/talis.html) (Teaching and
Learning International Survey, OECD), teacher questionnaire.

- **Combined teacher file `ttgintt4.csv`** — 278,383 teachers, 55 countries, all
  school levels (ISCED 1/2/3: primary, lower-secondary, upper-secondary).
- Semicolon-delimited (`sep=";"`), 630 columns, ~616 MB.
- **Raw data is not in the repo** (too large) — it is gitignored and kept
  locally. Processed outputs are regenerated from the cleaning pipeline.

---

## Outcome: `ai_use_score` (0–9)

Question 37 asks teachers whether they used AI for each of nine teaching
purposes (assessing work, planning lessons, summarising a topic, skill practice,
etc.). The outcome is the **count of "Yes" answers across those nine items** — a
0–9 measure of *how many ways* a teacher uses AI.

- **Gate (Q36):** "Used AI in the last 12 months?" Teachers who answer "No" get
  code 6 ("logically not applicable") on the nine items; codes 2 (No) and 6 both
  count as 0, so a non-user correctly scores 0.
- **Analysis sample:** the AI module was administered to a **random ~32% of
  teachers** in every country (split-form design), so the outcome is only
  defined for those **89,818 teachers (32.3%)**. Because the subsample is
  random, restricting to it does not bias the analysis.
- **Distribution:** mean **1.86**, median **0**, and **~59.7% of administered
  teachers score 0** → the outcome is strongly **zero-inflated**, which shapes
  the modeling choice below.

---

## Cleaning plan

Implemented in `notebooks/eda_combined.ipynb`; decisions recorded in
`reports/cleaning_eda_summary.md`.

1. **Select columns.** Read only the ~85 project columns (of 630) from the
   616 MB CSV via `usecols` for speed and memory.
2. **Rename.** Map cryptic TALIS codes to readable names via a data dictionary
   (`TT4G37A` → `aiuse_assess`, `TT4G35A` → `ai_benefit_*`, …).
3. **Recode missing/special codes to `NaN`.** Rule of thumb: keep only the valid
   codes listed in the codebook, everything else → `NaN`.
   - `6` logically N/A, `8` not administered, `9` omitted.
   - Q35 belief items also use `5` = "I don't know" → `NaN`.
   - Continuous vars use `998/999`; the survey weight `TCHWGT` uses `9998/9999`.
   - *Exception:* on the outcome items, code 6 maps to **0**, not `NaN`.
4. **Build the outcome** `ai_use_score` and define the analysis sample (teachers
   administered the AI module).
5. **Save** `data/processed/ttgintt4_clean.parquet` (all rows) and
   `ttgintt4_analysis_sample.parquet` (administered teachers only).

---

## Predictors

**Usable set (observed together with the outcome):**

- **AI professional learning received** — `ai_pl_received` (Q21G).
- **AI attitudes** — AI benefit beliefs and AI risk beliefs (Q35 A–J).
- **Demographics / derived** — age, teaching experience, education, employment
  status, contract type, qualification, teacher leadership, hours worked, etc.
  (Gender is usable but only ~39% covered — it is also split-form.)

> ### ⚠️ Flagged finding — the split questionnaire limits predictors
> TALIS 2024 rotates question blocks across questionnaire forms. The AI module
> (Q21G, Q35, Q36, Q37) sits on a **different form** from the digital-skills
> blocks, so several planned predictors are **~64% present overall but 0% present
> among AI-module teachers** and therefore **cannot be used as individual-level
> predictors** of AI use:
> **Q33** digital self-efficacy · **Q34** digital-tool beliefs · **Q52** digital
> teaching practices · **Q47** class composition · **Q24** AI PL-need.
> A school-/country-level aggregate workaround is possible but is a separate,
> more advanced design.

---

## Analysis & modeling plan

**1. EDA** (`notebooks/eda_combined.ipynb`, outputs in `results/eda/`): coverage
by country, missingness, the outcome distribution, AI use by purpose, group
means, and correlations with the outcome (Spearman). Preview signals:

- **AI professional learning received** is by far the strongest correlate
  (mean score 3.21 if received vs 0.98 if not).
- **AI benefit beliefs** are positively associated (ρ ≈ +0.26 to +0.38);
  demographic effects are weak.

**2. Modeling.** Because the outcome is a zero-inflated count, plain OLS is
biased by the spike at 0. We use a **two-part / hurdle approach**:

- **(a) "Any use"** — classify score > 0 vs 0.
- **(b) Intensity** — model how many uses among teachers who use AI at all
  (or fit a single zero-inflated / hurdle count model).

**3. Evaluation (KPIs).**

- Intensity: **RMSE / MAE** vs a mean/median baseline.
- "Any use": **accuracy / F1** vs a majority-class baseline.

**4. Interpretation (RQ2).** Read feature importances / coefficients to rank the
most important predictors.

**Caveats.**

- **Reverse causality** — AI beliefs and AI professional learning are tightly
  coupled to use; report predictors as *associated with*, not *causing*, AI use.
- **Survey weights** (`TCHWGT`) are cleaned but not yet applied; decide whether
  population-weighted estimates are needed for final figures.

---

## Repository structure

```
.
├── notebooks/
│   └── eda_combined.ipynb      # cleaning + EDA, runnable top-to-bottom
├── talis_clean/                # reusable cleaning code (Python package)
├── reports/
│   └── cleaning_eda_summary.md # team-facing cleaning & EDA summary
├── results/
│   └── eda/                    # figures and tables
├── data/
│   ├── raw/                    # local only — gitignored (too large)
│   └── processed/              # parquet outputs — gitignored, regenerate
├── tests/
├── requirements.txt
└── README.md
```

---

## Setup

```bash
# Python environment (course conda env or a fresh venv)
pip install -r requirements.txt

# Open the cleaning + EDA notebook
jupyter lab notebooks/eda_combined.ipynb   # Kernel ▸ Restart & Run All
```

Raw TALIS data is **not** included (gitignored). Place the TALIS 2024 teacher
CSV locally, point the notebook's data path at it, and run the notebook to
regenerate the processed parquet files and EDA outputs.
