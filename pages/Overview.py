import pandas as pd
import plotly.express as px
import streamlit as st
from utils import load_clean_data, filter_and_aggregate_by_year
from theme import inject_global_css, page_header, section_title, kpi_card, info_card, empty_state, footer, style_fig, COLORS

st.set_page_config(page_title="System Overview", page_icon="🖥️", layout="wide")
inject_global_css()

with st.spinner("กำลังโหลดข้อมูล..."):
    df = load_clean_data()

if df.empty:
    empty_state()

page_header("🖥️", "ภาพรวมระบบจัดการขยะมูลฝอยประเทศไทย", "System Overview Dashboard สำหรับการตรวจสอบสถิติและสถานะโครงสร้างพื้นฐานระบบ")

with st.sidebar:
    st.markdown("## 🖥️ Overview")
    st.caption("ภาพรวมระบบจัดการขยะมูลฝอย")
    st.markdown("---")
    st.markdown("### ⚙️ ตัวกรองระบบ")
    years = sorted(df["year_be"].dropna().unique())
    year_options = ["ทั้งหมด"] + list(years)
    selected_year = st.selectbox("📅 เลือกปี พ.ศ. (System Year)", year_options, index=len(year_options) - 1, help="เลือก 'ทั้งหมด' เพื่อดูผลรวมสะสมทุกปี")
    st.markdown("---")
    st.caption("💡 ปรับปีเพื่อเปรียบเทียบสถานะระบบในแต่ละช่วงเวลา")

filtered = filter_and_aggregate_by_year(df, selected_year, group_by_cols=["province_display"])
year_label = "ภาพรวมสะสมทุกรอบปีระบบ (All Years Aggregate)" if selected_year == "ทั้งหมด" else f"รอบปีระบบ พ.ศ. {int(selected_year)}"

if filtered.empty:
    empty_state(f"ไม่พบชุดข้อมูลสำหรับตัวเลือก {selected_year}")

total_gen = filtered["generated_ton_day"].sum(min_count=1)
total_rec = filtered["recycled_ton_day"].sum(min_count=1)
total_cor = filtered["disposed_correct_ton_day"].sum(min_count=1)
total_inc = filtered["disposed_incorrect_ton_day"].sum(min_count=1)
total_res = filtered["residual_ton"].sum(min_count=1)

recycle_pct = (total_rec / total_gen * 100) if total_gen and total_gen > 0 else 0
correct_pct = (total_cor / total_gen * 100) if total_gen and total_gen > 0 else 0
incorrect_pct = (total_inc / total_gen * 100) if total_gen and total_gen > 0 else 0

section_title("📊", f"ตัวชี้วัดประสิทธิภาพระบบ · {year_label}")
col1, col2, col3, col4 = st.columns(4)
with col1:
    kpi_card("🔄", "อัตราการไหลรวม (Generation)", f"{total_gen:,.0f} ตัน/วัน", color=COLORS["primary"])
with col2:
    kpi_card("♻️", "อัตราการนำกลับมาใช้ (Recovery)", f"{total_rec:,.0f} ตัน/วัน", f"{recycle_pct:.1f}% ของระบบ", color=COLORS["success"])
with col3:
    kpi_card("⚙️", "อัตรากำจัดถูกต้อง (Standard)", f"{total_cor:,.0f} ตัน/วัน", f"{correct_pct:.1f}% ของระบบ", color=COLORS["info"])
with col4:
    kpi_card("⚠️", "อัตรากำจัดไม่ถูกต้อง (Non-Standard)", f"{total_inc:,.0f} ตัน/วัน", f"{incorrect_pct:.1f}% ของระบบ", color=COLORS["danger"])

st.write("")

section_title("🔍", "สถานะสุขภาพระบบและบันทึกตรวจสอบ (System Health Logs)")
col_alert1, col_alert2 = st.columns(2)
with col_alert1:
    if incorrect_pct > 25:
        st.error(f"🔴 **System Alert:** ตรวจพบอัตราการกำจัดไม่ถูกต้องสูงถึง **{incorrect_pct:.1f}%** เกินเกณฑ์มาตรฐานระบบ")
    else:
        st.success(f"🟢 **System Status Normal:** ประสิทธิภาพการจัดการตามมาตรฐานรวมอยู่ที่ **{correct_pct + recycle_pct:.1f}%**")
with col_alert2:
    st.warning(f"🟡 **Accumulated Residual:** ปริมาณขยะตกค้างสะสมในระบบโครงสร้างพื้นฐานรวม **{total_res:,.0f} ตัน**")

st.write("")

section_title("🧩", f"โครงสร้างสัดส่วนการบริหารจัดการขยะในระบบ · {year_label}")
with st.container(border=True):
    mgr_data = pd.DataFrame({
        "วิธีการจัดการ": ["นำกลับมาใช้ประโยชน์", "กำจัดถูกต้อง", "กำจัดไม่ถูกต้อง"],
        "ปริมาณ": [total_rec, total_cor, total_inc]
    })
    fig_pie = px.pie(
        mgr_data, values="ปริมาณ", names="วิธีการจัดการ", hole=0.55, color="วิธีการจัดการ",
        color_discrete_map={"นำกลับมาใช้ประโยชน์": COLORS["success"], "กำจัดถูกต้อง": COLORS["info"], "กำจัดไม่ถูกต้อง": COLORS["danger"]}
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label", textfont_size=15)
    fig_pie.update_layout(height=450, showlegend=True, legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05, font=dict(size=15)))
    style_fig(fig_pie, margin=dict(t=20, b=20, l=20, r=20))
    col_left, col_center, col_right = st.columns([1, 4, 1])
    with col_center:
        st.plotly_chart(fig_pie, use_container_width=True)

st.write("")
info_card("💡", "คำแนะนำการใช้งานระบบ", "เลือกโมดูลการวิเคราะห์เชิงลึกจากแถบ Sidebar ด้านซ้ายเพื่อตรวจสอบข้อมูลในมิติอื่นๆ", color=COLORS["primary"])
footer("System Overview")