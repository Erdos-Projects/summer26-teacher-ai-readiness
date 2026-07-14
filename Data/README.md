# Data

## Files included in this repository
- `talis2024_teacher_codebook.csv` — variable names, labels, and special missing codes.
  Required by both the Model notebooks and the EDA notebook; all notebooks reference this
  exact filename.
- Small derived CSV files documenting the feature-selection process.

## Files not included in this repository
The raw TALIS 2024 data files and the merged analysis file exceed GitHub's file-size limits
and are therefore excluded from version control. They can be obtained in either of the
following ways.

### Option A — Project Google Drive (recommended; contains all required files)
https://drive.google.com/drive/folders/1yukQZ_WQtgSw00vbXMJJwSFNGBVheNfd?usp=drive_link

| File | Destination | Used by |
|---|---|---|
| `ttgintt4.sav`, `tcgintt4.sav` (raw teacher and principal files, SPSS format) | `Data/SPSS/` | `Model/01_build_dataset.ipynb`, which constructs the merged file below |
| `teacher_principal_named_columns.csv` (~1.6 GB; built from the SPSS files) | `Data/output/` | Model notebooks 02–07 |
| `ttgintt4.csv` (raw teacher file, OECD CSV export; semicolon-delimited, ~616 MB) | `Data/CSV/` | the EDA notebook |

To reproduce the modeling results only, it is sufficient to download
`teacher_principal_named_columns.csv` and place it in `Data/output/`; the build step
(notebook 01) may then be skipped.

### Option B — OECD (original source)
https://www.oecd.org/en/data/datasets/talis-2024-database.html#data

The OECD requires completion of a brief registration form (name, institution, intended use)
before the download links become available. Download the **SPSS Teachers** and
**SPSS Principals** files (for the dataset build) and the **CSV Teachers** file (for the EDA),
place them as indicated in the table above, and run `Model/01_build_dataset.ipynb` once to
construct the merged analysis file.

## Expected directory layout after setup
```
Data/
├── talis2024_teacher_codebook.csv    # tracked in git
├── SPSS/                             # ttgintt4.sav, tcgintt4.sav (not in git)
├── CSV/                              # ttgintt4.csv for the EDA (not in git)
└── output/                           # merged file and notebook outputs (not in git)
```
