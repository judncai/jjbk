import streamlit as st
import google.generativeai as genai
import os
import time

# --- 1. 页面美化配置 ---
st.set_page_config(
    page_title="基金从业必胜 | 智能刷题",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义简单的 CSS 让界面稍微好看一点点
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        height: 3em;
    }
    .reportview-container {
        background: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 配置 API ---
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ 缺少 API Key，请在 Streamlit Advanced Settings 中配置。")
    st.stop()

genai.configure(api_key=api_key)

system_prompt = """
你是一位资深的【基金从业资格考试命题专家】。
请生成单项选择题，格式要求：
1. 题目清晰。
2. A/B/C/D 四个选项。
3. 【答案解析】：先给出正确答案，再详细解释原因。
请使用 Markdown 格式，加粗重点。
"""
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)

# --- 3. 侧边栏控制区 ---
with st.sidebar:
    st.header("⚙️ 出题设置")
    count = st.slider("题目数量 (建议3-5题)", 1, 10, 3)  # 默认改小，提高速度感
    st.info("💡 提示：题目越多生成越慢，建议每次练 3 题。")

# --- 4. 主界面 ---
st.title("💸 基金从业资格 - 智能模拟实战")
st.caption("AI 实时命题 | 包含详细解析 | 考点覆盖")

col1, col2 = st.columns([2, 1])
with col1:
    subject = st.selectbox("选择科目", [
        "科目一：法律法规与职业道德",
        "科目二：证券投资基金基础知识",
        "科目三：私募股权投资基金"
    ])
with col2:
    focus = st.text_input("强化考点 (可选)", placeholder="例如：久期、内幕交易")

# --- 5. 核心逻辑：带流式输出 ---
if st.button("🔥 立即出题"):
    
    prompt = f"请为【{subject}】生成 {count} 道单选题。考点侧重：{focus if focus else '核心高频考点'}。"
    
    st.divider()
    
    # 这一步是关键：创建一个空容器，用来接收“打字机”效果
    response_container = st.empty()
    full_text = ""
    
    try:
        # 使用 stream=True 开启流式传输
        response = model.generate_content(prompt, stream=True)
        
        # 循环获取每一个字
        for chunk in response:
            full_text += chunk.text
            # 实时更新页面，让你看到字在动
            response_container.markdown(full_text + "▌")
            
        # 最后把光标去掉
        response_container.markdown(full_text)
        
        st.success("✅ 出题完毕！")
        
    except Exception as e:
        st.error(f"出题中断：{e}")
