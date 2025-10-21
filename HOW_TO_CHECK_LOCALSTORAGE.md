# 如何查看 localStorage 資料 - 完整指南

## 🎯 目標
學會如何在瀏覽器中查看和驗證對話記錄是否正確儲存到 localStorage。

---

## 📋 方法 1：使用開發者工具（最直覺）

### Chrome / Edge / Brave 步驟

#### 步驟 1：開啟應用程式
1. 在瀏覽器中開啟你的 Lisa 老師文案助手
2. 發送至少一則訊息給 AI
3. 等待 AI 回應

#### 步驟 2：開啟開發者工具
- **方法 A**：按鍵盤 `F12` 鍵
- **方法 B**：按 `Ctrl + Shift + I`（Windows）或 `Cmd + Option + I`（Mac）
- **方法 C**：右鍵點擊頁面任意處 → 選擇「檢查」或「Inspect」

#### 步驟 3：切換到 Application 分頁
1. 開發者工具開啟後，看頂部的分頁列
2. 找到並點擊 **Application** 分頁
3. 如果看不到，點擊 `>>` 符號，在下拉選單中選擇 Application

#### 步驟 4：展開 Local Storage
1. 在左側選單中找到 **Storage** 區塊
2. 展開 **Local Storage** 項目
3. 點擊你的網址（例如：`https://your-app.streamlit.app` 或 `http://localhost:8501`）

#### 步驟 5：查看資料
你應該會看到以下 keys：

**Key: `lisa_chat_messages`**
- 點擊這個 key
- 右側會顯示 JSON 格式的對話記錄
- 應該包含你剛剛發送的訊息和 AI 的回應

**Key: `lisa_chat_api_logs`**
- 點擊這個 key
- 右側會顯示 API 呼叫記錄
- 包含時間戳記、請求資訊、回應時間等

#### 預期畫面
```
Key                        | Value
---------------------------|----------------------------------
lisa_chat_messages         | [{"role":"user","content":"...
lisa_chat_api_logs         | [{"timestamp":"2025-10-21...
```

---

### Firefox 步驟

#### 步驟 1-2：開啟開發者工具
- 按 `F12` 或 `Ctrl + Shift + I`

#### 步驟 3：切換到 Storage 分頁
- 點擊頂部的 **Storage** 分頁（不是 Application）

#### 步驟 4：展開 Local Storage
- 左側選單展開 **本機儲存空間** 或 **Local Storage**
- 點擊你的網址

#### 步驟 5：查看資料
- 右側會顯示所有 localStorage 的 keys 和 values

---

### Safari 步驟

#### 步驟 0：啟用開發者選單（首次使用）
1. Safari 選單 → 偏好設定 → 進階
2. 勾選「在選單列顯示開發選單」

#### 步驟 1：開啟網頁檢閱器
- 按 `Cmd + Option + I`

#### 步驟 2：切換到 Storage 分頁
- 點擊 **Storage** 分頁

#### 步驟 3：查看 Local Storage
- 左側選擇 **Local Storage** → 你的網址

---

## 💻 方法 2：使用 Console 快速檢查

### 基本指令

#### 1. 開啟 Console
- 按 `F12` → 切換到 **Console** 分頁
- 或直接按 `Ctrl + Shift + J`（Windows）/ `Cmd + Option + J`（Mac）

#### 2. 查看對話記錄
複製貼上以下指令並按 Enter：

```javascript
// 查看對話記錄
const messages = localStorage.getItem('lisa_chat_messages');
if (messages) {
    const data = JSON.parse(messages);
    console.log('📝 對話記錄數量:', data.length);
    console.log('📝 完整資料:', data);
} else {
    console.log('❌ 尚無對話記錄');
}
```

**預期輸出**：
```
📝 對話記錄數量: 2
📝 完整資料: Array(2)
  0: {role: 'user', content: '你好'}
  1: {role: 'assistant', content: '您好！我是 Lisa 老師...'}
```

#### 3. 查看 API 記錄
```javascript
// 查看 API 記錄
const apiLogs = localStorage.getItem('lisa_chat_api_logs');
if (apiLogs) {
    const data = JSON.parse(apiLogs);
    console.log('📊 API 記錄數量:', data.length);
    console.log('📊 完整資料:', data);

    // 顯示最新一筆
    if (data.length > 0) {
        console.log('🆕 最新記錄:', data[data.length - 1]);
    }
} else {
    console.log('❌ 尚無 API 記錄');
}
```

#### 4. 查看所有 localStorage keys
```javascript
// 列出所有 keys
console.log('🔑 所有 localStorage keys:', Object.keys(localStorage));
```

#### 5. 查看儲存空間使用情況
```javascript
// 計算使用的儲存空間
let totalSize = 0;
for (let key in localStorage) {
    if (localStorage.hasOwnProperty(key)) {
        totalSize += localStorage[key].length + key.length;
    }
}
console.log('💾 總使用空間:', (totalSize / 1024).toFixed(2) + ' KB');

// 個別項目大小
const messages = localStorage.getItem('lisa_chat_messages');
const apiLogs = localStorage.getItem('lisa_chat_api_logs');
console.log('💬 對話記錄:', (messages?.length / 1024).toFixed(2) + ' KB');
console.log('📊 API 記錄:', (apiLogs?.length / 1024).toFixed(2) + ' KB');
```

---

## 🧪 完整測試流程

### 測試 1：驗證儲存功能

#### Step 1：清空現有資料
在 Console 執行：
```javascript
localStorage.clear();
console.log('✅ localStorage 已清空');
```

#### Step 2：發送訊息
1. 在應用中輸入：`測試 localStorage`
2. 等待 AI 回應

