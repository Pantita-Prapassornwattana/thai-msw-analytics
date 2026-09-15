import pandas as pd
import plotly.express as px
import streamlit as st
from utils import load_clean_data, filter_and_aggregate_by_year

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="System Overview - Thai MSW Analytics",
    page_icon="🖥️",
    layout="wide"
)

# =========================================================
# LOAD DATA
# =========================================================
df = load_clean_data()

if df.empty:
    st.error("❌ ไม่พบข้อมูลในระบบ")
    st.stop()

# =========================================================
# HEADER
# =========================================================
st.title("🖥️ ภาพรวมระบบจัดการขยะมูลฝอยประเทศไทย")
st.caption("System Overview Dashboard สำหรับการตรวจสอบสถิติและสถานะโครงสร้างพื้นฐานระบบ")

# =========================================================
# SIDEBAR & FILTERING (ปรับแก้เพื่อรองรับตัวเลือก "ทั้งหมด")
# =========================================================
st.sidebar.header("⚙️ ตัวกรองระบบ")
years = sorted(df["year_be"].dropna().unique())

# เพิ่ม "ทั้งหมด" เข้าไปในลิสต์ตัวเลือก
year_options = ["ทั้งหมด"] + list(years)
selected_year = st.sidebar.selectbox("📅 เลือกปี พ.ศ. (System Year)", year_options, index=len(year_options) - 1)

# เรียกใช้ฟังก์ชันกรองข้อมูลและกำหนดชื่อปีแสดงผล
filtered = filter_and_aggregate_by_year(df, selected_year, group_by_cols=["province_display"])

if selected_year == "ทั้งหมด":
    year_label = "ภาพรวมสะสมทุกรอบปีระบบ (All Years Aggregate)"
else:
    year_label = f"รอบปีระบบ พ.ศ. {int(selected_year)}"

if filtered.empty:
    st.warning(f"⚠️ ไม่พบชุดข้อมูลสำหรับตัวเลือก {selected_year}")
    st.stop()

# =========================================================
# CALCULATE SYSTEM METRICS
# =========================================================
total_gen = filtered["generated_ton_day"].sum(min_count=1)
total_rec = filtered["recycled_ton_day"].sum(min_count=1)
total_cor = filtered["disposed_correct_ton_day"].sum(min_count=1)
total_inc = filtered["disposed_incorrect_ton_day"].sum(min_count=1)
total_res = filtered["residual_ton"].sum(min_count=1)

recycle_pct = (total_rec / total_gen * 100) if total_gen and total_gen > 0 else 0
correct_pct = (total_cor / total_gen * 100) if total_gen and total_gen > 0 else 0
incorrect_pct = (total_inc / total_gen * 100) if total_gen and total_gen > 0 else 0

# =========================================================
# 1. SYSTEM METRICS & PERFORMANCE CARDS
# =========================================================
st.markdown("---")
st.subheader(f"📊 ตัวชี้วัดประสิทธิภาพระบบ ({year_label})")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🔄 อัตราการไหลรวม (Generation)", f"{total_gen:,.0f} ตัน/วัน")
with col2:
    st.metric("♻️ อัตราการนำกลับมาใช้ (Recovery)", f"{total_rec:,.0f} ตัน/วัน", f"{recycle_pct:.1f}% ของระบบ")
with col3:
    st.metric("⚙️ อัตรากำจัดถูกต้อง (Standard Disposal)", f"{total_cor:,.0f} ตัน/วัน", f"{correct_pct:.1f}% ของระบบ")
with col4:
    st.metric("⚠️ อัตรากำจัดไม่ถูกต้อง (Non-Standard)", f"{total_inc:,.0f} ตัน/วัน", f"{incorrect_pct:.1f}% ของระบบ", delta_color="inverse")

# =========================================================
# 2. SYSTEM STATUS & HEALTH CHECK LOGS
# =========================================================
st.markdown("---")
st.subheader("🔍 สถานะสุขภาพระบบและบันทึกตรวจสอบ (System Health Logs)")

col_alert1, col_alert2 = st.columns(2)

with col_alert1:
    if incorrect_pct > 25:
        st.error(f"🔴 **System Alert:** ตรวจพบอัตราการกำจัดไม่ถูกต้องสูงถึง **{incorrect_pct:.1f}%** เกินเกณฑ์มาตรฐานระบบ")
    else:
        st.success(f"🟢 **System Status Normal:** ประสิทธิภาพการจัดการตามมาตรฐานรวมอยู่ที่ **{correct_pct + recycle_pct:.1f}%**")

with col_alert2:
    st.warning(f"🟡 **Accumulated Residual:** ปริมาณขยะตกค้างสะสมในระบบโครงสร้างพื้นฐานรวม **{total_res:,.0f} ตัน**")

# =========================================================
# 3. SYSTEM COMPOSITION STRUCTURE (DONUT CHART)
# =========================================================
st.markdown("---")
st.subheader(f"🧩 โครงสร้างสัดส่วนการบริหารจัดการขยะในระบบ ({year_label})")

mgr_data = pd.DataFrame({
    "วิธีการจัดการ": ["นำกลับมาใช้ประโยชน์", "กำจัดถูกต้อง", "กำจัดไม่ถูกต้อง"],
    "ปริมาณ": [total_rec, total_cor, total_inc]
})

fig_pie = px.pie(
    mgr_data,
    values="ปริมาณ",
    names="วิธีการจัดการ",
    hole=0.55,
    color="วิธีการจัดการ",
    color_discrete_map={
        "นำกลับมาใช้ประโยชน์": "#2ecc71",
        "กำจัดถูกต้อง": "#3498db",
        "กำจัดไม่ถูกต้อง": "#e74c3c"
    }
)
fig_pie.update_traces(
    textposition="inside", 
    textinfo="percent+label",
    textfont_size=15
)
fig_pie.update_layout(
    height=450,
    showlegend=True,
    legend=dict(
        orientation="v",          # เปลี่ยนเป็นแนวตั้ง (Vertical)
        yanchor="middle",
        y=0.5,                    # จัดให้อยู่กึ่งกลางแนวตั้งพอดี
        xanchor="left",
        x=1.05,                   # วางไว้ชิดขอบขวาของกราฟพอดี
        font=dict(size=16)        # ขนาดตัวอักษร
    ),
    margin=dict(t=20, b=20, l=20, r=20)
)

# จัดให้อยู่ตรงกลางด้วยคอลัมน์เปล่าซ้าย-ขวา เพื่อให้กราฟขยายใหญ่ขึ้นเต็มตา
col_left, col_center, col_right = st.columns([1, 4, 1])
with col_center:
    st.plotly_chart(fig_pie, use_container_width=True)

st.info("💡 **คำแนะนำการใช้งานระบบ:** เลือกโมดูลการวิเคราะห์เชิงลึกจากแถบ Sidebar ด้านซ้ายเพื่อตรวจสอบข้อมูลในมิติอื่นๆ เช่น **📈 Trends** (แนวโน้มอนุกรมเวลา), **🗺️ Spatial** (การกระจายตัวเชิงพื้นที่), หรือ **🤖 ML Analytics** (การทำเหมืองข้อมูลและจัดกลุ่ม)")