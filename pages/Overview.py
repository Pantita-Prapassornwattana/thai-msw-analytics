import pandas as pd
import plotly.express as px
import streamlit as st
from utils import load_clean_data

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Executive Summary - Thai MSW Analytics",
    page_icon="🏠",
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
st.title("🏠 ภาพรวมสถานการณ์ขยะมูลฝอยประเทศไทย")
st.caption("Executive Summary Dashboard สำหรับผู้บริหารและนักนโยบาย")

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.header("⚙️ ตัวกรองข้อมูล")
years = sorted(df["year_be"].dropna().unique())
selected_year = st.sidebar.selectbox("📅 เลือกปี พ.ศ.", years, index=len(years) - 1)

filtered = df[df["year_be"] == selected_year].copy()

if filtered.empty:
    st.warning(f"⚠️ ไม่พบข้อมูลในปี พ.ศ. {int(selected_year)}")
    st.stop()

# =========================================================
# CALCULATE KPI & METRICS
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
# 1. EXECUTIVE KPI CARDS
# =========================================================
st.markdown("---")
st.subheader(f"📊 สรุปตัวเลขสำคัญ ประจำปี พ.ศ. {int(selected_year)}")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("🗑️ ปริมาณขยะทั้งหมด", f"{total_gen:,.0f} ตัน/วัน")
with kpi2:
    st.metric("♻️ นำกลับมาใช้ประโยชน์", f"{total_rec:,.0f} ตัน/วัน", f"{recycle_pct:.1f}% ของขยะทั้งหมด")
with kpi3:
    st.metric("✅ กำจัดอย่างถูกต้อง", f"{total_cor:,.0f} ตัน/วัน", f"{correct_pct:.1f}% ของขยะทั้งหมด")
with kpi4:
    st.metric("⚠️ กำจัดไม่ถูกต้อง / ตกค้าง", f"{total_inc:,.0f} ตัน/วัน", f"{incorrect_pct:.1f}% ของขยะทั้งหมด", delta_color="inverse")

# =========================================================
# 2. EXECUTIVE STATUS & ALERT BOXES
# =========================================================
st.markdown("---")
st.subheader("🚨 สรุปสภาวะและข้อสังเกตสำคัญ")

col_alert1, col_alert2 = st.columns(2)

with col_alert1:
    if incorrect_pct > 25:
        st.error(f"⚠️ **เตือนภัยระดับสูง:** มีขยะที่กำจัดไม่ถูกต้องสูงถึง **{incorrect_pct:.1f}%** ควรเร่งขยายสถานที่กำจัดขยะมาตรฐาน")
    else:
        st.success(f"✅ **สภาวะปกติ:** ขยะได้รับการกำจัดอย่างถูกต้องและนำกลับมาใช้ประโยชน์รวมกันคิดเป็น **{correct_pct + recycle_pct:.1f}%**")

with col_alert2:
    st.warning(f"📦 **ขยะสะสมตกค้าง:** มีปริมาณขยะตกค้างสะสมในสถานที่กำจัดขยะรวม **{total_res:,.0f} ตัน** ทั่วประเทศ")

# =========================================================
# 3. HIGH-LEVEL MANAGEMENT BREAKDOWN (DONUT CHART ONLY)
# =========================================================
st.markdown("---")
st.subheader(f"♻️ โครงสร้างการจัดการขยะมูลฝอย (ปี พ.ศ. {int(selected_year)})")

mgr_data = pd.DataFrame({
    "วิธีการจัดการ": ["นำกลับมาใช้ประโยชน์", "กำจัดถูกต้อง", "กำจัดไม่ถูกต้อง"],
    "ปริมาณ": [total_rec, total_cor, total_inc]
})

fig_pie = px.pie(
    mgr_data,
    values="ปริมาณ",
    names="วิธีการจัดการ",
    hole=0.6,
    color="วิธีการจัดการ",
    color_discrete_map={
        "นำกลับมาใช้ประโยชน์": "#2ecc71",
        "กำจัดถูกต้อง": "#3498db",
        "กำจัดไม่ถูกต้อง": "#e74c3c"
    }
)
fig_pie.update_traces(textposition="inside", textinfo="percent+label")
fig_pie.update_layout(height=380, showlegend=True)

st.plotly_chart(fig_pie, use_container_width=True)

st.info("💡 **ต้องการดูรายละเอียดเชิงลึก?** เลือกเมนูด้านข้างเพื่อเจาะลึก: **📈 Trends** (แนวโน้มตามกาลเวลา), **🗺️ Spatial** (การกระจายเชิงพื้นที่/TreeMap), หรือ **🤖 ML Analytics** (การจัดกลุ่มจังหวัด)")