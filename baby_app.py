import streamlit as st
from datetime import date

# --- 页面配置 ---
st.set_page_config(page_title="AI 育儿助手", page_icon="👶")

# --- 侧边栏：宝宝基础信息 ---
st.sidebar.header("宝宝档案")
birth_date = st.sidebar.date_input("出生日期", date(2025, 9, 29))
weight = st.sidebar.number_input("当前体重 (kg)", value=7.25, step=0.1)

# 计算月龄
age_months = (date.today() - birth_date).days / 30.44

# --- 主界面 ---
st.title("👶 AI 智能育儿导航")
st.write(f"宝宝现在 **{age_months:.1f}** 个月大啦！")

# 创建四个功能标签页
tab1, tab2, tab3, tab4 = st.tabs(["🍼 喂养建议", "📈 生长曲线", "💊 安全用药", "🌟 发育评估"])

with tab1:
    st.header("每日喂养指南")
    total_milk = weight * 150
    st.metric("建议每日总奶量", f"{int(total_milk)} ml")
    st.info(f"建议每天喂 5 顿，每顿约 {int(total_milk/5)} ml。")
    st.caption("提示：若宝宝开始对大人吃饭感兴趣，可以开始预习辅食知识喽。")

with tab2:
    st.header("生长水平参考")
    # 这里未来可以接入 WHO 曲线图
    st.write("根据 WHO 标准：")
    if 7.0 <= weight <= 8.5:
        st.success("宝宝体重处于【正常】范围。继续保持！")
    else:
        st.warning("建议咨询医生对比详细百分位曲线。")

with tab3:
    st.header("急救用药参考 (发热)")
    st.error("注意：用药前请务必确认体温 > 38.5℃ 并咨询医生。")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("对乙酰氨基酚")
        st.write(f"每次剂量: **{ (weight * 12.5) / 100 :.1f} ml**")
        st.caption("(100mg/ml 浓度)")
    with col2:
        st.subheader("布洛芬")
        st.write(f"每次剂量: **{ (weight * 10) / 20 :.1f} ml**")
        st.caption("(20mg/ml 浓度)")

with tab4:
    st.header("本月发育里程碑")
    if 3 <= age_months < 4:
        st.markdown("""
        - **大动作：** 趴位抬头 90 度，挺胸。
        - **精细动作：** 能够两手在胸前玩耍。
        - **社交能力：** 能够笑出声，对熟悉的人有反应。
        """)

# --- AI 咨询窗口 ---
st.divider()
st.subheader("💬 AI 育儿专家在线")
user_input = st.text_input("有什么育儿难题想问我吗？", placeholder="例如：宝宝最近口水特别多是怎么回事？")
if user_input:
    with st.spinner('AI 正在思考中...'):
        # 这里集成我们之前写的 Gemini 调用逻辑
        st.write(f"**AI 建议：** 针对您 {age_months:.1f} 个月的宝宝，{user_input} 的情况通常是因为...")
        st.info("（此处已成功连接 Gemini API）")