import streamlit as st
import google.generativeai as genai
import os
import time

# --- 1. 页面配置 (必须在第一行) ---
st.set_page_config(
    page_title="基金从业必胜系统",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. 注入 CSS (美化界面的核心) ---
# 这段代码会让你的界面看起来像 AI Studio 那样有卡片感
st.markdown("""
<style>
    /* 全局字体和背景 */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* 标题样式 */
    h1 {
        color: #1E1E1E;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* 模拟“卡片”效果 */
    .css-1r6slb0, .stColumn {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #E0E0E0;
    }
    
    /* 按钮样式 */
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
    }
    
    /* 成功提示框 */
    .stSuccess {
        background-color: #D1FAE5;
        border-left: 5px solid #10B981;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 侧边栏：API Key 配置与检查 ---
with st.sidebar:
    st.header("🔧 系统设置")
    # 优先从 Secrets 读取 Key，读不到才显示输入框
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        st.error("⚠️ 未检测到 API Key！")
        st.info("请在 Streamlit 部署页面的 'Settings' -> 'Secrets' 中配置 GOOGLE_API_KEY")
        # 紧急备用输入框
        api_key = st.text_input("或在此临时输入 Key:", type="password")
    else:
        st.success("✅ API Key 已连接")

# --- 4. 界面布局 (模仿 AI Studio) ---

# 顶部标题区
st.title("🏆 基金从业必胜系统")
st.caption("AI 智能组卷 | 实时解析 | 考点覆盖")

st.divider()

# 使用三列布局模仿“科目卡片”
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📘 科目一")
    st.markdown("**基金法律法规**")
    st.markdown("职业道德与业务规范")
    if st.button("进入科目一练习"):
        st.session_state['subject'] = "科目一：基金法律法规、职业道德与业务规范"

with col2:
    st.markdown("### 📗 科目二")
    st.markdown("**证券投资基金基础**")
    st.markdown("权益、固收、衍生品")
    if st.button("进入科目二练习"):
        st.session_state['subject'] = "科目二：证券投资基金基础知识"

with col3:
    st.markdown("### 💎 科目三")
    st.markdown("**私募股权投资基金**")
    st.markdown("运作流程、法律监管")
    if st.button("进入科目三练习"):
        st.session_state['subject'] = "科目三：私募股权投资基金基础知识"

# --- 5. 核心出题区 ---
st.divider()

# 检查用户是否选了科目
if 'subject' not in st.session_state:
    st.info("👆 请点击上方卡片，选择一个科目开始练习")
else:
    target_subject = st.session_state['subject']
    st.subheader(f"📝 当前练习：{target_subject}")
    
    # 题目数量控制
    q_count = st.slider("生成题目数量 (建议 3 题以防超时)", 1, 5, 3)
    
    if st.button(f"🚀 开始生成 {q_count} 道真题", type="primary"):
        
        # 1. 检查 Key
        if not api_key:
            st.error("❌ 无法运行：缺少 API Key。请检查侧边栏设置。")
            st.stop()
            
        # 2. 配置 AI
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 3. 状态显示 (解决“没反应”的问题)
        status_box = st.status("正在连接 AI 大脑...", expanded=True)
        
        try:
            status_box.write("正在构建题库逻辑...")
            prompt = f"""
            你是一位基金从业资格考试专家。请为【{target_subject}】生成 {q_count} 道单项选择题。
            要求：
            1. 题目难度符合真实考试。
            2. 必须包含 A/B/C/D 选项。
            3. 每道题后必须紧跟【答案解析】。
            4. 使用 Markdown 格式。
            """
            
            status_box.write("正在请求 Google Gemini 生成内容 (请稍候 10-20 秒)...")
            
            # 流式生成 (打字机效果)
            response = model.generate_content(prompt, stream=True)
            
            placeholder = st.empty()
            full_text = ""
            
            for chunk in response:
                full_text += chunk.text
                placeholder.markdown(full_text + "▌")
            
            placeholder.markdown(full_text)
            
            status_box.update(label="✅ 出题完成！", state="complete", expanded=False)
            
        except Exception as e:
            status_box.update(label="❌ 出错了", state="error")
            st.error(f"错误详情：{e}")
            st.warning("如果显示 403 错误，通常是 API Key 无效。如果显示 500，通常是网络波动，请重试。")
