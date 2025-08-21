# 部署指南（Streamlit Community Cloud）

1) 推送到 GitHub（入口文件：`app_streamlit.py`）
2) 打开 share.streamlit.io → Create app → 选择仓库/分支 → 部署
3) **Secrets** 添加：
```
APIFY_TOKEN="<你的 Apify Token>"
SUBSCRIPTION_URL="https://buy.stripe.com/your-monthly-link"
SUBSCRIPTION_URL_Q="https://buy.stripe.com/your-quarterly-link"
SUBSCRIPTION_URL_Y="https://buy.stripe.com/your-yearly-link"
SUBSCRIPTION_REFUND="首次下单 7 天内不满意可全额退款"
SUBSCRIPTION_SCHEDULE="每周一 / 周四 20:00（本地时区）更新"
SUPPORT_EMAIL="support@yourdomain.com"
```
