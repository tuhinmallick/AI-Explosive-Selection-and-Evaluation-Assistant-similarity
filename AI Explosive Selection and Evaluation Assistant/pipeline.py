from __future__ import annotations
import argparse, os
from typing import List
from src.ingest.loader import load_sample
from src.features.compute_features import build_features
from src.models.scorer import compute_hotscore
from src.utils.common import Paths, ensure_dirs

BEAUTY_HASHTAGS_DEFAULT = ["skincare","sunscreen","retinol","lipstick","makeup","mascara","eyeliner","eyeshadow","foundation","concealer","blush","primer","serum","niacinamide","vitaminC","toner","cleanser","moisturizer","sunscreenstick","spf50","haircare","hairmask","dryshampoo","fragrance"]
def run_pipeline(source: str = "sample", hashtags: List[str] | None = None, top_k: int = 30):
    ensure_dirs()
    if source == "sample":
        raw = load_sample()
    elif source == "apify":
        from src.connectors.tiktok_apify import fetch_tiktok_by_hashtags
        if not hashtags: hashtags = BEAUTY_HASHTAGS_DEFAULT
        raw = fetch_tiktok_by_hashtags(hashtags)
        def tag_to_beauty(title: str) -> str:
            t=(title or "").lower(); keys = set(BEAUTY_HASHTAGS_DEFAULT + ["beauty"])
            return "Beauty" if any(k in t for k in keys) else "Other"
        raw["category"] = raw["title"].apply(tag_to_beauty)
        if "price" not in raw or raw["price"].isna().all(): raw["price"]=19.99
        raw["brand"]=raw.get("brand","NoBrand"); raw["currency"]=raw.get("currency","USD")
    else:
        raise RuntimeError(f"Unknown source: {source}")
    feat = build_features(raw); scored = compute_hotscore(feat)
    out_path = os.path.join(Paths.REPORTS, "hotscore_top.csv")
    scored[['rank','platform','title','category','brand','price','HotScore_norm','growth_7','growth_30','reviews','rating','url']].head(top_k).to_csv(out_path, index=False)
    brief_path = os.path.join(Paths.REPORTS, "briefing.md")
    with open(brief_path, 'w', encoding='utf-8') as f:
        f.write("# Product Research AI 选品简报\n\n")
        f.write("**Top 候选（前 %d 条）**\n\n" % top_k)
        for _, r in scored.head(top_k).iterrows():
            f.write(f"- [{int(r['rank']):>02}] ({r['platform']}) {r['title']} | ${float(r['price']):.2f} | HotScore={float(r['HotScore_norm']):.3f} | ↑7d={float(r.get('growth_7') or 0):.2f}\n")
        f.write("\n> 数据源：%s\n" % source)
    print(f"已生成：{out_path} 和 {brief_path}")
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--use-sample", action="store_true")
    parser.add_argument("--source", type=str, default="sample", choices=["sample","apify"])
    parser.add_argument("--hashtags", nargs="*", default=None)
    parser.add_argument("--top-k", type=int, default=30)
    args = parser.parse_args()
    if args.use_sample: run_pipeline(source="sample", top_k=args.top_k)
    else: run_pipeline(source=args.source, hashtags=args.hashtags, top_k=args.top_k)
