# SmartLid 快速入門指南

這是一個簡化版的快速開始教程，適合想快速測試系統的使用者。

## 🚀 5 分鐘快速上手

### 步驟 1：下載專案

```bash
cd ~
git clone https://github.com/your-username/SmartToilet.git
cd SmartToilet
```

### 步驟 2：安裝依賴

```bash
# 更新系統
sudo apt update

# 安裝必要套件
sudo apt install python3-pip python3-gpiozero python3-pygame -y

# 安裝 Python 套件
pip3 install -r requirements.txt
```

### 步驟 3：設定環境變數

```bash
# 複製範例檔案
cp .env

# 編輯設定檔
nano .env
```

**必須修改的項目：**
- `LINE_CHANNEL_ACCESS_TOKEN` → 你的 LINE Bot Token
- `LINE_USER_ID` → 你的 LINE User ID

### 步驟 4：準備音效檔案

將兩個 MP3 檔案放入 `data/sounds/` 目錄：
```bash
# 建立目錄
mkdir -p data/sounds

# 複製你的音效檔案
cp /path/to/your/alert1.mp3 data/sounds/
cp /path/to/your/alert2.mp3 data/sounds/
```

### 步驟 5：檢查系統

```bash
sudo python3 check_system.py
```

如果所有檢查都通過，繼續下一步。

### 步驟 6：執行程式

```bash
cd ~/SmartToilet
sudo python3 src/main.py
```

---

## 🔌 硬體快速連接

### 磁簧開關

```
Raspberry Pi GPIO 17 ──┬── 磁簧開關一端
                       │
Raspberry Pi GND ──────┴── 磁簧開關另一端
```

### 伺服馬達（SG90）

```
Raspberry Pi GPIO 18 ──── 黃色線（訊號）
Raspberry Pi 5V      ──── 紅色線（電源）
Raspberry Pi GND     ──── 棕色線（地線）
```

### 音響

```
Raspberry Pi 3.5mm 音源孔 ──── 外接音響 AUX IN
```

---

## 🧪 測試功能

### 測試 1：磁簧開關

執行程式後，手動移動磁鐵靠近/遠離磁簧開關，應該會看到：

```
[偵測] 訊號 HIGH (1): 馬桶蓋抬起！
[偵測] 訊號 LOW (0): 馬桶蓋放下！
```

### 測試 2：計時器

磁鐵遠離開關後等待 60 秒，應該會看到：

```
⏰ 計時器到期！蓋子仍未放下。
🔔 [階段1 提醒] 當日第 1 次
```

### 測試 3：音效播放

提醒時應該會自動播放音效。

### 測試 4：伺服馬達

提醒時馬達應該會轉動。

### 測試 5：LINE 通知

第二次未落蓋時應該會收到 LINE 通知。

---

## ❓ 常見問題速查

### Q1: 權限錯誤

```bash
# 解決方法：加 sudo
sudo python3 src/main.py
```

### Q2: 找不到模組

```bash
# 重新安裝依賴
pip3 install -r requirements.txt --force-reinstall
```

### Q3: 磁簧開關沒反應

- 檢查接線是否正確
- 磁鐵距離是否太遠（建議 < 1cm）
- 嘗試翻轉磁鐵極性

### Q4: 伺服馬達不動

- 確認電源線接在 5V 針腳
- 調整 `.env` 中的 `SERVO_DUTY_PUSH` 參數

### Q5: 沒有聲音

```bash
# 測試音效裝置
speaker-test -t wav

# 手動播放音效
mpg123 data/sounds/alert1.mp3
```

---

## 📞 取得協助

- **詳細文件**：請參考 `README.md`
- **LINE Bot 設定**：請參考 `docs/LINE_MESSAGING_API_GUIDE.md`

---

**祝你使用順利！🚀**
