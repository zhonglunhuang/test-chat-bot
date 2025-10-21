# API 呼叫記錄功能測試

## 測試目標
驗證 API 呼叫記錄的 localStorage 儲存功能是否正確運作。

---

## 測試案例 1：API 記錄基本儲存

### 步驟
1. 開啟應用程式
2. 輸入訊息：`測試 API 記錄`
3. 等待 AI 回應完成
4. 點擊左側邊欄的 **"📋 API 呼叫記錄"**
5. 展開查看記錄

### 預期結果
✅ 顯示 1 筆 API 呼叫記錄
✅ 記錄包含以下資訊：
- 時間戳記（格式：YYYY-MM-DD HH:MM:SS）
- 請求資訊：
  - `prompt_id`
  - `prompt_version`
  - `input_preview`（前 100 字）
  - `input_length`
  - `context_messages`
- 回應資訊：
  - `success: true`
  - `output_preview`（前 200 字）
  - `output_length`
  - `elapsed_time_seconds`

### 範例格式
```json
{
  "timestamp": "2025-10-21 12:34:56",
  "data": {
    "request": {
      "prompt_id": "pmpt_68f663c9400081968c77a12c68f176e80438728839e32f32",
      "prompt_version": "6",
      "input_preview": "測試 API 記錄",
      "input_length": 20,
      "context_messages": 0
    },
    "response": {
      "success": true,
      "output_preview": "您好！我是 Lisa 老師的專屬文案助手...",
      "output_length": 150,
      "elapsed_time_seconds": 2.34
    }
  }
}
```

---

## 測試案例 2：API 記錄 localStorage 驗證

### 步驟
1. 完成測試案例 1（已有 1 筆 API 記錄）
2. 按 **F12** 開啟開發者工具
3. 切換到 **Application** > **Local Storage**
4. 查看 `lisa_chat_api_logs` 項目
5. 檢查內容

### 預期結果
✅ localStorage 中存在 `lisa_chat_api_logs` key
✅ 值為 JSON 陣列格式
✅ 陣列包含 1 個物件
✅ 物件結構與測試案例 1 的範例格式一致

### 驗證方法
在 Console 執行：
```javascript
JSON.parse(localStorage.getItem('lisa_chat_api_logs'))
```

應該返回包含 API 記錄的陣列。

---

## 測試案例 3：重新整理後 API 記錄保留

### 步驟
1. 完成測試案例 1（已有 1 筆 API 記錄）
2. 按 **F5** 重新整理頁面
3. 等待頁面完全載入
4. 點擊左側邊欄的 **"📋 API 呼叫記錄"**
5. 展開查看

### 預期結果
✅ 顯示 "共 1 筆記錄"
✅ API 記錄完整顯示
✅ 時間戳記正確
✅ 所有欄位資料完整

### 失敗條件
❌ API 記錄消失
❌ 顯示 "尚無 API 呼叫記錄"
❌ 記錄資料不完整

---

## 測試案例 4：多次 API 呼叫記錄累積

### 步驟
1. 開啟應用程式
2. 依序輸入以下訊息（每次等待回應）：
   - `第一次測試`
   - `第二次測試`
   - `第三次測試`
3. 檢查 API 呼叫記錄
4. 重新整理頁面
5. 再次檢查 API 呼叫記錄

### 預期結果
重新整理前：
✅ 顯示 "共 3 筆記錄"
✅ 記錄按時間倒序排列（最新的在上面）
✅ 每筆記錄的編號正確（#3, #2, #1）

重新整理後：
✅ 仍顯示 "共 3 筆記錄"
✅ 所有記錄完整保留
✅ 順序和編號正確

---

## 測試案例 5：上下文訊息數量正確記錄

### 步驟
1. 開啟應用程式
2. 輸入第一則訊息：`你好`
3. 等待回應後，檢查 API 記錄的 `context_messages`
4. 輸入第二則訊息：`你記得我是誰嗎？`
5. 等待回應後，檢查第二筆 API 記錄的 `context_messages`
6. 輸入第三則訊息：`謝謝`
7. 檢查第三筆 API 記錄

### 預期結果
✅ 第 1 筆記錄：`context_messages: 0`（沒有上下文）
✅ 第 2 筆記錄：`context_messages: 2`（1 個使用者訊息 + 1 個 AI 回應）
✅ 第 3 筆記錄：`context_messages: 4`（2 個使用者訊息 + 2 個 AI 回應）

### 驗證邏輯
`context_messages` 應該等於當前訊息之前的訊息總數。

---

## 測試案例 6：API 回應時間記錄

### 步驟
1. 輸入訊息並等待回應
2. 檢查 API 記錄中的 `elapsed_time_seconds`
3. 驗證時間是否合理

### 預期結果
✅ `elapsed_time_seconds` 為數字
✅ 數值合理（通常 1-10 秒）
✅ 精確到小數點後 2 位

