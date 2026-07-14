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

## How v1 was built (codebook-driven, label-faithful / lossless)
v1 replaces numeric codes with their text labels but **does not decide what is "missing"** —
it keeps every code. All rules read from `5 Codebook/talis2024_teacher_codebook.csv`:

1. **Every code → its label; nothing forced to `NaN`.** For categorical variables, *all* codes are
   replaced by their codebook labels and kept as categories — **including** the special codes
   `8 = Not administered`, `9 = Omitted or invalid`, `6 = Logically not applicable`, and
   `5 = I don't know`. They are kept, not dropped, so v1 stays faithful to the survey.
2. **Categorical variables (458) → ordered `Categorical`** with their text labels. Categories are in
   code order, so the special/missing labels sit at the end of the order.
3. **Continuous scales / weights / identifiers (172) are left exactly as the raw file** (numeric,
   untouched) — including their `9998/9999`-type codes, since they have no text labels to apply.
4. **Original TALIS variable names are kept** (`TT4G35A`, `T4SELF`, …) as the shared key. Use
   `5 Codebook/` or `variable_reference.md` for human-readable meanings.

### Which codes mean "missing" — handled in v2, not v1
The codebook column `special_missing_or_skip_codes` lists, per variable, the codes that mean
*not administered / omitted / invalid*. v1 keeps them visible as labels; **v2** is where you decide
which become `NaN`, drop `Q35 = 5 "I don't know"`, and build `AI_USE_SCORE` from the `Q37` items
(treating `6 = Logically not applicable` as a real 0).

### Known caveats (intentional)
- `ordered=True` is meaningful for the Likert/frequency scales, but **arbitrary for nominal variables**
  (gender, country) and for the special-code categories (`Not administered`, etc.) that now sit at the
  top of the order. Treat the ordering as meaningful only among the substantive response codes.
- **Continuous columns still contain their raw `9998/9999` codes** — do not compute statistics on them
  in v1 without recoding those to `NaN` first (that's a v2 step).

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
