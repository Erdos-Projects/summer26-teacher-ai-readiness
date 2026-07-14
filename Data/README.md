# Data

## In this folder (tracked in git)
- `talis2024_teacher_codebook.csv` — variable names, labels and missing codes.
  Required by the Model notebooks and the EDA; all notebooks read this exact filename.
- Small derived predictor CSVs from the feature-selection work.

## Not in git (too large)

Everything below is gitignored. Get it one of two ways.

### Option A — our Google Drive (fastest, has everything)
https://drive.google.com/drive/folders/1yukQZ_WQtgSw00vbXMJJwSFNGBVheNfd?usp=drive_link

The folder contains all the files this project needs:

| File | Put it in | Used by |
|---|---|---|
| `teacher_principal_named_columns.csv` (~1.6 GB) | `Data/output/` | Model notebooks 02-07 (skips the build step) |
| `ttgintt4.sav`, `tcgintt4.sav` | `Data/SPSS/` | `Model/01_build_dataset.ipynb` (only if rebuilding from raw) |
| `ttgintt4.csv` (semicolon-delimited, ~616 MB) | `Data/CSV/` | the EDA notebook |

If you just want to run the models: grab the merged 'teacher_principal_named_columns.csv' CSV, put it in `Data/output/`, done.

### Option B — download from OECD (the original source)
https://www.oecd.org/en/data/datasets/talis-2024-database.html#data

OECD asks you to fill a short registration form (name, institution, intended use)
before the download links work. Take **SPSS Teachers + Principals** (for the build)
and **CSV Teachers** (for the EDA), then place them as in the table above and run
`Model/01_build_dataset.ipynb` once to create the merged file.

## Layout after setup
```
Data/
├── talis2024_teacher_codebook.csv    # in git
├── SPSS/                             # ttgintt4.sav, tcgintt4.sav (not in git)
├── CSV/                              # ttgintt4.csv for the EDA (not in git)
└── output/                           # merged file + notebook outputs (not in git)
```
