
Model

Modeling notebooks for both research questions. Elif Yegenoglu.

Notebooks

01_build_dataset.ipynb — merges the raw TALIS .sav files into one CSV
(Data/output/teacher_principal_named_columns.csv, ~1.6GB). Slow, run once.
Skip it if you downloaded the merged file already (see Data/README.md).

02_model.ipynb — analysis samples for both parts, school-grouped split,
nested feature tiers, model comparison, Part 2 model.

03_results.ipynb — features importance, parsimony, calibration, ROC/PR, within-country AUCs,
confusion matrices, odds ratio forest plots. Figures save to Data/output/.

04_robustness.ipynb — null-target shuffles, seed stability for both
parts, D/E outcome sensitivity, train/test balance, SMD check.

05_school_block_check.ipynb — why the 19 school-context variables were
dropped: almost no AUC gain, and requiring complete school data costs rows
unevenly across countries.

06_weight_sensitivity.ipynb — TCHWGT weighted vs unweighted adoption
rates by ISCED level. Quick, only loads 3 columns.

07_experiments.ipynb — reruns the experiments that shaped the model
(baselines, beliefs in/out, individual items vs composites, alternative
Part 2 outcomes, weighted refit, tuning).


Running

Run 01 once (or place the downloaded merged file in Data/output/), then any
of 02-07 in any order. Each notebook is standalone: 03, 04, 05 and 07 start
with setup cells copied from 02, so if the pipeline in 02 changes those
copies need updating too.

Install packages first: pip install -r requirements.txt from the repo root.
Notebooks find their paths whether Jupyter starts from the repo root or from
this folder.
