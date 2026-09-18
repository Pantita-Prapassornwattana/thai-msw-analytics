import pandas as pd
import plotly.express as px
import streamlit as st
from utils import load_clean_data, filter_and_aggregate_by_year
from theme import inject_global_css, page_header, section_title, kpi_card, empty_state, footer, style_fig, COLORS

st.set_page_config(page_title="Spatial Analytics", page_icon="🗺️", layout="wide")
inject_global_css()

with st.spinner("กำลังโหลดข้อมูล..."):
    df = load_clean_data()

if df.empty:
    empty_state()

page_header("🗺️", "การวิเคราะห์เชิงพื้นที่ (Spatial Analytics)", "เจาะลึกความหนาแน่นด้วยสีสันใน Treemap — กล่องยิ่งใหญ่ สียิ่งเข้ม คือพื้นที่ที่มีปริมาณเยอะ")

with st.sidebar:
    st.markdown("## 🗺️ Spatial")
    st.caption("วิเคราะห์การกระจายตัวเชิงพื้นที่")
    st.markdown("---")
    st.markdown("### ⚙️ ตัวกรองเชิงพื้นที่")
    years = ["ทั้งหมด"] + list(sorted(df["year_be"].dropna().unique(), reverse=True))
    selected_year = st.selectbox("📅 เลือกปี พ.ศ.", years)
    
    metric_options = {
        "🗑️ ขยะที่เกิดขึ้น": "generated_ton_day",
        "♻️ นำกลับมาใช้ประโยชน์": "recycled_ton_day",
        "✅ กำจัดถูกต้อง": "disposed_correct_ton_day",
        "⚠️ กำจัดไม่ถูกต้อง": "disposed_incorrect_ton_day",
        "📦 ขยะตกค้างสะสม": "residual_ton"
    }
    metric_label = st.selectbox("📊 ตัวแปรที่วิเคราะห์", list(metric_options.keys()))
    selected_metric = metric_options[metric_label]
    st.markdown("---")
    st.caption("💡 คลิกที่กล่องใน Treemap เพื่อ Zoom เข้าดูรายละเอียดระดับภูมิภาค/จังหวัด")

df_year = filter_and_aggregate_by_year(df[df["province_display"] != "ไม่ระบุ"], selected_year, group_by_cols=["province_display", "region_display"])
year_label = "ทุกปีสะสม" if selected_year == "ทั้งหมด" else f"พ.ศ. {int(selected_year)}"

if df_year.empty:
    empty_state(f"ไม่พบข้อมูลสำหรับ {year_label}")

mcolor = COLORS["success"]
total_value = df_year[selected_metric].sum(min_count=1)
top_row = df_year.loc[df_year[selected_metric].idxmax()]
top_region = df_year.groupby("region_display")[selected_metric].sum().idxmax()

section_title("📊", f"สรุปเชิงพื้นที่ · {metric_label.split(' ', 1)[1]} ({year_label})")
k1, k2, k3 = st.columns(3)
with k1:
    kpi_card("Σ", "ปริมาณรวมทั่วประเทศ", f"{total_value:,.0f} ตัน/วัน", color=mcolor)
with k2:
    kpi_card("🏆", "จังหวัดสูงสุด", str(top_row["province_display"]), f"{top_row[selected_metric]:,.2f} ตัน/วัน", color=mcolor)
with k3:
    kpi_card("🗺️", "ภูมิภาคสูงสุด", str(top_region), color=mcolor)

st.write("")

section_title("🧩", f"สัดส่วนเชิงพื้นที่: {metric_label.split(' ', 1)[1]} ({year_label})")
with st.container(border=True):
    fig_tree = px.treemap(
        df_year, path=[px.Constant("ประเทศไทย"), "region_display", "province_display"],
        values=selected_metric, color=selected_metric,
        color_continuous_scale="Greens", hover_data=[selected_metric]
    )
    fig_tree.update_traces(hovertemplate="<b>%{label}</b><br>ปริมาณ: %{value:,.2f} ตัน/วัน<extra></extra>", marker=dict(line=dict(color='white', width=1.5)))
    style_fig(fig_tree, height=550, margin=dict(t=10, l=10, r=10, b=10))
    st.plotly_chart(fig_tree, use_container_width=True)

st.write("")

section_title("🔥", "สรุปรายภาค & Hotspot รายจังหวัด")
col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.markdown("#### 📍 สรุปปริมาณแยกรายภาค")
        reg_sum = df_year.groupby("region_display")[selected_metric].sum().reset_index().sort_values(selected_metric, ascending=False)
        reg_sum.columns = ["ภูมิภาค", "ปริมาณรวม"]
        st.dataframe(reg_sum.style.bar(subset=['ปริมาณรวม'], color='#34d399').format({"ปริมาณรวม": "{:,.2f}"}), use_container_width=True, hide_index=True)

with col2:
    with st.container(border=True):
        st.markdown("#### 🔥 5 จังหวัด Hotspot สูงสุด")
        top5 = df_year.nlargest(5, selected_metric)[["province_display", "region_display", selected_metric]]
        top5.columns = ["จังหวัด", "ภูมิภาค", "ปริมาณ"]
        st.dataframe(top5.style.bar(subset=['ปริมาณ'], color='#10b981').format({"ปริมาณ": "{:,.2f}"}), use_container_width=True, hide_index=True)

footer("Spatial Analytics")