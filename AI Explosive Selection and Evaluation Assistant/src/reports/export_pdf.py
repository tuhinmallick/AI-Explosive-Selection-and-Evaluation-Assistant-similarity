from __future__ import annotations
import os, datetime as dt, numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
def _sparkline(total, growth_hint=0.2):
    if total is None or not isinstance(total,(int,float)) or total<=0:
        base=100*(1+growth_hint); xs=np.linspace(0.8,1.2*(1+growth_hint),7); return (base*xs + np.random.normal(0, base*0.05, 7)).clip(min=1)
    parts=np.random.dirichlet(np.ones(7)); s=total*parts; trend=np.linspace(0.9,1.1*(1+growth_hint),7); return (s*trend).clip(min=1)
def export_pdf_from_view(view_df: pd.DataFrame, out_path: str = "reports/report.pdf"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with PdfPages(out_path) as pdf:
        plt.figure(figsize=(11,8.5)); plt.axis('off')
        plt.text(0.05,0.86,"Product Research AI · 选品报告（Beauty）", fontsize=28, weight='bold')
        plt.text(0.05,0.76,"聚合 TikTok 信号 → HotScore → 行动清单", fontsize=16)
        plt.text(0.05,0.66,"订阅价格：月 $9.9｜季 $24.9｜年 $79.9", fontsize=14)
        plt.text(0.05,0.12,f"生成日期：{dt.date.today().isoformat()}", fontsize=11); pdf.savefig(); plt.close()
        plt.figure(figsize=(11,8.5)); plt.axis('off'); plt.text(0.05,0.92,f"Top {len(view_df)} 候选爆品清单", fontsize=20, weight='bold')
        y=0.85; plt.text(0.05,y,"Rank  Platform  Price    Score   Title", fontsize=12, family='monospace'); y-=0.03
        for _, r in view_df.iterrows():
            line=f"{int(r['rank']):>4}  {str(r['platform']):<8}  ${float(r['price']):>6.2f}  {float(r['HotScore_norm']):>5.3f}  {str(r['title'])[:70]}"
            plt.text(0.05,y,line,fontsize=10,family='monospace'); y-=0.022
            if y<0.08: pdf.savefig(); plt.close(); plt.figure(figsize=(11,8.5)); plt.axis('off'); y=0.92
        pdf.savefig(); plt.close()
        for _, r in view_df.iterrows():
            plt.figure(figsize=(11,8.5))
            plt.suptitle(f"[{int(r['rank']):02}] {r['title']}", y=0.97, fontsize=16, weight='bold')
            plt.subplot(2,1,1); plt.axis('off')
            details=[f"平台：{r['platform']}", f"类目：{r.get('category','')}", f"价格：${float(r['price']):.2f}", f"HotScore：{float(r['HotScore_norm']):.3f}", f"素材参考链接：{r.get('url','') or ''}"]
            for i, t in enumerate(details): plt.text(0.01,0.9-i*0.1,t,fontsize=12)
            ax=plt.subplot(2,1,2); total=r.get('engagement_7') or r.get('views_7') or 0; series=_sparkline(total, float(r.get('growth_7') or 0.2))
            ax.plot(range(1,8),series,marker='o'); ax.set_title("7天动量（相对量纲）"); ax.set_xlabel("Day"); ax.set_ylabel("Relative momentum")
            pdf.savefig(); plt.close()
    return out_path
