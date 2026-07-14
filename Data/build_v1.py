"""Build v1: full LABEL-FAITHFUL (lossless) TALIS 2024 teacher dataset, codebook-driven.

v1 replaces every numeric code with its text label and keeps ALL codes — including
'Not administered', 'Omitted or invalid', 'Logically not applicable', 'I don't know'.
Nothing is forced to NaN here; deciding what counts as missing is v2's job.
"""
from pathlib import Path
import time, re
import pandas as pd

DATA_DIR = Path("/Users/ruipinghuang/Desktop/9 Data Science/1 Data/TALIS2024_teachers_NoESE_CSV")
CODEBOOK = Path("/Users/ruipinghuang/Desktop/9 Data Science/5 Codebook/talis2024_teacher_codebook.csv")
OUT      = Path("/Users/ruipinghuang/Desktop/9 Data Science/9 Lean by myself/06-20_clean_data/v1_ttgintt4_labeled.parquet")
data_path = DATA_DIR / "ttgintt4.csv"

cb = pd.read_csv(CODEBOOK).set_index("variable_name")

def value_labels(var):
    """Full {code: label} for TRUE categorical variables, covering ALL codes
       (valid AND special/missing). Returns {} for continuous / id / weight columns
       (their only 'labels' are missing codes, and they hold decimals) so they stay raw.

       Categorical-ness is decided by `valid_value_labels` (real answer codes); the labels
       themselves come from `all_value_labels` so special codes (8/9/6/5) are kept too."""
    if pd.isna(cb.loc[var, "valid_value_labels"]):
        return {}                                        # continuous / id / weight -> leave raw
    s = cb.loc[var, "all_value_labels"]                  # categorical: EVERY code + its label
    m = {}
    for part in str(s).split("|"):                       # split "code = label" pieces
        mt = re.match(r"\s*(\d+)\s*=\s*(.*?)\s*$", part)  # group(1)=code, group(2)=label
        if mt:
            m[int(mt.group(1))] = mt.group(2)            # keep EVERY code, nothing dropped
    return dict(sorted(m.items()))                       # code order -> categories in order

# ANNOTATION ONLY: documents which codes mean "missing" so v2 knows what to NaN later.
# This is NOT applied in v1 — these codes are kept as their labels.
ADMIN = re.compile(r"not administered|omitted|invalid", re.I)
def missing_codes(var):
    return {c for c, lab in value_labels(var).items() if ADMIN.search(lab)}

t0 = time.time()
df = pd.read_csv(data_path, sep=";", low_memory=False)
print(f"loaded raw: {df.shape} in {time.time()-t0:.0f}s")

n_cat = n_num = 0
for col in df.columns:
    lm = value_labels(col)
    if lm:                                               # categorical: map EVERY code -> label
        df[col] = df[col].astype("Int64").map(lm)        # incl 'Not administered', etc.
        df[col] = pd.Categorical(df[col], categories=list(lm.values()), ordered=True)
        n_cat += 1
    else:                                                # continuous / id / weight: left RAW
        n_num += 1                                       # (no labels exist; untouched)

print(f"categorical (all codes labeled): {n_cat} | numeric/id (raw, untouched): {n_num}")
df.to_parquet(OUT, index=False)
mb = OUT.stat().st_size / 1e6
print(f"saved: {OUT.name}  shape={df.shape}  size={mb:.1f} MB  total {time.time()-t0:.0f}s")

# sanity: special codes are now KEPT as labels, not NaN
print("\nTT4G36  categories:", list(df['TT4G36'].cat.categories))
print("TT4G37A categories:", list(df['TT4G37A'].cat.categories))
print("'missing-type' codes flagged for v2 (annotation only):", missing_codes('TT4G37A'))
print("T4SELF (continuous, left raw) dtype:", df['T4SELF'].dtype,
      "| max still has 9999 code? max =", df['T4SELF'].max())
