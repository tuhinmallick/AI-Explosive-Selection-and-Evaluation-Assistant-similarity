from __future__ import annotations
import os, time, requests, pandas as pd
APIFY_ACTOR = "clockworks/tiktok-scraper"
def fetch_tiktok_by_hashtags(hashtags: list[str]) -> pd.DataFrame:
    token = os.getenv("APIFY_TOKEN")
    if not token: raise RuntimeError("缺少 APIFY_TOKEN 环境变量")
    results = []
    for tag in hashtags:
        payload = {"hashtags":[tag],"resultsLimit":50}
        r = requests.post(f"https://api.apify.com/v2/acts/{APIFY_ACTOR}/runs",
                          headers={"Authorization": f"Bearer {token}"}, json=payload, timeout=60)
        r.raise_for_status(); run_id = r.json()["data"]["id"]
        dataset_id = None
        while True:
            s = requests.get(f"https://api.apify.com/v2/actor-runs/{run_id}",
                             headers={"Authorization": f"Bearer {token}"}, timeout=60).json()
            if s["data"]["status"] in ("SUCCEEDED","FAILED","TIMED-OUT"):
                dataset_id = s["data"].get("defaultDatasetId"); break
            time.sleep(2)
        if dataset_id:
            items = requests.get(f"https://api.apify.com/v2/datasets/{dataset_id}/items",
                                 headers={"Authorization": f"Bearer {token}"}, timeout=60).json()
            for it in items:
                results.append({"platform":"tiktok","product_id":it.get("id"),"title":it.get("text"),"category":None,"brand":None,"price":None,"currency":"USD","date":it.get("createTime"),"views_7":it.get("playCount"),"likes_7":it.get("diggCount"),"comments_7":it.get("commentCount"),"shares_7":it.get("shareCount"),"sales_rank_7":None,"reviews":None,"rating":None,"growth_7":None,"growth_30":None,"url":it.get("webVideoUrl") or it.get("shareUrl")})
    return pd.DataFrame(results)
