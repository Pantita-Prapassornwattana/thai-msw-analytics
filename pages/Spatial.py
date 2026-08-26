import pandas as pd
import plotly.express as px
import streamlit as st
from utils import load_clean_data

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Spatial Analytics - Thai MSW Analytics",
    page_icon="🗺️",
    layout="wide",
)

st.title("🗺️ การวิเคราะห์การกระจายตัวเชิงพื้นที่ (Spatial Analytics)")
st.caption("เจาะลึกความเข้มข้นของปริมาณขยะรายภูมิภาคและรายจังหวัดด้วย Treemap")

# =========================================================
# LOAD DATA
# =========================================================
df = load_clean_data()

if df.empty:
    st.error("❌ ไม่พบข้อมูลในระบบ")
    st.stop()

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.header("⚙️ ตัวกรองเชิงพื้นที่")

years = sorted(df["year_be"].dropna().unique(), reverse=True)
selected_year = st.sidebar.selectbox("📅 เลือกปี พ.ศ.", years, index=0)

metric_options = {
    "🗑️ ขยะที่เกิดขึ้น": "generated_ton_day",
    "♻️ นำกลับมาใช้ประโยชน์": "recycled_ton_day",
    "✅ กำจัดถูกต้อง": "disposed_correct_ton_day",
    "⚠️ กำจัดไม่ถูกต้อง": "disposed_incorrect_ton_day",
    "📦 ขยะตกค้างสะสม": "residual_ton",
}

selected_metric_label = st.sidebar.selectbox(
    "📊 เลือกตัวแปรที่ต้องการวิเคราะห์", list(metric_options.keys())
)
selected_metric = metric_options[selected_metric_label]

df_year = df[
    (df["year_be"] == selected_year) & (df["province_display"] != "ไม่ระบุ")
].copy()

if df_year.empty:
    st.warning(f"⚠️ ไม่พบข้อมูลสำหรับปี พ.ศ. {selected_year}")
    st.stop()

# =========================================================
# 1. SPATIAL TREEMAP (HERO VISUAL)
# =========================================================
st.markdown("---")
st.subheader(f"🧩 สัดส่วนเชิงพื้นที่: {selected_metric_label} (พ.ศ. {int(selected_year)})")
st.caption("ขนาดของกล่องสี่เหลี่ยมแทนปริมาณขยะ สามารถกดคลิกที่กล่องภูมิภาคเพื่อเจาะลึกรายจังหวัดได้")

fig_treemap = px.treemap(
    df_year,
    path=[px.Constant("ประเทศไทย"), "region_display", "province_display"],
    values=selected_metric,
    color=selected_metric,
    color_continuous_scale="Reds",
    hover_data=[selected_metric],
)
fig_treemap.update_traces(
    root_color="lightgrey",
    hovertemplate="<b>%{label}</b><br>ปริมาณ: %{value:,.2f} ตัน/วัน<extra></extra>",
)
fig_treemap.update_layout(height=550, margin=dict(t=20, l=10, r=10, b=10))

st.plotly_chart(fig_treemap, use_container_width=True)

# =========================================================
# 2. REGIONAL COMPARISON TABLE & HOTSPOTS
# =========================================================
st.markdown("---")
col_reg, col_top = st.columns([1, 1])

with col_reg:
    st.subheader("📍 สรุปปริมาณแยกรายภาค")
    reg_summary = (
        df_year.groupby("region_display")[selected_metric]
        .sum()
        .reset_index()
        .sort_values(by=selected_metric, ascending=False)
    )
    reg_summary.columns = ["ภูมิภาค", "ปริมาณรวม (ตัน/วัน)"]
    st.dataframe(
        reg_summary.style.format({"ปริมาณรวม (ตัน/วัน)": "{:,.2f}"}),
        use_container_width=True,
        hide_index=True,
    )

with col_top:
    st.subheader("🔥 5 จังหวัด Hotspot ที่มีปริมาณสูงสุด")
    top5_prov = df_year.nlargest(5, selected_metric)[
        ["province_display", "region_display", selected_metric]
    ]
    top5_prov.columns = ["จังหวัด", "ภูมิภาค", "ปริมาณ (ตัน/วัน)"]
    st.dataframe(
        top5_prov.style.format({"ปริมาณ (ตัน/วัน)": "{:,.2f}"}),
        use_container_width=True,
        hide_index=True,
    )