### 範例
```json
"elapsed_time_seconds": 2.34
```

---

## 測試案例 7：錯誤情況的 API 記錄

### 步驟
1. 嘗試觸發 API 錯誤（例如：暫時關閉網路，或等待 API 配額用盡）
2. 檢查 API 呼叫記錄

### 預期結果
✅ 錯誤也會被記錄
✅ 記錄包含：
```json
{
  "timestamp": "2025-10-21 12:34:56",
  "data": {
    "request": {
      "prompt_id": "...",
      "prompt_version": "6",
      "input_preview": "測試訊息"
    },
    "response": {
      "success": false,
      "error": "錯誤訊息",
      "error_type": "錯誤類型"
    }
  }
}
```

✅ 重新整理後錯誤記錄仍保留

---

## 測試案例 8：清除 API 記錄

### 步驟
1. 完成測試案例 4（已有 3 筆 API 記錄）
2. 點擊 **"🗑️ 清除對話歷史"**
3. 檢查 API 呼叫記錄
4. 重新整理頁面
5. 再次檢查

### 預期結果
點擊清除後：
✅ API 呼叫記錄區域顯示 "尚無 API 呼叫記錄"
✅ 顯示 "共 0 筆記錄" 或不顯示筆數

重新整理後：
✅ 仍然是空的
✅ localStorage 中的 `lisa_chat_api_logs` 已被移除或為空陣列

### 驗證方法
在 Console 執行：
```javascript
localStorage.getItem('lisa_chat_api_logs')
```
應該返回 `null` 或 `"[]"`

---

## 測試案例 9：輸入長度截斷測試

### 步驟
1. 輸入一則超過 100 字的訊息
2. 等待 AI 回應
3. 檢查 API 記錄的 `input_preview`

### 預期結果
✅ `input_preview` 只顯示前 100 字
✅ 結尾有 `...` 省略符號
✅ `input_length` 顯示完整長度（包含上下文）

### 範例
```json
"input_preview": "這是一則很長很長很長很長很長很長很長很長很長很長很長很長很長很長很長很長很長很長很長很長很長很長很長很長很長很長很長很長很長很長的訊息...",
"input_length": 500
```

---

## 測試案例 10：輸出長度截斷測試

### 步驟
1. 輸入：`請寫一篇 500 字的文章`
2. 等待 AI 回應（應該會很長）
3. 檢查 API 記錄的 `output_preview`

### 預期結果
✅ `output_preview` 只顯示前 200 字
✅ 結尾有 `...` 省略符號
✅ `output_length` 顯示完整長度

---

## 瀏覽器 Console 檢查指令

### 查看所有 API 記錄
```javascript
const logs = JSON.parse(localStorage.getItem('lisa_chat_api_logs'));
console.log('API Logs:', logs);
console.log('Total logs:', logs ? logs.length : 0);
```

### 查看最新一筆記錄
```javascript
const logs = JSON.parse(localStorage.getItem('lisa_chat_api_logs'));
console.log('Latest log:', logs[logs.length - 1]);
```

### 清除 API 記錄
```javascript
localStorage.removeItem('lisa_chat_api_logs');
console.log('API logs cleared');
```

### 檢查記錄大小
```javascript
const logs = localStorage.getItem('lisa_chat_api_logs');
console.log('Storage size:', logs ? (logs.length / 1024).toFixed(2) + ' KB' : '0 KB');
```

---

## 驗收標準

### 必須通過（P0）
- ✅ 測試案例 1：API 記錄基本儲存
- ✅ 測試案例 2：localStorage 驗證
- ✅ 測試案例 3：重新整理後保留
- ✅ 測試案例 4：多次呼叫累積
- ✅ 測試案例 8：清除功能

### 應該通過（P1）
- ✅ 測試案例 5：上下文數量正確
- ✅ 測試案例 6：回應時間記錄
- ✅ 測試案例 7：錯誤記錄

### 可選通過（P2）
- ✅ 測試案例 9：輸入截斷
- ✅ 測試案例 10：輸出截斷

---

## 快速測試檢查清單

執行以下步驟快速驗證 API 記錄功能：

1. ☐ 發送 1 則訊息，檢查 API 記錄出現
2. ☐ 按 F12 檢查 localStorage 有 `lisa_chat_api_logs`
3. ☐ 重新整理頁面，API 記錄仍在
4. ☐ 發送第 2、3 則訊息，記錄累積到 3 筆
5. ☐ 檢查 `context_messages` 遞增（0, 2, 4）
6. ☐ 檢查 `elapsed_time_seconds` 有數值
7. ☐ 點擊清除按鈕，記錄清空
8. ☐ 重新整理確認記錄不會恢復

**全部完成** ✅ = API 記錄功能正常運作！
