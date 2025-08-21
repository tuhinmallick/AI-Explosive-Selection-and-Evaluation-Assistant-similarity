![Hero](README_hero.png)

# Product Research AI · 爆品选品助手（Beauty 版）

见 DEPLOYMENT_GUIDE.md 获取部署与订阅说明。

## 💳 订阅与退款政策（Stripe）
**价位：** 月付 **$9.9** ｜ 季付 **$24.9** ｜ 年付 **$79.9**  
**退款承诺：** 首次下单 **7 天内** 不满意可全额退款（发邮件/表单即处理）。  
**更新频率：** 固定 **每周一 / 周四** 产出新报告（可在环境变量中自定义）。

### 配置方式（本地/服务器 环境变量或 Streamlit Cloud Secrets）
```ini
SUBSCRIPTION_URL="https://buy.stripe.com/your-monthly-link"      # 月付 $9.9
SUBSCRIPTION_URL_Q="https://buy.stripe.com/your-quarterly-link"  # 季付 $24.9
SUBSCRIPTION_URL_Y="https://buy.stripe.com/your-yearly-link"     # 年付 $79.9
SUBSCRIPTION_REFUND="首次下单 7 天内不满意可全额退款"
SUBSCRIPTION_SCHEDULE="每周一 / 周四 20:00（本地时区）更新"
SUPPORT_EMAIL="support@yourdomain.com"
```
