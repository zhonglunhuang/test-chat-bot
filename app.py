#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from openai import OpenAI
import os
import json
from datetime import datetime
import streamlit.components.v1 as components

# 設定頁面配置
st.set_page_config(
    page_title="Lisa老師專屬文案助手",
    page_icon="📝",
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# 隱藏 Streamlit 右上角選單和 footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# localStorage 同步腳本
def render_localStorage_sync():
    """在頁面載入時從 localStorage 讀取資料，並在資料變更時儲存"""
    sync_script = """
    <script>
    // 確保只執行一次
    if (!window.localStorageInitialized) {
        window.localStorageInitialized = true;

        // 從 localStorage 讀取資料
        function loadData() {
            try {
                const messages = localStorage.getItem('lisa_chat_messages');
                const apiLogs = localStorage.getItem('lisa_chat_api_logs');

                return {
                    messages: messages ? JSON.parse(messages) : [],
                    api_logs: apiLogs ? JSON.parse(apiLogs) : []
                };
            } catch (e) {
                console.error('Error loading from localStorage:', e);
                return { messages: [], api_logs: [] };
            }
        }

        // 將資料傳送給 Streamlit
        const data = loadData();
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: data
        }, '*');

        console.log('Loaded from localStorage:', data);
    }
    </script>
    """
    return components.html(sync_script, height=0)

def save_to_localStorage(key, data):
    """儲存資料到 localStorage"""
    json_str = json.dumps(data, ensure_ascii=False).replace("'", "\\'").replace('"', '\\"')
    save_script = f"""
    <script>
    try {{
        const data = JSON.parse("{json_str}");
        localStorage.setItem('{key}', JSON.stringify(data));
        console.log('Saved to localStorage {key}:', data.length, 'items');
    }} catch (e) {{
        console.error('Error saving to localStorage:', e);
    }}
    </script>
    """
    components.html(save_script, height=0)

def clear_localStorage():
    """清除 localStorage"""
    clear_script = """
    <script>
    localStorage.removeItem('lisa_chat_messages');
    localStorage.removeItem('lisa_chat_api_logs');
    console.log('Cleared localStorage');
    </script>
    """
    components.html(clear_script, height=0)

# 初始化 OpenAI 客戶端
@st.cache_resource
def init_openai_client():
    """初始化 OpenAI 客戶端（使用快取避免重複建立）"""
    try:
        # 優先使用 Streamlit secrets，本地開發時使用環境變數
        api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
        if not api_key:
            st.error("❌ 未設定 OPENAI_API_KEY")
            st.stop()
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"❌ 無法初始化 OpenAI 客戶端: {e}")
        st.stop()

# 取得 Prompt 配置
def get_prompt_config():
    """取得 Prompt ID 和版本（優先使用 secrets）"""
    prompt_id = st.secrets.get("PROMPT_ID", "pmpt_68f663c9400081968c77a12c68f176e80438728839e32f32")
    prompt_version = st.secrets.get("PROMPT_VERSION", "6")
    return prompt_id, prompt_version

# 初始化
client = init_openai_client()
PROMPT_ID, PROMPT_VERSION = get_prompt_config()

# 從 localStorage 載入資料（頁面載入時）
if "loaded_from_storage" not in st.session_state:
    st.session_state.loaded_from_storage = False
    local_data = render_localStorage_sync()

    # 如果成功載入資料
    if local_data and isinstance(local_data, dict):
        st.session_state.messages = local_data.get('messages', [])
        st.session_state.api_logs = local_data.get('api_logs', [])
        st.session_state.loaded_from_storage = True

# 初始化 session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_logs" not in st.session_state:
    st.session_state.api_logs = []

# 保留文字原始格式
def format_text_with_breaks(text):
    """保留文字的原始格式，不做任何替換"""
    return text if text else ""

# 側邊欄功能
with st.sidebar:
    st.header("⚙️ 功能")

    if st.button("🗑️ 清除對話歷史", use_container_width=True):
        st.session_state.messages = []
        st.session_state.api_logs = []
        clear_localStorage()
        st.rerun()

    st.divider()

    st.subheader("📊 對話統計")
    st.metric("訊息數量", len(st.session_state.messages))

    if st.session_state.loaded_from_storage and len(st.session_state.messages) > 0:
        st.success("✅ 已從瀏覽器載入歷史記錄")

    st.divider()

    st.subheader("💡 使用說明與範例")

    st.markdown("### 如何使用")
    st.markdown("""
    1. 在下方輸入框輸入訊息
    2. 按 Enter 發送
    3. AI 會記住完整對話上下文
    4. 每個使用者的對話記錄是獨立的
    5. **重新整理頁面對話記錄會保留**
    6. 對話記錄儲存在您的瀏覽器中（隱私安全）
    """)

    st.markdown("### 📝 範例 Prompt")
    st.code("""請幫我參照以下內容改寫一篇電子報

主題：2025年數據分析師必備技能

內容素材：
1. 掌握 AI 落地應用趨勢
2. 了解公司現況在 AI 發展優勢（以 Shutterstock 為例）
3. 善用自動化減少日常採集資料工作""", language="text")

    st.divider()

    # API 呼叫 Log 顯示區
    with st.expander("📋 API 呼叫記錄", expanded=False):
        if st.session_state.api_logs:
            st.caption(f"共 {len(st.session_state.api_logs)} 筆記錄")
            for idx, log in enumerate(reversed(st.session_state.api_logs), 1):
                with st.container():
                    st.markdown(f"**#{len(st.session_state.api_logs) - idx + 1}** - {log['timestamp']}")
                    st.json(log['data'])
                    if idx < len(st.session_state.api_logs):
                        st.divider()
        else:
            st.info("尚無 API 呼叫記錄")

