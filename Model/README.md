# Model

Modeling notebooks for both research questions.
Author: Elif Yegenoglu.

## Notebooks

**`01_build_dataset.ipynb`** — merges the raw TALIS SPSS files into a single analysis file,
`Data/output/teacher_principal_named_columns.csv` (~1.6 GB). This step is slow and needs to be
run only once. It may be skipped entirely if the merged file has already been downloaded
(see `Data/README.md`).

**`02_model.ipynb`** — constructs the analysis samples for both research questions, performs the
school-grouped train/test split, builds the nested feature tiers, compares model families, and
fits the Part 2 (student-facing use) model.

**`03_results.ipynb`** — produces the results reported in the presentation: feature importance,
parsimony curves, calibration, ROC and precision–recall curves, within-country AUCs, confusion
matrices, and the odds-ratio forest plots. Figures are saved to `Data/output/`.

**`04_robustness.ipynb`** — robustness checks: null-target shuffles, seed stability for both
parts, sensitivity of the Part 2 outcome definition (items D/E), train/test feature balance,
and the standardized-mean-difference check.

**`05_school_block_check.ipynb`** — documents why the 19 school-context variables were excluded
from the final model: they provide almost no AUC gain, while requiring complete school data
reduces the sample unevenly across countries.

**`06_weight_sensitivity.ipynb`** — compares TCHWGT-weighted and unweighted adoption rates by
ISCED level. Fast; loads only the three columns it requires.

**`07_experiments.ipynb`** — re-runs the experiments that shaped the final model: trivial
baselines, models with and without the belief composites, individual belief items versus the
composites, alternative Part 2 outcome definitions, a weighted refit, and hyperparameter tuning.

## Running the notebooks

Run notebook 01 once (or place the downloaded merged file in `Data/output/`), after which
notebooks 02–07 may be run in any order. Each notebook is self-contained: notebooks 03, 04, 05,
and 07 begin with setup cells copied from notebook 02, so any change to the pipeline in 02 must
also be propagated to those copies.

Install the required packages first, from the repository root:

```
pip install -r requirements.txt
```

Path resolution is automatic: the notebooks locate the repository whether Jupyter is started
from the repository root or from this folder.
