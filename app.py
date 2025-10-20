#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from openai import OpenAI
import os

# 設定頁面配置
st.set_page_config(
    page_title="AI 聊天助手",
    page_icon="🤖",
    layout="centered"
)

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
    prompt_version = st.secrets.get("PROMPT_VERSION", "5")
    return prompt_id, prompt_version

# 初始化
client = init_openai_client()
PROMPT_ID, PROMPT_VERSION = get_prompt_config()

# 初始化 session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 標題和說明
st.title("🤖 AI 聊天助手")
st.caption(f"使用 OpenAI Responses API | Prompt 版本: {PROMPT_VERSION}")

# 側邊欄功能
with st.sidebar:
    st.header("⚙️ 功能")

    if st.button("🗑️ 清除對話歷史", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("📊 對話統計")
    st.metric("訊息數量", len(st.session_state.messages))

    st.divider()

    st.subheader("ℹ️ 使用說明")
    st.markdown("""
    1. 在下方輸入框輸入訊息
    2. 按 Enter 或點擊發送
    3. AI 會根據設定的 Prompt 回應
    4. 可隨時清除對話記錄重新開始
    """)

# 顯示對話歷史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 聊天輸入框
if prompt := st.chat_input("輸入訊息..."):
    # 顯示使用者訊息
    with st.chat_message("user"):
        st.markdown(prompt)

    # 加入到對話歷史
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 顯示 AI 回應
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                # 呼叫 OpenAI Responses API
                response = client.responses.create(
                    prompt={
                        "id": PROMPT_ID,
                        "version": PROMPT_VERSION
                    },
                    input=prompt
                )

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

                # 顯示回應
                st.markdown(ai_message)

                # 加入到對話歷史
                st.session_state.messages.append({"role": "assistant", "content": ai_message})

            except Exception as e:
                error_msg = f"❌ 錯誤: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
