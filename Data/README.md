# Data

## In this folder (tracked in git)
- `talis2024_teacher_codebook.csv` — variable names, labels and missing codes.
  Required by the Model notebooks and the EDA; all notebooks read this exact filename.
- Small derived predictor CSVs from the feature-selection work.

## Not in git (too large)

Everything below is gitignored. Get it one of two ways.

### Option A — download from OECD
Source: https://www.oecd.org/en/data/datasets/talis-2024-database.html#data

Note: OECD asks you to fill a short registration form (name, institution, intended use)
before the download links work. Free, takes a couple of minutes.

Which files to take:
- **SPSS, Teachers** and **SPSS, Principals** (compressed) — needed by
  `Model/01_build_dataset.ipynb`. Unzip and put `ttgintt4.sav` and `tcgintt4.sav`
  in `Data/SPSS/`.
- **CSV, Teachers** (compressed) — needed by the EDA notebook. Unzip and put
  `ttgintt4.csv` in `Data/CSV/`. It is semicolon-delimited (~616 MB).

Then run `Model/01_build_dataset.ipynb` once to build the merged file.

### Option B — prebuilt merged file (skips the OECD form and the build step)
Download `teacher_principal_named_columns.csv` (~1.6 GB) from our Google Drive: **[ADD LINK]**
Put it in `Data/output/`. This covers the Model notebooks (02-07); the EDA still
needs the CSV from Option A.

## Layout after setup
```
Data/
├── talis2024_teacher_codebook.csv    # in git
├── SPSS/                             # ttgintt4.sav, tcgintt4.sav (not in git)
├── CSV/                              # ttgintt4.csv for the EDA (not in git)
└── output/                           # merged file + notebook outputs (not in git)
```
