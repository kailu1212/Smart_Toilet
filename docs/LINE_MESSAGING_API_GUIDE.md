# LINE Messaging API 設定與測試指南

## 📋 步驟 1：建立 LINE Messaging API Channel

### 1. 前往 LINE Developers Console
開啟：https://developers.line.biz/console/

### 2. 建立 Provider（如果還沒有）
- 點選 "Create a new provider"
- 輸入 Provider 名稱（例如：SmartLid）

### 3. 建立 Messaging API Channel
- 在 Provider 下點選 "Create a Messaging API channel"
- 填寫資訊：
  - Channel name: `SmartLid Bot`
  - Channel description: `智慧馬桶蓋提醒系統`
  - Category: 選擇相關類別
  - Subcategory: 選擇相關子類別
- 同意條款後建立

### 4. 取得 Channel Access Token
- 進入剛建立的 Channel
- 點選 "Messaging API" 頁籤
- 往下滾動到 "Channel access token"
- 點選 "Issue" 發行 Token
- **複製並保存這個 Token**

### 5. 取得你的 User ID

**方法 A：使用 LINE 官方帳號管理員（最簡單）**
1. 用手機掃描 Channel 的 QR Code 加 Bot 為好友
2. 發送任意訊息給 Bot
3. 在 LINE Official Account Manager 中查看訊息記錄
4. 可以看到 User ID

**方法 B：使用測試工具**
```bash
# 安裝 line-bot-sdk
pip install line-bot-sdk

# 建立簡單的腳本來取得 User ID（參考下方程式碼）
```

**方法 C：暫時使用 Webhook（最準確）**
- 稍後會提供簡單的腳本來取得

---

## 📋 步驟 2：設定環境變數

編輯 `.env` 檔案：

```bash
# LINE Messaging API 配置
LINE_CHANNEL_ACCESS_TOKEN=你的_Channel_Access_Token
LINE_USER_ID=你的_User_ID
```

---

## 🧪 步驟 3：測試發送訊息

### 基本測試
```bash
cd /Users/lyon/Documents/中央/物聯網/專案/SmartToilet
python src/services/line_messaging.py
```

### 自訂測試
```python
from src.services.line_messaging import LineMessagingService

# 建立服務
line_service = LineMessagingService(
    channel_access_token="你的Token",
    user_id="你的UserID"
)

# 發送測試訊息
line_service.send_message("測試訊息 🎉")

# 發送提醒
line_service.send_alert(alert_count=2, today_date="2025-12-07")

# 發送美化版提醒（Flex Message）
line_service.send_alert_flex(alert_count=2, today_date="2025-12-07")
```

---

## 🎨 功能特色

### 1. 基本文字訊息
簡單的純文字通知

### 2. Flex Message（推薦）✨
- 更美觀的卡片式訊息
- 支援顏色、圖示、排版
- 更好的使用者體驗

### 3. 免費額度
- 每月 500 則推播訊息免費
- 對於 SmartLid 專案完全足夠

---

## 💡 取得 User ID 的簡單方法

如果你不確定如何取得 User ID，可以先執行這個簡單測試：

```python
# 使用任意 User ID 測試（會失敗但會顯示錯誤訊息）
from src.services.line_messaging import LineMessagingService

line = LineMessagingService("你的Token", "測試用ID")
line.send_message("測試")
# 檢查錯誤訊息，可能會提示正確的格式
```

或者我可以幫你建立一個簡單的 Webhook 伺服器來取得 User ID！

---

## ✅ 優點

- ✅ 不需要 Webhook（使用 Push Message）
- ✅ 更豐富的訊息格式
- ✅ 官方長期支援
- ✅ 免費額度足夠使用

## 📝 下一步

1. 建立 LINE Bot Channel
2. 取得 Channel Access Token 和 User ID
3. 更新 `.env` 檔案
4. 執行測試腳本
5. 整合到 SmartLid 主程式

需要幫忙建立取得 User ID 的工具嗎？
