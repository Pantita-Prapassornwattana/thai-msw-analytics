import streamlit as st
from theme import inject_global_css, page_path

st.set_page_config(
    page_title="Thai MSW Analytics",
    page_icon="🇹🇭",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_global_css()

pages = [
    st.Page(page_path("Home"), title="หน้าแรก", icon="🏠", url_path="home", default=True),
    st.Page(page_path("Overview"), title="ภาพรวมระบบ", icon="🖥️", url_path="overview"),
    st.Page(page_path("Trends"), title="แนวโน้ม", icon="📈", url_path="trends"),
    st.Page(page_path("Spatial"), title="เชิงพื้นที่", icon="🗺️", url_path="spatial"),
    st.Page(page_path("ML_Analytics"), title="จัดกลุ่มด้วย ML", icon="🤖", url_path="ml-analytics"),
    st.Page(page_path("Explorer"), title="ค้นหาและส่งออก", icon="🔍", url_path="explorer"),
]

st.navigation(pages).run()