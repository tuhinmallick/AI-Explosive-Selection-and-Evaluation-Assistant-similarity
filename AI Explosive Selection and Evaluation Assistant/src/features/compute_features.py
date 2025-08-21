import numpy as np, pandas as pd
def safe_norm(s: pd.Series) -> pd.Series:
    s = s.fillna(0); rng = s.max() - s.min()
    return (s - s.min()) / rng if rng != 0 else s*0
def build_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out['engagement_7'] = (out['likes_7'].fillna(0)*1.0 + out['comments_7'].fillna(0)*3.0 + out['shares_7'].fillna(0)*4.0)
    out['engagement_density'] = out['engagement_7'] / (out['views_7'].replace(0, np.nan))
    out['engagement_density'] = out['engagement_density'].fillna(0)
    out['rank_score'] = 1 - safe_norm(out['sales_rank_7'].replace(0, np.nan))
    out['review_score'] = safe_norm(out['reviews']); out['rating_score'] = safe_norm(out['rating'])
    out['growth_7_norm'] = safe_norm(out['growth_7']); out['growth_30_norm'] = safe_norm(out['growth_30'])
    price = out['price'].clip(lower=1, upper=200)
    out['price_centered'] = 1 - np.abs((price - price.median())/(price.mad()+1e-6)); out['price_centered'] = out['price_centered'].clip(0,1)
    out['f_social'] = safe_norm(out['engagement_density']) + safe_norm(out['engagement_7'])
    maxv = out['f_social'].replace(0, np.nan).max(); out['f_social'] = out['f_social']/maxv if maxv and maxv>0 else out['f_social']
    out['f_commerce'] = (out['rank_score']*0.6 + out['review_score']*0.2 + out['rating_score']*0.2).fillna(0)
    out['f_growth'] = (out['growth_7_norm']*0.4 + out['growth_30_norm']*0.6).fillna(0)
    out['f_price'] = out['price_centered'].fillna(0); return out
