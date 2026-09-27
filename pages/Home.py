import streamlit as st
from theme import hero, section_title, nav_card, footer, page_path, COLORS

hero("🇹🇭 Thai MSW Analytics", "ระบบวิเคราะห์ข้อมูลขยะมูลฝอยประเทศไทยอัจฉริยะ")

st.info("👋 **ยินดีต้อนรับ!** เลือกเมนูจากแถบด้านซ้ายหรือการ์ดด้านล่างเพื่อเริ่มต้นใช้งานระบบ Dashboard ที่ออกแบบมาให้อ่านข้อมูลง่ายและรวดเร็ว")

section_title("🧭", "เลือกดูข้อมูลที่ต้องการ")

menu = [
    ("🖥️", "ภาพรวมระบบ", "ดูภาพรวมปริมาณขยะ สัดส่วนการกำจัด และการแจ้งเตือนสถานะของระบบ", "Overview", "เปิดภาพรวมระบบ", COLORS["primary"]),
    ("📈", "วิเคราะห์แนวโน้ม", "ดูกราฟเส้นและกราฟแท่งเปรียบเทียบขยะรายปี พร้อมอัตราการเติบโต YoY แยกสีชัดเจนเพื่อความเข้าใจในพริบตา", "Trends", "เปิดหน้าแนวโน้ม", COLORS["info"]),
    ("🗺️", "การกระจายตัวเชิงพื้นที่", "ใช้ Treemap สีสันโทนเขียวในการเจาะลึกปริมาณขยะแต่ละภูมิภาคและจังหวัด พร้อมค้นหา Hotspot", "Spatial", "เปิดหน้าเชิงพื้นที่", COLORS["success"]),
    ("🤖", "ML Analytics", "จัดกลุ่มพฤติกรรมจังหวัดด้วย K-Means เพื่อเจาะลึกลักษณะของแต่ละกลุ่ม", "ML_Analytics", "เปิดหน้า ML", COLORS["purple"]),
    ("🔍", "ค้นหาและส่งออกข้อมูล", "ค้นหา กรอง และส่งออกตารางข้อมูลดิบเป็น CSV เพื่อนำไปวิเคราะห์ต่อ", "Explorer", "เปิดหน้าค้นหาข้อมูล", COLORS["warning"]),
]

for row_start in range(0, len(menu), 3):
    cols = st.columns(3)
    for col, (icon, title, desc, page, link_label, color) in zip(cols, menu[row_start:row_start + 3]):
        with col:
            nav_card(icon, title, desc, color=color)
            st.page_link(page_path(page), label=link_label, icon="➡️", use_container_width=True)

footer("หน้าแรก")