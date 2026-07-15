
# EDA

Exploratory data analysis for both research questions.
Author: Ruiping Huang.

## Notebook

**`TALIS_EDA_Final.ipynb`** — the complete exploratory analysis, runnable top to bottom.
Its sections cover:

- **Analytic samples** — construction of the RQ1 and RQ2 samples from the split-form design
  (the AI module was administered to approximately one third of teachers), with validity checks
  on the outcome items.
- **Outcome exploration** — AI-use rates across countries/regions and school levels; barriers to
  AI use among non-users; the definition and distribution of the student-facing (RQ2) outcome;
  country-level variation in student-facing use; and the AI-use-purposes heatmap by country.
- **Predictor selection** — a valid-response screen across the questionnaire, overlap refinement
  with the analytic samples, construction of the AI-belief composite scores, and the resulting
  set of 26 primary predictors proposed for the modeling stage.
- **Predictor–outcome correlations** — Spearman correlations of all 26 predictors with both
  outcomes, including the comparison figure used in the presentation.

## Inputs

| File | Location | Notes |
|---|---|---|
| `ttgintt4.csv` | `Data/CSV/` | raw OECD teacher file, semicolon-delimited (~616 MB); see `Data/README.md` for download options |
| `talis2024_teacher_codebook.csv` | `Data/` | tracked in the repository |

## Outputs

All tables and figures are written to `EDA/output/`, which is created automatically and is not
tracked in git; a full run regenerates it. Selected figures used in the main README are copied
to the repository-level `Figures/` folder.

## Running

Install the required packages from the repository root (`pip install -r requirements.txt`),
place the input files as indicated above, open the notebook, and select Run All. Path
resolution is automatic whether Jupyter is started from the repository root or from this folder.
