#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from openai import OpenAI
import os
import sys

def main():
    """
    OpenAI 互動式聊天程式（使用 Responses API）
    使用方法：
    1. 設定環境變數 OPENAI_API_KEY
    2. 在 OpenAI 平台建立 Prompt 並取得 Prompt ID
    3. 將 Prompt ID 和版本號填入下方的 PROMPT_ID 和 PROMPT_VERSION
    4. 執行此程式
    5. 輸入訊息與 AI 對話
    6. 輸入 'exit' 或 'quit' 離開
    """

    # ⚠️ 請在 OpenAI 平台建立 Prompt 後，將 ID 和版本號填入這裡
    PROMPT_ID = "pmpt_68f663c9400081968c77a12c68f176e80438728839e32f32"  # 請替換成你的 Prompt ID
    PROMPT_VERSION = "4"  # 請替換成你的 Prompt 版本號

    # 初始化 OpenAI 客戶端
    # 確保已設定 OPENAI_API_KEY 環境變數
    try:
        client = OpenAI()
    except Exception as e:
        print(f"❌ 錯誤：無法初始化 OpenAI 客戶端")
        print(f"請確保已設定環境變數 OPENAI_API_KEY")
        print(f"設定方法：export OPENAI_API_KEY='your-api-key'")
        print(f"\n詳細錯誤：{e}")
        sys.exit(1)

    # 對話歷史記錄（用於顯示和管理對話）
    conversation_history = []

    print("=" * 80)
    print("🤖 OpenAI 聊天程式 (Responses API)")
    print("=" * 80)
    print(f"📝 使用 Prompt ID: {PROMPT_ID[:20]}...")
    print(f"📌 版本: {PROMPT_VERSION}")
    print("=" * 80)
    print("輸入 'exit' 或 'quit' 離開")
    print("輸入 'clear' 清除對話歷史")
    print("輸入 'history' 查看對話歷史")
    print("=" * 80)
    print()

    while True:
        # 取得使用者輸入
        try:
            user_input = input("👤 您: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 再見！")
            break

        # 檢查特殊命令
        if user_input.lower() in ['exit', 'quit', '離開', '退出']:
            print("\n👋 再見！")
            break

        if user_input.lower() in ['clear', '清除']:
            conversation_history = []
            print("✅ 對話歷史已清除\n")
            continue

        if user_input.lower() in ['history', '歷史']:
            print("\n📜 對話歷史：")
            for idx, msg in enumerate(conversation_history, 1):
                role = "👤 您" if msg['role'] == 'user' else "🤖 AI"
                print(f"{idx}. {role}: {msg['content'][:100]}...")
            print()
            continue

        if not user_input:
            continue

        # 將使用者訊息加入歷史
        conversation_history.append({
            "role": "user",
            "content": user_input
        })

        try:
            # 呼叫 OpenAI Responses API
            print("\n🤖 AI 正在思考中...\n")

            # Responses API 使用 prompt 模板和 input 參數
            response = client.responses.create(
                prompt={
                    "id": PROMPT_ID,
                    "version": PROMPT_VERSION
                },
                input=user_input
            )

            # 取得 AI 回應
            # Responses API 回傳一個 Response 物件
            ai_message = ""

            # Response 物件可能有不同的屬性來存放實際內容
            # 常見的屬性有: output, data, items, content
            response_items = []

            # 嘗試不同的方式獲取內容
            if hasattr(response, 'output'):
                # 如果有 output 屬性，可能是列表或字串
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

            # 如果已經取得字串，就不用繼續解析
            if not ai_message and response_items:
                # 遍歷回應項目，找到 message 類型的輸出
                for item in response_items:
                    # 檢查是否為 message 類型且狀態為 completed
                    if (hasattr(item, 'type') and item.type == 'message' and
                        hasattr(item, 'status') and item.status == 'completed'):

                        if hasattr(item, 'content') and item.content:
                            # content 是一個列表，提取所有文字內容
                            for content_item in item.content:
                                if hasattr(content_item, 'type') and content_item.type == 'output_text':
                                    if hasattr(content_item, 'text'):
                                        ai_message += content_item.text

            # 如果還是沒有取得內容，嘗試直接轉字串（可能是簡單文字回應）
            if not ai_message:
                # 顯示可用的屬性以便除錯
                available_attrs = [attr for attr in dir(response) if not attr.startswith('_')]
                print(f"⚠️ 無法解析 AI 回應")
                print(f"回應類型: {type(response)}")
                print(f"可用屬性: {available_attrs[:10]}")  # 只顯示前 10 個

                # 嘗試直接取得字串表示
                if hasattr(response, '__str__'):
                    ai_message = str(response)
                else:
                    ai_message = "[無法取得回應內容]"

            # 將 AI 回應加入歷史
            conversation_history.append({
                "role": "assistant",
                "content": ai_message
            })

            # 顯示 AI 回應
            print(f"🤖 AI: {ai_message}\n")
            print("-" * 80)
            print()

        except Exception as e:
            print(f"❌ 錯誤：{e}\n")
            print(f"💡 提示：請確保已在 OpenAI 平台建立 Prompt，並正確設定 PROMPT_ID 和 PROMPT_VERSION")
            # 如果發生錯誤，移除最後加入的使用者訊息
            conversation_history.pop()

if __name__ == "__main__":
    main()
