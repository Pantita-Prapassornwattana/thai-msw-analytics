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
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 20px;
        color: #666;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    .card {
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #e6e6e6;
        background-color: #ffffff;
        min-height: 180px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }

    .card h3 {
        margin-top: 0;
        font-size: 21px;
    }

    .card p {
        color: #666;
        line-height: 1.6;
    }

    .feature-box {
        padding: 20px;
        border-radius: 14px;
        background-color: #f7f9fc;
        border: 1px solid #e9edf3;
        text-align: center;
        min-height: 130px;
    }

    .feature-number {
        font-size: 30px;
        font-weight: 700;
    }

    .feature-label {
        color: #666;
        font-size: 15px;
    }

    .footer {
        text-align: center;
        color: #888;
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# Header
# =========================
st.markdown(
    '<div class="main-title">🇹🇭 Thai MSW Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">ระบบวิเคราะห์ข้อมูลขยะมูลฝอยประเทศไทย</div>',
    unsafe_allow_html=True
)

st.markdown("---")


# =========================
# Introduction
# =========================
st.markdown(
    '<div class="section-title">📊 ระบบวิเคราะห์ข้อมูลขยะมูลฝอย</div>',
    unsafe_allow_html=True
)

st.write("""
ระบบนี้รวบรวมและนำเสนอข้อมูลขยะมูลฝอยของประเทศไทยในรูปแบบ Interactive Dashboard
เพื่อช่วยให้ผู้ใช้งานสามารถสำรวจข้อมูล วิเคราะห์แนวโน้ม เปรียบเทียบพื้นที่
และศึกษาความสัมพันธ์ของข้อมูล รวมถึงการประยุกต์ใช้ Machine Learning
สำหรับการพยากรณ์ข้อมูลในอนาคต
""")


# =========================
# Quick Features
# =========================
st.markdown(
    '<div class="section-title">✨ ฟังก์ชันหลักของระบบ</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-number">📈</div>
        <div class="feature-label">วิเคราะห์แนวโน้ม</div>
        <p>ศึกษาการเปลี่ยนแปลงของปริมาณขยะตามช่วงเวลา</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-number">🗺️</div>
        <div class="feature-label">วิเคราะห์เชิงพื้นที่</div>
        <p>เปรียบเทียบข้อมูลขยะระหว่างจังหวัดและภูมิภาค</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-number">🔍</div>
        <div class="feature-label">สำรวจข้อมูล</div>
        <p>ค้นหาและตรวจสอบข้อมูลในรูปแบบ Interactive</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-number">🤖</div>
        <div class="feature-label">Machine Learning</div>
        <p>วิเคราะห์และพยากรณ์ข้อมูลขยะในอนาคต</p>
    </div>
    """, unsafe_allow_html=True)


# =========================
# Navigation Guide
# =========================
st.markdown(
    '<div class="section-title">🧭 เมนูการใช้งาน</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    <div class="card">
        <h3>🏠 ภาพรวมประเทศไทย</h3>
        <p>
        แสดงภาพรวมข้อมูลขยะมูลฝอยของประเทศไทย
        พร้อมสถิติสำคัญและข้อมูลในแต่ละปี
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>🗺️ การกระจายตัว</h3>
        <p>
        วิเคราะห์การกระจายตัวของปริมาณขยะในแต่ละจังหวัด
        และภูมิภาค เพื่อให้เห็นความแตกต่างเชิงพื้นที่
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>🤖 Machine Learning</h3>
        <p>
        ใช้โมเดล Machine Learning เพื่อวิเคราะห์รูปแบบข้อมูล
        และพยากรณ์แนวโน้มปริมาณขยะในอนาคต
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="card">
        <h3>📈 วิเคราะห์แนวโน้ม</h3>
        <p>
        วิเคราะห์แนวโน้มของปริมาณขยะตามช่วงเวลา
        พร้อมกราฟสำหรับเปรียบเทียบข้อมูลแต่ละปี
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>🔍 สำรวจข้อมูล</h3>
        <p>
        เลือกข้อมูลและตัวแปรที่ต้องการวิเคราะห์ได้อย่างอิสระ
        เหมาะสำหรับการสำรวจและค้นหารูปแบบที่น่าสนใจใน Dataset
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "💡 เริ่มต้นใช้งานโดยเลือกเมนูจาก Sidebar ทางด้านซ้าย"
    )


# =========================
# Footer
# =========================
st.markdown("""
<div class="footer">
    🇹🇭 Thai MSW Analytics System<br>
    ระบบวิเคราะห์และพยากรณ์ข้อมูลขยะมูลฝอยประเทศไทย
</div>
""", unsafe_allow_html=True)