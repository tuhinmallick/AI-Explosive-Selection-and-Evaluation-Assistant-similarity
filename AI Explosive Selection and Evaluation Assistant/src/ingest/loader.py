from __future__ import annotations
import os, pandas as pd
from ..utils.common import Paths, ensure_dirs
def load_sample() -> pd.DataFrame:
    ensure_dirs()
    f = os.path.join(Paths.DATA, "sample_tiktok_amazon_etsy.csv")
    df = pd.read_csv(f)
    for col in ["price","views_7","likes_7","comments_7","shares_7","sales_rank_7","reviews","rating","growth_7","growth_30"]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df
