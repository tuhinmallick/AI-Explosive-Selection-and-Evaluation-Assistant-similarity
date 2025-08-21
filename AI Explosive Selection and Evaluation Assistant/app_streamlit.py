import os, streamlit as st, pandas as pd
from src.ingest.loader import load_sample
from src.features.compute_features import build_features
from src.models.scorer import compute_hotscore

st.set_page_config(page_title="Product Research AI", layout="wide")
st.title("📈 Product Research AI · 爆品选品助手"); st.caption("演示数据 · 支持接入 TikTok / Amazon / Etsy 实时数据")

# 订阅栏：三档价格 + 文案
st.sidebar.subheader("💳 订阅")
SUBSCRIBE_URL_M = os.getenv("SUBSCRIPTION_URL", "")
SUBSCRIBE_URL_Q = os.getenv("SUBSCRIPTION_URL_Q", "")
SUBSCRIBE_URL_Y = os.getenv("SUBSCRIPTION_URL_Y", "")
pricing = {"月付": "9.9", "季付": "24.9", "年付": "79.9"}
cols = st.sidebar.columns(3)
if SUBSCRIBE_URL_M: cols[0].markdown(f"[月付 ${pricing['月付']}]({SUBSCRIBE_URL_M})")
else: cols[0].button(f"月付 ${pricing['月付']}")
if SUBSCRIBE_URL_Q: cols[1].markdown(f"[季付 ${pricing['季付']}]({SUBSCRIBE_URL_Q})")
else: cols[1].button(f"季付 ${pricing['季付']}")
if SUBSCRIBE_URL_Y: cols[2].markdown(f"[年付 ${pricing['年付']}]({SUBSCRIBE_URL_Y})")
else: cols[2].button(f"年付 ${pricing['年付']}")
st.sidebar.caption("设置 SUBSCRIPTION_URL / SUBSCRIPTION_URL_Q / SUBSCRIPTION_URL_Y 即可跳转到 Stripe")

# 附加文案（可由环境变量自定义）
REFUND = os.getenv('SUBSCRIPTION_REFUND', '首次下单 7 天内不满意可全额退款')
SCHEDULE = os.getenv('SUBSCRIPTION_SCHEDULE', '每周一 / 周四 20:00（本地时区）更新')
SUPPORT = os.getenv('SUPPORT_EMAIL', '')
st.sidebar.markdown(f"**退款承诺：** {REFUND}")
st.sidebar.markdown(f"**更新时间：** {SCHEDULE}")
if SUPPORT: st.sidebar.caption(f"支持邮箱：{SUPPORT}")
else: st.sidebar.caption('可设置 SUPPORT_EMAIL 展示联系邮箱')

@st.cache_data
def get_scored():
    raw=load_sample(); feat=build_features(raw); return compute_hotscore(feat)
df=get_scored()

left, right = st.columns([1,3])
with left:
    plats = st.multiselect("平台", options=sorted(df['platform'].unique()), default=sorted(df['platform'].unique()))
    cats = st.multiselect("类目", options=sorted(df['category'].dropna().unique()), default=None)
    price_max=float(df['price'].max())
    price_range = st.slider("价格区间 ($)", 0.0, float(max(100.0, price_max)), (0.0, float(max(50.0, price_max))))
    topk = st.number_input("显示前 N 条", min_value=5, max_value=100, value=30, step=5)
mask = df['platform'].isin(plats)
if 'cats' in locals() and cats: mask &= df['category'].isin(cats)
mask &= (df['price']>=price_range[0]) & (df['price']<=price_range[1])
view = df[mask].sort_values('HotScore_norm', ascending=False).head(int(topk))

with right:
    st.subheader("候选爆品 (按 HotScore 排序)")
    st.dataframe(view[['rank','platform','title','category','brand','price','HotScore_norm','growth_7','growth_30','reviews','rating','url']])

st.divider(); st.subheader("🧠 打分解释（权重见 src/models/scorer.py）")
explain = df[['f_social','f_commerce','f_growth','f_price']].describe().T
st.dataframe(explain)

st.divider(); st.subheader("📤 导出报告")
if st.button("导出 CSV & 简报到 reports/ "):
    view[['rank','platform','title','category','brand','price','HotScore_norm','growth_7','growth_30','reviews','rating','url']].to_csv("reports/hotscore_top.csv", index=False)
    with open("reports/briefing.md","w",encoding="utf-8") as f:
        for _, r in view.iterrows():
            f.write(f"- [{int(r['rank']):>02}] ({r['platform']}) {r['title']} | ${float(r['price']):.2f} | HotScore={float(r['HotScore_norm']):.3f} | ↑7d={float(r.get('growth_7') or 0):.2f}\n")
    st.success("已导出到 reports/ 目录。")

if st.button("导出 PDF 报告 (reports/report.pdf)"):
    from src.reports.export_pdf import export_pdf_from_view
    export_pdf_from_view(view)
    st.success("已生成 reports/report.pdf")
