import pandas as pd
import plotly.express as px
import streamlit as st
from utils import load_clean_data

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Overview - Thai MSW Analytics", page_icon="🏠", layout="wide"
)

# =========================================================
# LOAD DATA (เรียกใช้จาก utils.py)
# =========================================================
df = load_clean_data()

# =========================================================
# HEADER & SIDEBAR FILTER
# =========================================================
st.title("🏠 ภาพรวมปริมาณขยะมูลฝอยประเทศไทย")

# ดึงรายการปี พ.ศ. ที่มีข้อมูลจริง
years = sorted(df["year_be"].dropna().unique())

if not years:
    st.error("❌ ไม่พบข้อมูลปี พ.ศ. ในชุดข้อมูล")
    st.stop()

selected_year = st.sidebar.selectbox(
    "📅 เลือกปี พ.ศ.", years, index=len(years) - 1
)

# กรองข้อมูลเฉพาะปีที่เลือก
filtered = df[df["year_be"] == selected_year].copy()

# =========================================================
# KPI METRICS
# =========================================================
# ใช้ sum(min_count=1) เพื่อคืนค่า NaN หากข้อมูลในปีนั้นเป็นค่าวางทั้งหมด
total_gen = filtered["generated_ton_day"].sum(min_count=1)
total_rec = filtered["recycled_ton_day"].sum(min_count=1)
total_cor = filtered["disposed_correct_ton_day"].sum(min_count=1)
total_inc = filtered["disposed_incorrect_ton_day"].sum(min_count=1)
total_res = filtered["residual_ton"].sum(min_count=1)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if pd.isna(total_gen):
        st.metric("🗑️ ขยะที่เกิดขึ้นทั้งหมด", "ไม่มีข้อมูล")
    else:
        st.metric("🗑️ ขยะที่เกิดขึ้นทั้งหมด", f"{total_gen:,.2f} ตัน/วัน")

with col2:
    if pd.isna(total_rec):
        st.metric("♻️ นำกลับมาใช้ประโยชน์", "ไม่มีข้อมูล")
    else:
        st.metric("♻️ นำกลับมาใช้ประโยชน์", f"{total_rec:,.2f} ตัน/วัน")

with col3:
    if pd.isna(total_gen) or pd.isna(total_cor) or total_gen == 0:
        st.metric("✅ กำจัดถูกต้อง", "ไม่มีข้อมูล")
    else:
        cor_pct = (total_cor / total_gen) * 100
        st.metric("✅ กำจัดถูกต้อง", f"{cor_pct:.2f}%")

with col4:
    if pd.isna(total_res):
        st.metric("⚠️ ขยะตกค้างสะสม", "ไม่มีข้อมูล")
    else:
        st.metric("⚠️ ขยะตกค้างสะสม", f"{total_res:,.2f} ตัน")

st.markdown("---")

# =========================================================
# DONUT CHART - MANAGEMENT BREAKDOWN
# =========================================================
st.subheader(f"📊 สัดส่วนการจัดการขยะมูลฝอยภาพรวม (ปี พ.ศ. {int(selected_year)})")

# สร้าง DataFrame สรุปวิธีการจัดการ
mgr_data = pd.DataFrame(
    {
        "วิธีการจัดการ": [
            "นำกลับมาใช้ประโยชน์ (Recycle)",
            "กำจัดถูกต้อง",
            "กำจัดไม่ถูกต้อง",
        ],
        "ปริมาณ (ตัน/วัน)": [
            0.0 if pd.isna(total_rec) else total_rec,
            0.0 if pd.isna(total_cor) else total_cor,
            0.0 if pd.isna(total_inc) else total_inc,
        ],
    }
)

# ตรวจสอบว่ามีข้อมูลนำมาแสดงกราฟหรือไม่
if mgr_data["ปริมาณ (ตัน/วัน)"].sum() > 0:
    fig_pie = px.pie(
        mgr_data,
        values="ปริมาณ (ตัน/วัน)",
        names="วิธีการจัดการ",
        hole=0.4,
        color="วิธีการจัดการ",
        color_discrete_map={
            "นำกลับมาใช้ประโยชน์ (Recycle)": "#2ecc71",
            "กำจัดถูกต้อง": "#3498db",
            "กำจัดไม่ถูกต้อง": "#e74c3c",
        },
    )

    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="%{label}<br>ปริมาณ: %{value:,.2f} ตัน/วัน (%{percent})",
    )

    fig_pie.update_layout(
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5
        )
    )

    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("ℹ️ ไม่มีข้อมูลสัดส่วนการจัดการขยะในปีที่เลือก")