# 標題和說明
st.title("📝 Lisa老師專屬文案助手")
st.caption(f"使用 OpenAI Responses API | Prompt 版本: {PROMPT_VERSION}")

# 顯示對話歷史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # 處理換行並顯示
        formatted_content = format_text_with_breaks(message["content"])
        st.markdown(formatted_content)

# 聊天輸入框
if prompt := st.chat_input("輸入訊息..."):
    # 顯示使用者訊息
    with st.chat_message("user"):
        formatted_prompt = format_text_with_breaks(prompt)
        st.markdown(formatted_prompt)

    # 加入到對話歷史
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 儲存到 localStorage
    save_to_localStorage('lisa_chat_messages', st.session_state.messages)

    # 顯示 AI 回應
    with st.chat_message("assistant"):
        with st.spinner("Lisa老師正在思考中..."):
            try:
                # 準備完整的對話歷史（上下文記憶）
                conversation_context = ""
                if len(st.session_state.messages) > 1:
                    # 將之前的對話整理成上下文
                    for msg in st.session_state.messages[:-1]:  # 排除剛剛加入的最新訊息
                        role_name = "使用者" if msg["role"] == "user" else "助手"
                        conversation_context += f"{role_name}: {msg['content']}\n\n"

                # 當前輸入
                current_input = f"{conversation_context}使用者: {prompt}"

                # 記錄 API 請求開始時間
                request_time = datetime.now()

                # 呼叫 OpenAI Responses API
                response = client.responses.create(
                    prompt={
                        "id": PROMPT_ID,
                        "version": PROMPT_VERSION
                    },
                    input=current_input
                )

                # 記錄 API 回應時間
                response_time = datetime.now()
                elapsed_time = (response_time - request_time).total_seconds()

                # 解析回應
                ai_message = ""
                response_items = []

                # 嘗試不同的方式獲取內容
                if hasattr(response, 'output'):
                    if isinstance(response.output, list):
                        response_items = response.output
                    elif isinstance(response.output, str):
                        ai_message = response.output
                elif hasattr(response, 'data'):
                    response_items = response.data if isinstance(response.data, list) else [response.data]
                elif hasattr(response, 'items'):
                    response_items = response.items if isinstance(response.items, list) else [response.items]
                elif isinstance(response, list):
                    response_items = response

                # 解析 response_items
                if not ai_message and response_items:
                    for item in response_items:
                        if (hasattr(item, 'type') and item.type == 'message' and
                            hasattr(item, 'status') and item.status == 'completed'):
                            if hasattr(item, 'content') and item.content:
                                for content_item in item.content:
                                    if hasattr(content_item, 'type') and content_item.type == 'output_text':
                                        if hasattr(content_item, 'text'):
                                            ai_message += content_item.text

                # 如果還是沒有內容
                if not ai_message:
                    ai_message = "抱歉，無法解析 AI 回應。"

                # 記錄完整的 API 呼叫 log
                api_log = {
                    "timestamp": request_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "data": {
                        "request": {
                            "prompt_id": PROMPT_ID,
                            "prompt_version": PROMPT_VERSION,
                            "input_preview": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                            "input_length": len(current_input),
                            "context_messages": len(st.session_state.messages) - 1
                        },
                        "response": {
                            "success": True,
                            "output_preview": ai_message[:200] + "..." if len(ai_message) > 200 else ai_message,
                            "output_length": len(ai_message),
                            "elapsed_time_seconds": round(elapsed_time, 2)
                        }
                    }
                }
                st.session_state.api_logs.append(api_log)
                # 儲存到 localStorage
                save_to_localStorage('lisa_chat_api_logs', st.session_state.api_logs)

                # 處理換行並顯示回應
                formatted_ai_message = format_text_with_breaks(ai_message)
                st.markdown(formatted_ai_message)

                # 加入到對話歷史（儲存原始內容）
                st.session_state.messages.append({"role": "assistant", "content": ai_message})
                # 儲存到 localStorage
                save_to_localStorage('lisa_chat_messages', st.session_state.messages)

            except Exception as e:
                error_msg = f"❌ 錯誤: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                # 儲存到 localStorage
                save_to_localStorage('lisa_chat_messages', st.session_state.messages)

                # 記錄錯誤到 API log
                error_log = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "data": {
                        "request": {
                            "prompt_id": PROMPT_ID,
                            "prompt_version": PROMPT_VERSION,
                            "input_preview": prompt[:100] + "..." if len(prompt) > 100 else prompt
                        },
                        "response": {
                            "success": False,
                            "error": str(e),
                            "error_type": type(e).__name__
                        }
                    }
                }
                st.session_state.api_logs.append(error_log)
                # 儲存到 localStorage
                save_to_localStorage('lisa_chat_api_logs', st.session_state.api_logs)
