import streamlit as st
from datetime import date
import google.generativeai as genai

# --- 1. 页面风格美化 (Marketing Branding) ---
st.set_page_config(page_title="萌宝导航 - AI 智能育儿", page_icon="👼")

st.markdown("""
    <style>
    .stApp {
        background-color: #FFF9F5; /* 暖米色背景 */
    }
    .st-emotion-cache-1cvow48 {
        border-radius: 15px; /* 圆角设计 */
    }
    h1 {
        color: #FF8C94; /* 珊瑚粉色标题 */
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 侧边栏及基础逻辑 ---
st.sidebar.header("👶 宝宝档案")
# 默认填入你宝宝的信息
birth_date = st.sidebar.date_input("出生日期", date(2025, 9, 29))
current_weight = st.sidebar.number_input("当前体重 (kg)", value=7.25, step=0.1)
api_key = st.sidebar.text_input("填入你的 Gemini API Key", type="password")

# 计算月龄
today = date.today()
age_days = (today - birth_date).days
age_months = age_days / 30.44

st.title("👼 萌宝成长导航")
st.subheader(f"宝宝今天 {int(age_months)} 个月 {int(age_days % 30.44)} 天大啦！")

# --- 3. 核心功能标签页 ---
tab1, tab2, tab3, tab4 = st.tabs(["🍼 科学喂养", "📈 生长曲线", "💊 安全用药", "📝 发育自测"])

with tab1:
    st.header("奶量计算器")
    total_milk = current_weight * 150
    col1, col2 = st.columns(2)
    col1.metric("建议总奶量", f"{int(total_milk)} ml")
    col2.metric("建议餐数", "5 顿")
    st.write(f"建议每顿奶量约为 **{int(total_milk/5)} ml**。")
    st.info("💡 3-4个月宝宝可能会进入厌奶期，如果精神好、尿布满，不要过度焦虑哦。")

with tab2:
    st.header("WHO 生长百分位参考")
    # 模拟 WHO 3个月男婴标准：中位数约为 6.4kg，85%约为 7.2kg
    if current_weight > 7.0:
        st.success(f"宝宝当前体重 {current_weight}kg，处于同龄宝宝的**前 15% (壮硕型)**，长得真棒！")
    else:
        st.info("宝宝体重处于标准中位数水平，非常健康。")
    st.caption("注：此数据基于 WHO 0-6月生长标准。")
    

with tab3:
    st.header("急救用药（发热 38.5℃+）")
    st.warning("⚠️ 剂量严格按体重计算，请务必核对包装浓度！")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("对乙酰氨基酚")
        st.code(f"每次: {(current_weight * 12.5) / 100:.1f} ml", language=None)
        st.caption("参考泰诺林(100mg/ml)")
    with c2:
        st.subheader("布洛芬")
        st.code(f"每次: {(current_weight * 10) / 20:.1f} ml", language=None)
        st.caption("参考美林(20mg/ml)")

with tab4:
    st.header("3-4个月发育里程碑")
    checklist = [
        "俯卧时能否抬头 90 度并用手臂撑起？",
        "是否会大声笑出声？",
        "小手是否能主动抓握面前的玩具？",
        "视线是否能灵活追随移动的物体？"
    ]
    for item in checklist:
        st.checkbox(item)
    if st.button("生成发育简报"):
        st.write("🎉 太棒了！宝宝正在按节奏探索世界，记得多和宝宝说话哦。")

# --- 4. 接入 AI 大脑 ---
st.divider()
st.subheader("💬 育儿专家 AI 咨询")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    user_q = st.text_input("有什么想问专家的？", placeholder="比如：宝宝最近总流口水是要长牙吗？")
    if user_q:
        with st.spinner("专家正在查阅资料..."):
            system_prompt = f"你是一个温柔的育儿专家。针对一个{int(age_months)}个月大、体重{current_weight}kg的宝宝，回答妈妈的问题：{user_q}"
            response = model.generate_content(system_prompt)
            st.write("---")
            st.write(f"**专家建议：**\n\n{response.text}")
else:
    st.info("🔑 请在左侧边栏输入你的 Gemini API Key 以激活 AI 对话功能。")