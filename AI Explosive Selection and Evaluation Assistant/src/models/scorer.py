import pandas as pd
DEFAULT_WEIGHTS = {"social":0.45,"commerce":0.30,"growth":0.20,"price":0.05}
def compute_hotscore(feat_df: pd.DataFrame, weights: dict | None = None) -> pd.DataFrame:
    w = {**DEFAULT_WEIGHTS, **(weights or {})}; df = feat_df.copy()
    df['HotScore'] = df['f_social'].fillna(0)*w['social'] + df['f_commerce'].fillna(0)*w['commerce'] + df['f_growth'].fillna(0)*w['growth'] + df['f_price'].fillna(0)*w['price']
    df['HotScore_norm'] = df.groupby('platform')['HotScore'].transform(lambda s: (s - s.min())/(s.max()-s.min()) if s.max()!=s.min() else 0)
    df = df.sort_values(['HotScore_norm'], ascending=False); df['rank'] = range(1, len(df)+1); df['is_candidate'] = (df['HotScore_norm']>=0.75).astype(int); return df
