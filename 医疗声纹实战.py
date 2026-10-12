import streamlit as st

# 1. 页面配置：设置宽屏模式，符合产品工作台的比例
st.set_page_config(layout="wide", page_title="医疗声纹转写工作台")

# 2. 注入自定义CSS，实现三种状态的标签视觉（这是老师最看重的地方）
st.markdown("""
<style>
    /* 绿色实心标签 */
    .tag-doctor {
        background-color: #28a745;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 14px;
        display: inline-block;
        margin-right: 10px;
    }
    /* 灰色虚线标签 */
    .tag-ai {
        border: 2px dashed #8899a6;
        color: #8899a6;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 14px;
        display: inline-block;
        margin-right: 10px;
    }
    /* 黄色高亮标签 */
    .tag-pending {
        background-color: #ffc107;
        color: #333333;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 14px;
        display: inline-block;
        margin-right: 10px;
    }
    /* 对话气泡基础样式 */
    .chat-text {
        font-size: 16px;
        color: #333333;
        line-height: 2.2;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid #f0f0f0;
    }
    /* 右侧角色投放框 */
    .role-box {
        border: 2px dashed #cccccc;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
        font-weight: bold;
        color: #555555;
        background-color: #f9f9f9;
        cursor: pointer;
    }
    .role-box:hover {
        border-color: #007bff;
        color: #007bff;
        background-color: #e6f2ff;
    }
</style>
""", unsafe_allow_html=True)

# 3. 初始化对话数据（使用 session_state 存储状态，模拟真实交互）
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"id": 1, "text": "你哪里不舒服？", "status": "doctor", "label": "医生（张医生）"},
        {"id": 2, "text": "我头痛三天了，一直不见好。", "status": "ai", "label": "Speaker1（AI推断，请确认）"},
        {"id": 3, "text": "之前有没有吃过什么药？", "status": "doctor", "label": "医生（张医生）"},
        {"id": 4, "text": "家里有布洛芬，吃了一次不管用。", "status": "pending", "label": "Speaker1（待识别）"}
    ]

# 4. 定义三个主列
col_audio, col_transcript, col_role = st.columns([1.2, 2.5, 1])

# ================= 左侧：音频波形控制区 =================
with col_audio:
    st.subheader("🎙️ 音频与波形")
    # 用折线图模拟音频波形
    import pandas as pd
    import numpy as np
    chart_data = pd.DataFrame(np.random.randn(50, 1), columns=["Wave"])
    st.line_chart(chart_data, height=150)
    st.caption("🔊 01:23 / 05:40")
    st.button("▶️ 播放 / ⏸️ 暂停", use_container_width=True)

# ================= 中间：对话转写流 =================
with col_transcript:
    st.subheader("📝 对话转写流")
    
    # 遍历数据渲染对话
    for msg in st.session_state.messages:
        html_content = f"""
        <div class="chat-text">
            <span class="tag-{msg['status']}">{msg['label']}</span>
            {msg['text']}
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)

# ================= 右侧：角色投放框（模拟修正交互） =================
with col_role:
    st.subheader("🎯 角色修正面板")
    
    # 下拉框选择要修正的对话
    msg_options = {f"第 {m['id']} 句: {m['text'][:10]}...": m['id'] for m in st.session_state.messages}
    selected_msg_label = st.selectbox("选择需要修正的对话：", list(msg_options.keys()))
    selected_id = msg_options[selected_msg_label]
    
    st.markdown("---")
    st.write("将以下选中项拖拽/点击指定为：")
    
    # 两个大按钮模拟投放框
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("👨‍⚕️ 医生", use_container_width=True):
            for msg in st.session_state.messages:
                if msg['id'] == selected_id:
                    msg['status'] = 'doctor'
                    msg['label'] = '医生（张医生）'
            st.rerun() # 刷新页面，改变标签颜色

    with col_btn2:
        if st.button("🤒 患者方", use_container_width=True):
            for msg in st.session_state.messages:
                if msg['id'] == selected_id:
                    msg['status'] = 'pending' # 这里为了颜色好看，暂时复用黄色高亮代表患者
                    msg['label'] = '患者方'
            st.rerun()

    st.info("💡 提示：低置信度（灰色虚线）和待识别（黄色高亮）标签必须确认后才能归档。")