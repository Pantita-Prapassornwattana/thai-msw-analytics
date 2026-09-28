import os
import streamlit as st
from theme import page_header, section_title, info_card, footer, COLORS

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="Poster - Thai MSW Analytics",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# Header
# =========================
page_header("🖼️", "โปสเตอร์อินโฟกราฟิกโครงการ", "แสดงสรุปผลงานและข้อมูลสำคัญของการวิเคราะห์ระบบขยะมูลฝอยประเทศไทย")

# =========================
# Main Content (Poster Display)
# =========================
section_title("📊", "โครงงานและอินโฟกราฟิกสรุปผลงาน")

poster_filename = "poster.png"

if os.path.exists(poster_filename):
    # ใช้ container พร้อมกรอบเพื่อให้หน้าตาเข้าชุดกับการ์ดอื่นๆ ในระบบ
    with st.container(border=True):
        st.image(poster_filename, caption="Thai MSW Analytics Project Poster", use_container_width=True)
    
    st.write("")
    
    # ปุ่มดาวน์โหลดจัดกึ่งกลางเพื่อความสวยงาม
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with open(poster_filename, "rb") as file:
            st.download_button(
                label="📥 ดาวน์โหลดไฟล์โปสเตอร์ (PNG)",
                data=file,
                file_name="Thai_MSW_Analytics_Poster.png",
                mime="image/png",
                use_container_width=True
            )
else:
    st.warning(f"⚠️ ยังไม่พบไฟล์รูปภาพ `{poster_filename}` ในโฟลเดอร์หลักของโปรเจกต์")
    st.info("💡 วิธีแก้ไข: นำไฟล์รูปภาพ PNG ของคุณมาวางไว้ที่โฟลเดอร์หลัก แล้วตั้งชื่อว่า `poster.png` ครับ")

st.write("")

# คำแนะนำเพิ่มเติมท้ายหน้า
info_card("💡", "คำแนะนำเพิ่มเติม", "คุณสามารถดาวน์โหลดโปสเตอร์เพื่อนำไปใช้ในการนำเสนอผลงาน (Presentation) หรือเผยแพร่ต่อได้ทันที", color=COLORS["primary"])

# =========================
# Footer
# =========================
footer("Poster Overview")