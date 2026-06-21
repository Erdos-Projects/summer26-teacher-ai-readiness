"""Build v1: full cleaned + labeled TALIS 2024 teacher dataset (codebook-driven)."""
from pathlib import Path
import time, re
import pandas as pd

DATA_DIR = Path("/Users/ruipinghuang/Desktop/9 Data Science/1 Data/TALIS2024_teachers_NoESE_CSV")
CODEBOOK = Path("/Users/ruipinghuang/Desktop/9 Data Science/5 Codebook/talis2024_teacher_codebook.csv")
OUT      = Path("/Users/ruipinghuang/Desktop/9 Data Science/9 Lean by myself/06-20_clean_data/v1_ttgintt4_labeled.parquet")
data_path = DATA_DIR / "ttgintt4.csv"

cb = pd.read_csv(CODEBOOK).set_index("variable_name")

# Codes whose LABEL means "no usable answer" -> NaN. ("Logically not applicable" is kept.)
ADMIN = re.compile(r"not administered|omitted|invalid", re.I)

def na_codes(var):
    s = cb.loc[var, "all_value_labels"]; out = set()
    if pd.isna(s): return out
    for part in str(s).split("|"):
        m = re.match(r"\s*(\d+)\s*=\s*(.*)", part)
        if m and ADMIN.search(m.group(2)): out.add(int(m.group(1)))
    return out

def label_map(var):
    m = {}
    for col in ["valid_value_labels", "special_missing_or_skip_codes"]:
        s = cb.loc[var, col]
        if pd.isna(s): continue
        for part in str(s).split("|"):
            mt = re.match(r"\s*(\d+)\s*=\s*(.*?)\s*$", part)
            if mt and not ADMIN.search(mt.group(2)): m[int(mt.group(1))] = mt.group(2)
    return dict(sorted(m.items()))

t0 = time.time()
df = pd.read_csv(data_path, sep=";", low_memory=False)
print(f"loaded raw: {df.shape} in {time.time()-t0:.0f}s")

n_cat = n_num = n_skip = 0
for col in df.columns:
    if col not in cb.index:
        n_skip += 1; continue
    nac = na_codes(col)
    if nac:
        df[col] = df[col].where(~df[col].isin(nac))        # admin-missing -> NaN
    lm = label_map(col)
    if lm:                                                  # categorical -> ordered Categorical
        df[col] = df[col].astype("Int64").map(lm)
        df[col] = pd.Categorical(df[col], categories=list(lm.values()), ordered=True)
        n_cat += 1
    else:
        n_num += 1

print(f"categorical: {n_cat} | numeric/id: {n_num} | skipped(not in codebook): {n_skip}")
df.to_parquet(OUT, index=False)
mb = OUT.stat().st_size / 1e6
print(f"saved: {OUT.name}  shape={df.shape}  size={mb:.1f} MB  total {time.time()-t0:.0f}s")

# sanity checks
print("\nTT4G37A categories:", list(df['TT4G37A'].cat.categories))
print("TT4G35A categories:", list(df['TT4G35A'].cat.categories))
print("T4SELF dtype:", df['T4SELF'].dtype, "| range:", round(df['T4SELF'].min(),2), "-", round(df['T4SELF'].max(),2))
