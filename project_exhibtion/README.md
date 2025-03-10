# LINE Bot Exhibition Assistant

## 專案簡介（本 md 為 AI 生成，程式碼則否）

這是一個基於 Flask 框架開發的 LINE Bot 展覽助手系統，整合了多項功能來協助使用者獲取和管理展覽相關資訊。

## 主要功能

- 展覽資訊查詢與回覆
- 圖片訊息處理
- 使用者互動記錄
- MongoDB 資料儲存
- 自動載入動畫
- Webhook 事件處理

## 系統需求

- Python 3.8+
- Flask
- LINE Messaging API SDK v3
- MongoDB
- 其他相依套件請參考 requirements.txt

## 安裝步驟

1. 複製專案

```bash
git clone [repository-url]
cd project_exhibition
```

2. 安裝相依套件

```bash
pip install -r requirements.txt
```

3. 設定環境變數
   建立 `config.ini` 檔案，包含以下設定：

```ini
[LINE]
CHANNEL_ACCESS_TOKEN=your_channel_access_token
CHANNEL_SECRET=your_channel_secret
```

## 專案結構

```
project_exhibition/
├── app.py                      # 主程式入口
├── loading_animation.py        # 載入動畫功能
├── start_estab_mgdb.py        # MongoDB 初始化
├── user_reply_mgdb.py         # 使用者回覆處理
├── postback_reply_mgdb.py     # Postback 事件處理
└── config.ini                 # 設定檔
```

## 使用方法

1. 啟動服務器

```bash
python app.py
```

服務器將在 port 5001 啟動

2. 設定 LINE Bot Webhook URL

- 設定為 `https://your-domain/callback`

## API 文件

### 主要端點

- `/callback` (POST): LINE Webhook 接收端點

### 事件處理

- 文字訊息處理
- 圖片訊息處理
- Postback 事件處理

## 資料庫結構

使用 MongoDB 儲存：

- 使用者資訊
- 事件記錄
- 互動歷史

## 開發者

- 專案負責人：[您的名字]
- 聯絡方式：[您的聯絡資訊]

## 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案
