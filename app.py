import streamlit as st
import google.generativeai as genai
import os

# --- 1. 页面基础配置 ---
st.set_page_config(
    page_title="基金从业必胜 - 智能出题系统",
    page_icon="📝",
    layout="wide"
)

# --- 2. 获取 API Key ---
# 优先从系统环境变量获取，如果没有，尝试从 Streamlit Secrets 获取
api_key = os.environ.get("GOOGLE_API_KEY")

# 如果都没有，给用户一个手动输入框（方便调试，部署时建议删掉这部分）
if not api_key:
    with st.sidebar:
        st.warning("⚠️ 未检测到环境变量。")
        api_key = st.text_input("请输入你的 Google API Key:", type="password")

if not api_key:
    st.error("❌ 请配置 GOOGLE_API_KEY 才能开始使用。")
    st.stop()

# --- 3. 配置 Google AI 模型 ---
genai.configure(api_key=api_key)

# ★★★ 核心修改：植入你的“命题专家”系统指令 ★★★
system_prompt = """
你是一位资深的【基金从业资格考试命题专家】。
你的任务是根据用户的要求，生成高质量的单项选择题。

出题原则：
1. 【严谨性】：题目必须符合中国基金从业真实考试难度，严禁常识性错误。
2. 【格式规范】：每道题必须包含 A、B、C、D 四个选项。
3. 【详细解析】：必须提供正确答案，并对每个选项进行解析（为什么对，为什么错）。
4. 【引用法规】：如果题目涉及法律法规，请在解析中引用相关法条。
5. 【排版】：请使用 Markdown 格式，让重点清晰可见。
"""

# 初始化模型
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=system_prompt
)

# --- 4. 界面设计 (UI) ---
st.title("🎓 基金从业资格考试 - 智能模拟出题")
st.markdown("选择科目和题目数量，AI 命题专家将为你实时生成考题。")

# 创建两列布局
col1, col2 = st.columns(2)

with col1:
    # 考试科目选择
    subject = st.selectbox(
        "请选择考试科目：",
        [
            "科目一：基金法律法规、职业道德与业务规范",
            "科目二：证券投资基金基础知识",
            "科目三：私募股权投资基金基础知识",
            "自定义科目（请在下方备注中说明）"
        ]
    )

with col2:
    # 题目数量滑动条 (限制在 1-10 题，防止生成超时)
    count = st.slider("生成题目数量：", min_value=1, max_value=10, value=3)

# 补充说明（可选）
extra_req = st.text_input("有没有特定的考点想重点练？(例如：内幕交易、久期计算)", placeholder="留空则随机出题")

# --- 5. 生成逻辑 ---
if st.button("开始出题 🚀", type="primary"):
    
    # 拼接最终发送给 AI 的指令
    user_prompt = f"""
    请根据以下要求出题：
    1. 科目内容：{subject}
    2. 题目数量：{count} 道单项选择题
    3. 重点考查范围：{extra_req if extra_req else "覆盖该科目的核心高频考点"}
    
    请严格按照单选题格式输出，并附带详细解析。
    """

    # 显示加载状态
    with st.spinner(f"正在调取题库，生成 {count} 道【{subject}】考题中..."):
        try:
            # 调用 AI
            response = model.generate_content(user_prompt)
            
            # 显示结果
            st.divider()
            st.subheader("📝 模拟试题")
            st.markdown(response.text)
            
            # 成功提示
            st.success("出题完成！请仔细阅读解析。")
            
        except Exception as e:
            st.error(f"出题失败，请检查网络或 Key。错误信息: {e}")

# --- 底部版权 ---
st.markdown("---")
st.caption("🤖 Powered by Google Gemini 1.5 Flash | 基金从业必胜系统")