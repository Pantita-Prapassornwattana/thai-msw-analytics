import streamlit as st

st.set_page_config(page_title="Thai MSW Analytics", page_icon="🇹🇭", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .main-title {
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 0px;
        background: -webkit-linear-gradient(45deg, #0ea5e9, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    .subtitle {
        font-size: 20px;
        color: var(--text-color);
        opacity: 0.8;
        margin-bottom: 30px;
        text-align: center;
        font-weight: 500;
    }
    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 20px;
        color: var(--text-color);
        border-bottom: 3px solid #0ea5e9;
        padding-bottom: 10px;
        display: inline-block;
    }
    .card {
        padding: 24px;
        border-radius: 16px;
        background-color: var(--background-color);
        border: 1px solid var(--secondary-background-color);
        border-left: 5px solid #0ea5e9;
        height: 100%;
        min-height: 160px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(14, 165, 233, 0.2);
        border-left: 5px solid #3b82f6;
    }
    .card h3 {
        margin-top: 0;
        font-size: 20px;
        color: var(--text-color);
    }
    .card p {
        color: var(--text-color);
        opacity: 0.8;
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 0;
        margin-top: auto;
    }
    .feature-box {
        padding: 24px 16px;
        border-radius: 16px;
        background-color: var(--secondary-background-color);
        border: 1px solid var(--secondary-background-color);
        text-align: center;
        height: 100%;
        min-height: 170px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: transform 0.2s ease;
    }
    .feature-box:hover {
        transform: scale(1.05);
    }
    .feature-number {
        font-size: 36px;
        margin-bottom: 10px;
    }
    .feature-label {
        font-weight: 700;
        color: var(--text-color);
        font-size: 16px;
        margin-bottom: 6px;
    }
    .feature-desc {
        color: var(--text-color);
        opacity: 0.7;
        font-size: 13px;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🇹🇭 Thai MSW Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">ระบบวิเคราะห์ข้อมูลขยะมูลฝอยประเทศไทยอัจฉริยะ</div>', unsafe_allow_html=True)

with st.container():
    st.info("👋 **ยินดีต้อนรับ!** เลือกเมนูจากแถบด้านซ้ายเพื่อเริ่มต้นใช้งานระบบ Dashboard ที่ออกแบบมาให้อ่านข้อมูลง่ายและรวดเร็ว")

st.markdown('<div class="section-title">✨ ฟังก์ชันหลักของระบบ</div>', unsafe_allow_html=True)

cols = st.columns(4)
features = [
    ("📈", "Trends", "วิเคราะห์แนวโน้มและอัตราการเติบโต YoY"),
    ("🗺️", "Spatial", "เปรียบเทียบพื้นที่ ค้นหา Hotspot จังหวัด"),
    ("🔍", "Explorer", "ค้นหา กรอง และส่งออกข้อมูลเป็น CSV"),
    ("🤖", "ML Analytics", "จัดกลุ่มพฤติกรรมจังหวัดด้วย AI")
]

for col, (icon, label, desc) in zip(cols, features):
    with col:
        st.markdown(f"""
        <div class="feature-box">
            <div class="feature-number">{icon}</div>
            <div class="feature-label">{label}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("---")

st.markdown('<div class="section-title">🧭 แนะนำเมนู (Select from Sidebar)</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="card">
        <h3>📊 ภาพรวมระบบ (Overview)</h3>
        <p>ดูภาพรวมปริมาณขยะ สัดส่วนการกำจัด และการแจ้งเตือนสถานะของระบบแบบ Real-time</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.markdown("""
    <div class="card">
        <h3>📍 การกระจายตัว (Spatial)</h3>
        <p>ใช้ Treemap สีสันโทนเขียวในการเจาะลึกปริมาณขยะแต่ละภูมิภาคและจังหวัดได้อย่างรวดเร็ว</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="card">
        <h3>📊 วิเคราะห์แนวโน้ม (Trends)</h3>
        <p>ดูกราฟเส้นและกราฟแท่งเปรียบเทียบขยะรายปี แยกสีชัดเจนเพื่อความเข้าใจในพริบตา</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.markdown("""
    <div class="card">
        <h3>🧠 ML Analytics & Explorer</h3>
        <p>เจาะลึกด้วย K-Means และตารางข้อมูลดิบที่มาพร้อมกับการดาวน์โหลดเพื่อใช้วิเคราะห์ต่อ</p>
    </div>
    """, unsafe_allow_html=True)