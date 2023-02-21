from pathlib import Path

import pandas as pd

all = ["read_table"]


def read_table(file, dtype=str) -> pd.DataFrame:
    if isinstance(file, Path) and file.suffix == ".xlsx":
        return pd.read_excel(file, dtype=dtype)
    else:
        return pd.read_csv(file, dtype=dtype)
