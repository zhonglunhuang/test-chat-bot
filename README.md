# 🤖 AI 聊天助手

使用 OpenAI Responses API 的網頁版聊天應用程式，透過 Streamlit 建立，可免費部署到雲端讓客戶使用。

## ✨ 功能特色

- 💬 即時對話介面
- 🎨 簡潔友善的 UI
- 📝 對話歷史記錄
- 🔒 API Key 安全隱藏
- ☁️ 可部署到雲端

## 🚀 部署到 Streamlit Cloud（推薦）

### 步驟 1: 準備 GitHub Repository

1. 在 GitHub 建立新的 repository
2. 將此專案推送到 GitHub：

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的使用者名稱/你的repo名稱.git
git push -u origin main
```

⚠️ **重要**: 確保 `.gitignore` 已經加入，這樣 API key 不會被上傳到 GitHub

### 步驟 2: 部署到 Streamlit Cloud

1. 前往 [share.streamlit.io](https://share.streamlit.io/)
2. 使用 GitHub 帳號登入
3. 點擊 "New app"
4. 選擇你的 repository、branch (main) 和 main file (app.py)
5. 點擊 "Deploy"

### 步驟 3: 設定環境變數（Secrets）

部署後，需要設定 API Key：

1. 在 Streamlit Cloud 的應用設定頁面
2. 點擊 "⚙️ Settings" → "Secrets"
3. 加入以下內容：

```toml
OPENAI_API_KEY = "your-api-key-here"
PROMPT_ID = "pmpt_68f663c9400081968c77a12c68f176e80438728839e32f32"
PROMPT_VERSION = "4"
```

4. 點擊 "Save"
5. 應用程式會自動重新啟動

### 步驟 4: 分享給客戶

部署完成後，你會得到一個公開網址，例如：
```
https://你的應用名稱.streamlit.app
```

直接分享這個網址給客戶，他們就可以透過瀏覽器使用，**不需要任何 API key**！

## 💻 本地測試

如果想在部署前本地測試：

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 設定環境變數

建立 `.streamlit/secrets.toml` 檔案（不會被 git 追蹤）：

```toml
OPENAI_API_KEY = "your-api-key-here"
PROMPT_ID = "pmpt_68f663c9400081968c77a12c68f176e80438728839e32f32"
PROMPT_VERSION = "4"
```

或使用環境變數：

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. 執行應用

```bash
streamlit run app.py
```

瀏覽器會自動開啟 `http://localhost:8501`

## 📁 專案結構

```
.
├── app.py                 # Streamlit 主程式
├── ai_chat拷貝.py        # 原始命令列版本
├── requirements.txt       # Python 依賴套件
├── .gitignore            # Git 忽略檔案（保護 secrets）
└── README.md             # 說明文件
```

## 🔒 安全性說明

- ✅ API Key 透過 Streamlit Secrets 管理，不會出現在程式碼中
- ✅ `.gitignore` 確保 secrets 檔案不會被上傳到 GitHub
- ✅ 客戶只能透過你的應用使用 AI，無法直接存取你的 API Key
- ✅ 可在 OpenAI 平台設定使用額度限制

## 🆓 費用說明

- **Streamlit Cloud**: 免費方案（public apps）
- **OpenAI API**: 依使用量計費，建議設定月度預算

## 🛠️ 進階設定

### 限制使用額度

在 OpenAI 平台設定：
1. 前往 [platform.openai.com](https://platform.openai.com)
2. Settings → Limits
3. 設定 Monthly budget

### 自訂 Prompt

1. 在 OpenAI 平台修改你的 Prompt
2. 更新 Streamlit Secrets 中的 `PROMPT_VERSION`

### 監控使用情況

在 OpenAI 平台的 Usage 頁面可以查看 API 使用統計

## 📞 支援

如有問題，請檢查：
- Streamlit Cloud logs（在應用設定頁面）
- OpenAI API 額度是否足夠
- Secrets 是否正確設定

## 📝 授權

此專案為示範用途，可自由修改使用。
