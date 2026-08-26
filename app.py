import streamlit as st

st.set_page_config(
    page_title="Thai MSW Analytics",
    page_icon="🇹🇭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🇹🇭 Thai MSW Analytics System")
st.subheader("ระบบวิเคราะห์และพยากรณ์ข้อมูลขยะมูลฝอยประเทศไทย")

st.markdown("""
---
### 📌 ยินดีต้อนรับสู่ระบบวิเคราะห์ข้อมูลขยะมูลฝอย (MSW Analytics)
กรุณาเลือกเมนูที่ต้องการวิเคราะห์จาก **Sidebar ทางด้านซ้ายมือ**:

1. **🏠 ภาพรวมประเทศไทย (Overview)**
2. **📈 วิเคราะห์แนวโน้ม (Trends)**
3. **🗺️ การกระจายตัว (Spatial)**
4. **🔍 สำรวจข้อมูล (Explorer)**
5. **🤖 Machine Learning**
---
""")

st.info("👈 หากเมนูด้านซ้ายยังไม่ขึ้น ให้กด Stop แล้วสั่ง Clear Cache รันใหม่ตามวิธีด้านล่าง")