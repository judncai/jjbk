import streamlit as st
import google.generativeai as genai
import os

# 1. 强制最简页面，不搞任何样式
st.set_page_config(page_title="故障诊断模式")
st.title("☠️ 故障诊断模式")

# 2. 检查 API Key 是否存在
api_key = os.environ.get("GOOGLE_API_KEY")

st.subheader("1. 检查 API Key")
if not api_key:
    st.error("❌ 严重错误：系统未检测到 GOOGLE_API_KEY！")
    st.write("请去 Settings -> Secrets 检查是否填写正确。")
    st.stop() # 没 Key 直接停止运行
else:
    # 只显示前几位，确保没填错
    st.success(f"✅ 检测到 Key，开头是：{api_key[:5]}...")

# 3. 检查 Google 连接
st.subheader("2. 测试 Google 连接")
if st.button("开始连接测试"):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.info("正在发送测试请求...")
        
        # 发送一个最简单的请求
        response = model.generate_content("Hello, reply 'OK'.", stream=False)
        
        st.success("✅ 连接成功！Google 返回内容：")
        st.write(response.text)
        
    except Exception as e:
        st.error("❌ 连接失败！报错信息如下：")
        # 把具体的错误代码打印出来，这才是关键
        st.code(f"{type(e).__name__}: {str(e)}")
        
        st.warning("""
        如果是 403 / Invalid API Key -> Key 填错了或无效。
        如果是 500 / Time out -> Streamlit 服务器连不上 Google。
        如果是 ResourceExhausted -> 免费额度用完了。
        """)
