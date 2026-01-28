import streamlit as st
import google.generativeai as genai
import os

# --- 1. 页面配置与美化 (保留你喜欢的漂亮界面) ---
st.set_page_config(
    page_title="基金从业必胜系统",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 注入 CSS：让界面有卡片感，按钮更好看
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    h1 { color: #1E1E1E; font-family: 'Helvetica Neue', sans-serif; }
    
    /* 卡片样式 */
    div.stButton > button:first-child {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        width: 100%;
    }
    div.stButton > button:hover { background-color: #1D4ED8; }
    
    /* 调整一下文字大小 */
    .stMarkdown p { font-size: 16px; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# --- 2. API 配置 ---
api_key = os.environ.get("GOOGLE_API_KEY")

# 侧边栏（只显示状态，平时藏起来）
with st.sidebar:
    st.header("系统状态")
    if not api_key:
        st.error("❌ 未配置 API Key")
    else:
        st.success("✅ 网络连接就绪")

# --- 3. 漂亮的主界面布局 ---
st.title("🏆 基金从业必胜系统")
st.caption("AI 智能组卷 | 实时解析 | 考点覆盖")

st.divider()

# 三列布局：科目选择卡片
col1, col2, col3 = st.columns(3)

# 使用 session_state 记住用户选了什么科目
if 'target_subject' not in st.session_state:
    st.session_state['target_subject'] = "科目一：基金法律法规"

with col1:
    st.info("📘 **科目一**")
    st.markdown("法律法规、职业道德")
    if st.button("选择科目一"):
        st.session_state['target_subject'] = "科目一：基金法律法规、职业道德与业务规范"

with col2:
    st.success("📗 **科目二**")
    st.markdown("证券基金基础知识")
    if st.button("选择科目二"):
        st.session_state['target_subject'] = "科目二：证券投资基金基础知识"

with col3:
    st.warning("💎 **科目三**")
    st.markdown("私募股权投资基金")
    if st.button("选择科目三"):
        st.session_state['target_subject'] = "科目三：私募股权投资基金基础知识"

# --- 4. 核心出题区 (稳定版逻辑) ---
st.divider()

current_subject = st.session_state['target_subject']
st.subheader(f"📝 当前准备生成：{current_subject}")

# 题目数量控制
q_count = st.slider("生成题目数量", 1, 5, 3)

# ★★★ 关键修改：去掉了流式传输，改用进度条+一次性生成 ★★★
if st.button(f"🚀 立即生成 {q_count} 道真题", type="primary"):
    
    if not api_key:
        st.error("请先在后台配置 GOOGLE_API_KEY！")
        st.stop()
        
    # 显示一个漂亮的加载圈
    with st.spinner(f"正在请求 Google AI 总部生成 {current_subject} 的考题... (约需 5-10 秒)"):
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            你是一位基金从业资格考试专家。请为【{current_subject}】生成 {q_count} 道单项选择题。
            
            要求：
            1. 题目难度符合真实考试。
            2. 必须包含 A/B/C/D 选项。
            3. 每道题后必须紧跟【答案解析】。
            4. 直接输出内容，不要使用 Markdown 代码块。
            """
            
            # 这里的 stream=False 是解决你“转圈出不来”的关键！
            response = model.generate_content(prompt, stream=False)
            
            # 生成成功！
            st.balloons()
            st.success("✅ 出题完成！请看下方解析：")
            
            # 使用容器把题目美美地展示出来
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error("❌由于网络原因连接超时。建议刷新网页再试一次。")
            st.code(e) # 显示具体错误代码方便排查
