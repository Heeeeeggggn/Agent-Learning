import streamlit as st
import json
import os
from main import app
from memory import update_memory

# ===== 路径 =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_PATH = os.path.join(BASE_DIR, "memory.json")

st.set_page_config(page_title="学习规划助手")

# ===== 标题 =====
st.title("AI学习规划助手")
st.caption("由智能 Agent 驱动，为你定制专属学习计划")

# ===== 初始化聊天记录 =====
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===== 展示聊天 =====
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ===== 输入 =====
user_input = st.chat_input("请输入你的学习需求...")

if user_input:
    # 显示用户消息
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # ===== 调用 Agent =====
    with st.spinner("正在为你生成学习规划..."):
        result = app.invoke({
            "input": user_input
    })

    reply = result.get("plan") or result.get("response") or "我还没理解你的意思"

    # ===== 显示 AI 回复 =====
    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    # ===== 自动写入记忆 =====
    if reply:
        update_memory("last_plan", reply)

