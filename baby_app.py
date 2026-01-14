import streamlit as st
from datetime import date

# --- 1. 界面设计 ---
st.set_page_config(page_title="萌宝导航 - 纯净版", page_icon="👶")

st.markdown("""
    <style>
    .stApp { background-color: #FDFCFB; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #F8F9FA;
        border-radius: 10px 10px 0px 0px;
        padding: 10px;
    }
    .main-header { color: #E88D67; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 侧边栏 ---
st.sidebar.header("👶 宝宝档案")
birth_date = st.sidebar.date_input("出生日期", date(2025, 9, 29))
current_weight = st.sidebar.number_input("当前体重 (kg)", value=7.25, step=0.1)

# 计算月龄
age_days = (date.today() - birth_date).days
age_months = age_days / 30.44

st.markdown(f"<h1 class='main-header'>萌宝成长导航</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align: center;'>宝宝今天 <b>{int(age_months)}</b> 个月 <b>{int(age_days % 30.44)}</b> 天大啦！</p>", unsafe_allow_html=True)

# --- 3. 核心功能 ---
tab1, tab2, tab3, tab4 = st.tabs(["🍼 喂养建议", "📈 生长指标", "💊 用药参考", "📝 发育打卡"])

with tab1:
    st.header("奶量计算 (150ml/kg法)")
    total_milk = current_weight * 150
    st.metric("建议每日总奶量", f"{int(total_milk)} ml")
    
    col1, col2 = st.columns(2)
    col1.write("**分餐建议：**")
    col1.write("- 5 顿制: 每顿约 " + str(int(total_milk/5)) + " ml")
    col1.write("- 6 顿制: 每顿约 " + str(int(total_milk/6)) + " ml")
    
    st.info("💡 此时期宝宝视力范围扩大，喂奶时容易被周围吸引，建议在安静阴暗的环境下喂哺。")

with tab2:
    st.header("WHO 生长曲线对比")
    # 简单的 WHO 男婴 3-4 月体重参考
    st.write("根据 WHO 标准，3.5 个月男婴体重范围：")
    st.write("- **偏瘦：** < 5.8 kg")
    st.write("- **标准：** 5.8 kg - 7.5 kg")
    st.write("- **壮硕：** > 7.5 kg")
    
    if current_weight > 7.5:
        st.success(f"当前体重 {current_weight}kg：长势喜人，超过了 85% 的同龄宝宝！")
    elif current_weight < 5.8:
        st.warning(f"当前体重 {current_weight}kg：偏轻，建议咨询医生是否需要增加喂养频率。")
    else:
        st.success(f"当前体重 {current_weight}kg：处于非常完美的标准区间！")
    
    

with tab3:
    st.header("家庭常备药剂量 (发热用)")
    st.error("⚠️ 仅用于体温 > 38.5℃ 情况。剂量随体重实时计算，请严格核对浓度！")
    
    st.subheader("1. 对乙酰氨基酚 (如泰诺林)")
    st.info(f"浓度 100mg/ml：每次建议滴入 **{(current_weight * 12.5) / 100:.1f} ml**")
    
    st.subheader("2. 布洛芬 (如美林)")
    st.info(f"浓度 20mg/ml：每次建议喂入 **{(current_weight * 10) / 20:.1f} ml**")
    
    st.caption("注：两次给药需间隔 4-6 小时，24小时内不超过 4 次。")

with tab4:
    st.header(f"{int(age_months)}个月里程碑自测")
    checklist = [
        "趴着时能稳稳抬头 90 度吗？",
        "会寻找声音的来源吗？",
        "能够自发地微笑吗？",
        "视线能随着移动的物体转动吗？"
    ]
    
    score = 0
    for item in checklist:
        if st.checkbox(item):
            score += 1
    
    progress = score / len(checklist)
    st.progress(progress)
    st.write(f"完成度：{int(progress * 100)}%")
    
    if score == len(checklist):
        st.balloons()
        st.success("宝宝发育超标！继续加油！")

st.divider()
st.caption("© 2026 萌宝导航 - 妈妈的私人育儿小助手")