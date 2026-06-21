# v1 — Full Cleaned & Labeled TALIS 2024 Teacher Dataset

**Contributor:** Ruiping · **Created:** 2026-06-21
**File:** `v1_ttgintt4_labeled.parquet` · **Shape:** 278,383 teachers × 630 variables (all ISCED levels, 55 countries)

This is the **canonical cleaned + labeled** version of the combined TALIS 2024 teacher file — the shared, human-readable base layer for the team. It is *faithful to the survey*: it applies only mechanical cleaning + value labels, **not** any analysis/modeling decisions (those live in each member's `v2`).

---

## Data source & license (please read before sharing)
- **Source:** OECD — *Teaching and Learning International Survey (TALIS) 2024*, teacher public-use file (`ttgintt4.csv`, combined file). Downloaded from the [OECD TALIS 2024 Database](https://www.oecd.org/en/data/datasets/talis-2024-database.html).
- **This is a *derived* (cleaned) copy**, not the original distribution.
- **License:** the OECD default is **Creative Commons Attribution 4.0 (CC BY 4.0)**, which permits sharing and adaptation **with attribution** — but TALIS-specific terms should be confirmed against the OECD "Terms and Conditions" on the download page before public redistribution.
- **Required attribution / citation:** *OECD (2025), TALIS 2024 Database, OECD, Paris.* Always cite the OECD as the data source.

---

## How v1 was cleaned (codebook-driven)
Every rule comes from `5 Codebook/talis2024_teacher_codebook.csv`, applied to **all 630 columns**:

1. **Admin-missing → NaN.** Codes whose label means *"Not administered" / "Omitted" / "Invalid"* (8, 9, 9998/9999, 999998/999999, …) become `NaN`.
2. **Meaningful non-answers are kept and labeled** — `6 = Logically not applicable` and `5 = I don't know` are *preserved as categories*, because they are informative responses, not missing data.
3. **Categorical variables (458) → ordered `Categorical`** with their text labels (e.g. `Strongly disagree < … < Strongly agree`). Original numeric codes are recoverable via `.cat.codes`.
4. **Continuous scales / weights / identifiers (172) stay numeric** (only their missing codes are set to `NaN`).
5. **Original TALIS variable names are kept** (`TT4G35A`, `T4SELF`, …) as the shared key. Use `5 Codebook/` or `variable_reference.md` for human-readable meanings.

### Known caveats (intentional, resolved downstream in v2)
- The `ordered=True` flag is correct for Likert/frequency scales but **arbitrary for nominal variables** (gender, country) — order there is meaningless.
- `Q35 "I don't know"` sits as the top-ranked category (code 5 > 4); it is **not** a true scale point. Each `v2` recodes it to `NaN` for modeling.
- v1 does **not** build the outcome. `AI_USE_SCORE` is built in `v2` from the preserved `Q37` items (treating `6 = Logically not applicable` as a real 0).

---

## How to regenerate (no committed data needed)
The pipeline is fully reproducible from the raw file + codebook:

```bash
conda activate erdos_ds_environment
jupyter lab build_v1.ipynb      # run all cells  (or: python build_v1.py)
```

Set the two paths at the top (`DATA_DIR`, `CODEBOOK`) to your local copies of the TALIS raw data and codebook. Output: `v1_ttgintt4_labeled.parquet`.

---

## Files in this folder
| File | What it is |
|---|---|
| `build_v1.ipynb` | Annotated notebook that builds v1 from the raw data (the pipeline). |
| `build_v1.py` | Script version of the same pipeline. |
| `README.md` | This file. |
| `v1_ttgintt4_labeled.parquet` | The cleaned + labeled dataset (≈108 MB) — **not committed to the repo** (over GitHub's 100 MB limit + keeps redistribution clean). Regenerate it with the notebook, or get the prebuilt copy from the team's shared drive. |