#### Step 3：立即檢查是否儲存
在 Console 執行：
```javascript
const messages = JSON.parse(localStorage.getItem('lisa_chat_messages'));
console.log('✅ 對話記錄已儲存:', messages.length, '則訊息');
```

**預期輸出**：`✅ 對話記錄已儲存: 2 則訊息`

---

### 測試 2：驗證重新整理後保留

#### Step 1：記錄當前訊息數量
在 Console 執行：
```javascript
const before = JSON.parse(localStorage.getItem('lisa_chat_messages')).length;
console.log('重新整理前:', before, '則訊息');
```

#### Step 2：重新整理頁面
按 `F5` 或點擊重新整理按鈕

#### Step 3：檢查資料是否保留
頁面載入後，在 Console 執行：
```javascript
const after = JSON.parse(localStorage.getItem('lisa_chat_messages')).length;
console.log('重新整理後:', after, '則訊息');

if (before === after) {
    console.log('✅ 資料完整保留！');
} else {
    console.log('❌ 資料遺失！');
}
```

---

### 測試 3：驗證清除功能

#### Step 1：確認有資料
```javascript
console.log('清除前:',
    JSON.parse(localStorage.getItem('lisa_chat_messages'))?.length || 0,
    '則訊息'
);
```

#### Step 2：點擊清除按鈕
在應用中點擊 **"🗑️ 清除對話歷史"**

#### Step 3：檢查是否清空
```javascript
const messages = localStorage.getItem('lisa_chat_messages');
const apiLogs = localStorage.getItem('lisa_chat_api_logs');

if (!messages || JSON.parse(messages).length === 0) {
    console.log('✅ 對話記錄已清除');
} else {
    console.log('❌ 對話記錄未清除');
}

if (!apiLogs || JSON.parse(apiLogs).length === 0) {
    console.log('✅ API 記錄已清除');
} else {
    console.log('❌ API 記錄未清除');
}
```

---

## 🔍 進階檢查指令

### 美化 JSON 輸出
```javascript
// 格式化顯示對話記錄
const messages = JSON.parse(localStorage.getItem('lisa_chat_messages'));
console.log(JSON.stringify(messages, null, 2));
```

### 搜尋特定內容
```javascript
// 搜尋包含特定關鍵字的訊息
const messages = JSON.parse(localStorage.getItem('lisa_chat_messages'));
const keyword = '測試';
const results = messages.filter(msg => msg.content.includes(keyword));
console.log(`找到 ${results.length} 則包含 "${keyword}" 的訊息:`, results);
```

### 統計資訊
```javascript
// 統計使用者訊息和 AI 回應數量
const messages = JSON.parse(localStorage.getItem('lisa_chat_messages'));
const userMsgs = messages.filter(m => m.role === 'user').length;
const aiMsgs = messages.filter(m => m.role === 'assistant').length;
console.log(`👤 使用者訊息: ${userMsgs} 則`);
console.log(`🤖 AI 回應: ${aiMsgs} 則`);
console.log(`📊 總計: ${messages.length} 則`);
```

### 匯出資料
```javascript
// 匯出所有資料為 JSON 檔案
const data = {
    messages: JSON.parse(localStorage.getItem('lisa_chat_messages')),
    apiLogs: JSON.parse(localStorage.getItem('lisa_chat_api_logs')),
    exportDate: new Date().toISOString()
};

const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'lisa_chat_backup.json';
a.click();

console.log('✅ 資料已匯出為 JSON 檔案');
```

---

## 📱 手機版查看方法

### iOS Safari
1. 在 Mac 上開啟 Safari → 開發 → [你的 iPhone] → [網頁]
2. 使用 Mac 的開發者工具查看

### Android Chrome
1. 在電腦 Chrome 開啟 `chrome://inspect`
2. 連接手機並啟用 USB 偵錯
3. 選擇手機上的分頁進行檢查

---

## ❓ 常見問題

### Q: 我看不到任何資料
**A:** 檢查以下幾點：
1. 確認已經發送過訊息
2. 確認不是在無痕模式（隱私瀏覽模式下 localStorage 可能無效）
3. 確認瀏覽器沒有停用 localStorage
4. 在 Console 執行：`console.log(localStorage)` 檢查是否可用

### Q: 資料格式看起來很亂
**A:** 使用以下指令美化顯示：
```javascript
console.log(JSON.stringify(JSON.parse(localStorage.getItem('lisa_chat_messages')), null, 2));
```

### Q: 如何完全清除所有資料？
**A:** 在 Console 執行：
```javascript
localStorage.clear();
location.reload();
```

### Q: localStorage 有大小限制嗎？
**A:** 是的，大多數瀏覽器限制為 5-10 MB。檢查當前使用量：
```javascript
let total = 0;
for (let key in localStorage) {
    if (localStorage.hasOwnProperty(key)) {
        total += (localStorage[key].length + key.length) * 2; // UTF-16
    }
}
console.log('使用量:', (total / 1024 / 1024).toFixed(2), 'MB / 5 MB');
```

---

## ✅ 快速檢查清單

執行以下步驟確認 localStorage 正常運作：

- [ ] 步驟 1：發送一則訊息
- [ ] 步驟 2：按 F12 開啟開發者工具
- [ ] 步驟 3：切換到 Application（Chrome）或 Storage（Firefox）
- [ ] 步驟 4：查看 Local Storage → 你的網址
- [ ] 步驟 5：確認看到 `lisa_chat_messages` 和 `lisa_chat_api_logs`
- [ ] 步驟 6：重新整理頁面（F5）
- [ ] 步驟 7：確認資料仍然存在
- [ ] 步驟 8：點擊清除按鈕
- [ ] 步驟 9：確認 localStorage 被清空

**全部完成** ✅ = localStorage 功能正常！
