import streamlit as st

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="Thai MSW Analytics",
    page_icon="🇹🇭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# Custom CSS
# =========================
st.markdown("""
<style>
    .main-title {
        font-size: 40px;
        font-weight: 700;
        margin-bottom: 0px;
        color: #1f2937;
    }

    .subtitle {
        font-size: 18px;
        color: #4b5563;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 15px;
        color: #111827;
    }

    .card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        background-color: #ffffff;
        height: 100%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    .card h3 {
        margin-top: 0;
        font-size: 19px;
        color: #1f2937;
    }

    .card p {
        color: #6b7280;
        font-size: 14px;
        line-height: 1.5;
        margin-bottom: 0;
    }

    /* ปรับปรุงส่วน Feature Box ให้มีความสูงเท่ากันทุกกล่อง */
    .feature-box {
        padding: 20px 16px;
        border-radius: 12px;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        text-align: center;
        height: 160px; /* ล็อกความสูงให้เท่ากันเป๊ะ */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .feature-number {
        font-size: 26px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .feature-label {
        font-weight: 600;
        color: #334155;
        font-size: 14px;
        margin-bottom: 4px;
    }

    .feature-desc {
        color: #64748b;
        font-size: 12px;
        margin: 0;
        line-height: 1.3;
    }

    .footer {
        text-align: center;
        color: #9ca3af;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #e5e7eb;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# Header
# =========================
st.markdown('<div class="main-title">🇹🇭 Thai MSW Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">ระบบวิเคราะห์ข้อมูลขยะมูลฝอยประเทศไทย</div>', unsafe_allow_html=True)
st.markdown("---")


# =========================
# Introduction
# =========================
st.markdown('<div class="section-title">📊 ภาพรวมระบบ</div>', unsafe_allow_html=True)
st.write("""
ระบบนี้รวบรวมและนำเสนอข้อมูลขยะมูลฝอยของประเทศไทยในรูปแบบ Interactive Dashboard 
เพื่อช่วยให้ผู้ใช้งานสามารถสำรวจข้อมูล วิเคราะห์แนวโน้ม เปรียบเทียบพื้นที่ 
และศึกษาความสัมพันธ์ของข้อมูล รวมถึงการประยุกต์ใช้ Machine Learning 
สำหรับการพยากรณ์ข้อมูลในอนาคตอย่างมีประสิทธิภาพ
""")


# =========================
# Quick Features (Grid Layout)
# =========================
st.markdown('<div class="section-title">✨ ฟังก์ชันหลักของระบบ</div>', unsafe_allow_html=True)

cols = st.columns(4)
features = [
    ("📈", "วิเคราะห์แนวโน้ม", "ศึกษาการเปลี่ยนแปลงปริมาณขยะตามช่วงเวลา"),
    ("🗺️", "วิเคราะห์เชิงพื้นที่", "เปรียบเทียบข้อมูลขยะระหว่างจังหวัดและภูมิภาค"),
    ("🔍", "สำรวจข้อมูล", "ค้นหาและตรวจสอบข้อมูลในรูปแบบ Interactive"),
    ("🤖", "Machine Learning", "วิเคราะห์และพยากรณ์ข้อมูลขยะในอนาคต")
]

for col, (icon, label, desc) in zip(cols, features):
    with col:
        st.markdown(f"""
        <div class="feature-box">
            <div class="feature-number">{icon}</div>
            <div class="feature-label">{label}</div>
            <p class="feature-desc">{desc}</p>
        </div>
        """, unsafe_allow_html=True)


# =========================
# Navigation Guide
# =========================
st.markdown('<div class="section-title">🧭 เมนูการใช้งาน</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h3>🏠 ภาพรวมประเทศไทย</h3>
        <p>แสดงภาพรวมข้อมูลขยะมูลฝอยของประเทศไทย พร้อมสถิติสำคัญและข้อมูลสรุปในแต่ละปี</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("") # เว้นระยะห่างเล็กน้อย
    
    st.markdown("""
    <div class="card">
        <h3>🗺️ การกระจายตัว</h3>
        <p>วิเคราะห์การกระจายตัวของปริมาณขยะในแต่ละจังหวัดและภูมิภาค เพื่อให้เห็นความแตกต่างเชิงพื้นที่</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    st.markdown("""
    <div class="card">
        <h3>🤖 Machine Learning</h3>
        <p>ใช้โมเดล Machine Learning เพื่อวิเคราะห์รูปแบบข้อมูลและพยากรณ์แนวโน้มปริมาณขยะในอนาคต</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>📈 วิเคราะห์แนวโน้ม</h3>
        <p>วิเคราะห์แนวโน้มของปริมาณขยะตามช่วงเวลา พร้อมกราฟแสดงการเปรียบเทียบข้อมูลในแต่ละปี</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    st.markdown("""
    <div class="card">
        <h3>🔍 สำรวจข้อมูล</h3>
        <p>เลือกข้อมูลและตัวแปรที่ต้องการวิเคราะห์ได้อย่างอิสระ เหมาะสำหรับการสำรวจ Dataset เชิงลึก</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    st.info("💡 **เริ่มต้นใช้งาน:** เลือกเมนูการทำงานที่ต้องการจากแถบ Sidebar ทางด้านซ้ายมือได้เลยครับ")


# =========================
# Footer
# =========================
st.markdown("""
<div class="footer">
    🇹🇭 Thai MSW Analytics System<br>
    ระบบสนับสนุนการบริหารจัดการและวิเคราะห์ข้อมูลขยะมูลฝอยประเทศไทย
</div>
""", unsafe_allow_html=True)