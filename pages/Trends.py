import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_clean_data


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Trends - Thai MSW Analytics",
    page_icon="📈",
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
# CHECK REQUIRED COLUMNS
# =========================================================
required_columns = [
    "year_be",
    "region_display",
    "generated_ton_day",
    "recycled_ton_day",
    "disposed_correct_ton_day",
    "disposed_incorrect_ton_day"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        "❌ ไม่พบคอลัมน์ที่จำเป็น: "
        + ", ".join(missing_columns)
    )
    st.stop()


# =========================================================
# HEADER
# =========================================================
st.title("📈 การวิเคราะห์แนวโน้มปริมาณขยะ")
st.subheader("Time-Series Analytics")

st.markdown("""
วิเคราะห์การเปลี่ยนแปลงของปริมาณขยะและรูปแบบการจัดการขยะ
ในแต่ละปี พร้อมเปรียบเทียบแนวโน้มระหว่างภูมิภาค
""")


# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.header("⚙️ ตัวกรองข้อมูล")


# ---------------------------------------------------------
# Region
# ---------------------------------------------------------
regions = (
    df["region_display"]
    .dropna()
    .unique()
)

regions = sorted([
    r for r in regions
    if r != "ไม่ระบุ"
])

regions = ["ทั้งหมด"] + regions


selected_region = st.sidebar.selectbox(
    "🗺️ เลือกภูมิภาค",
    regions
)


# =========================================================
# FILTER REGION
# =========================================================
df_filtered = df.copy()

if selected_region != "ทั้งหมด":

    df_filtered = df_filtered[
        df_filtered["region_display"]
        == selected_region
    ]


if df_filtered.empty:
    st.warning(
        "⚠️ ไม่พบข้อมูลสำหรับภูมิภาคที่เลือก"
    )
    st.stop()


# =========================================================
# AVAILABLE YEARS
# =========================================================
available_years = sorted(
    df_filtered["year_be"]
    .dropna()
    .unique()
)


if len(available_years) < 2:
    st.warning(
        "⚠️ ข้อมูลมีน้อยกว่า 2 ปี "
        "จึงไม่สามารถวิเคราะห์แนวโน้มได้"
    )
    st.stop()


# =========================================================
# YEAR RANGE
# =========================================================
selected_year_range = st.sidebar.slider(
    "📅 ช่วงปีที่ต้องการวิเคราะห์",
    min_value=int(min(available_years)),
    max_value=int(max(available_years)),
    value=(
        int(min(available_years)),
        int(max(available_years))
    )
)


df_filtered = df_filtered[
    df_filtered["year_be"].between(
        selected_year_range[0],
        selected_year_range[1]
    )
]


if df_filtered.empty:
    st.warning(
        "⚠️ ไม่พบข้อมูลในช่วงปีที่เลือก"
    )
    st.stop()


# =========================================================
# AGGREGATE YEARLY DATA
# =========================================================
# สำคัญ:
# ใช้ชื่อ column เดิมจาก Dataset ตลอด
# ไม่เปลี่ยนชื่อเป็นภาษาไทยระหว่างการคำนวณ
# =========================================================

trend_df = (
    df_filtered
    .groupby("year_be")
    .agg({
        "generated_ton_day": "sum",
        "recycled_ton_day": "sum",
        "disposed_correct_ton_day": "sum",
        "disposed_incorrect_ton_day": "sum"
    })
    .reset_index()
    .sort_values("year_be")
)


if trend_df.empty:
    st.warning(
        "⚠️ ไม่พบข้อมูลสำหรับการวิเคราะห์"
    )
    st.stop()


# =========================================================
# METRIC LABELS
# =========================================================
metric_options = {
    "🗑️ ขยะที่เกิดขึ้น": "generated_ton_day",
    "♻️ นำกลับมาใช้ประโยชน์": "recycled_ton_day",
    "✅ กำจัดถูกต้อง": "disposed_correct_ton_day",
    "⚠️ กำจัดไม่ถูกต้อง": "disposed_incorrect_ton_day"
}


metric_labels = {
    "generated_ton_day": "ขยะที่เกิดขึ้น",
    "recycled_ton_day": "นำกลับมาใช้ประโยชน์",
    "disposed_correct_ton_day": "กำจัดถูกต้อง",
    "disposed_incorrect_ton_day": "กำจัดไม่ถูกต้อง"
}


# =========================================================
# SELECT METRIC
# =========================================================
selected_metric_label = st.sidebar.selectbox(
    "📊 เลือกตัวแปรที่ต้องการวิเคราะห์",
    list(metric_options.keys())
)


selected_metric = metric_options[
    selected_metric_label
]


selected_metric_name = metric_labels[
    selected_metric
]


# =========================================================
# CALCULATE STATISTICS
# =========================================================
first_year = trend_df[
    "year_be"
].iloc[0]

last_year = trend_df[
    "year_be"
].iloc[-1]


first_value = trend_df[
    selected_metric
].iloc[0]


last_value = trend_df[
    selected_metric
].iloc[-1]


average_value = trend_df[
    selected_metric
].mean()


max_row = trend_df.loc[
    trend_df[selected_metric].idxmax()
]


min_row = trend_df.loc[
    trend_df[selected_metric].idxmin()
]


if pd.notna(first_value) and first_value != 0:

    change_pct = (
        (last_value - first_value)
        / first_value
    ) * 100

else:

    change_pct = None


# =========================================================
# KPI
# =========================================================
st.markdown("---")

st.subheader(
    f"📊 สรุปแนวโน้ม: {selected_metric_name}"
)


col1, col2, col3, col4, col5 = st.columns(5)


# ---------------------------------------------------------
# First Year
# ---------------------------------------------------------
with col1:

    st.metric(
        "📅 ปีแรก",
        (
            "ไม่มีข้อมูล"
            if pd.isna(first_value)
            else f"{first_value:,.0f}"
        ),
        f"พ.ศ. {int(first_year)}"
    )


# ---------------------------------------------------------
# Latest Year
# ---------------------------------------------------------
with col2:

    st.metric(
        "📅 ปีล่าสุด",
        (
            "ไม่มีข้อมูล"
            if pd.isna(last_value)
            else f"{last_value:,.0f}"
        ),
        f"พ.ศ. {int(last_year)}"
    )


# ---------------------------------------------------------
# Change
# ---------------------------------------------------------
with col3:

    st.metric(
        "📊 การเปลี่ยนแปลง",
        (
            "ไม่มีข้อมูล"
            if change_pct is None
            else f"{change_pct:+.2f}%"
        )
    )


# ---------------------------------------------------------
# Average
# ---------------------------------------------------------
with col4:

    st.metric(
        "📌 ค่าเฉลี่ย",
        (
            "ไม่มีข้อมูล"
            if pd.isna(average_value)
            else f"{average_value:,.0f}"
        )
    )


# ---------------------------------------------------------
# Maximum
# ---------------------------------------------------------
with col5:

    st.metric(
        "📈 ค่าสูงสุด",
        f"{max_row[selected_metric]:,.0f}",
        f"พ.ศ. {int(max_row['year_be'])}"
    )


# =========================================================
# MAIN TREND CHART
# =========================================================
st.markdown("---")

st.subheader(
    f"📈 แนวโน้ม {selected_metric_name}"
)


fig_line = px.line(
    trend_df,
    x="year_be",
    y=selected_metric,
    markers=True,
    labels={
        "year_be": "ปี พ.ศ.",
        selected_metric: "ปริมาณ (ตัน/วัน)"
    },
    title=(
        f"แนวโน้ม {selected_metric_name} "
        f"({selected_region})"
    )
)


fig_line.update_traces(
    line=dict(width=3),
    marker=dict(size=9)
)


fig_line.update_layout(
    height=500,
    hovermode="x unified"
)


st.plotly_chart(
    fig_line,
    use_container_width=True
)


# =========================================================
# YEAR OVER YEAR
# =========================================================
trend_yoy = trend_df.copy()

trend_yoy["yoy_change"] = (
    trend_yoy[selected_metric]
    .pct_change()
    * 100
)


st.markdown("---")

st.subheader(
    "📊 อัตราการเปลี่ยนแปลงรายปี "
    "(Year-over-Year)"
)


fig_yoy = px.bar(
    trend_yoy,
    x="year_be",
    y="yoy_change",
    text="yoy_change",
    labels={
        "year_be": "ปี พ.ศ.",
        "yoy_change": "การเปลี่ยนแปลง (%)"
    },
    title=(
        f"การเปลี่ยนแปลงของ "
        f"{selected_metric_name} เมื่อเทียบกับปีก่อน"
    )
)


fig_yoy.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)


fig_yoy.add_hline(
    y=0,
    line_width=1
)


fig_yoy.update_layout(
    height=450
)


st.plotly_chart(
    fig_yoy,
    use_container_width=True
)


# =========================================================
# ALL METRICS COMPARISON
# =========================================================
st.markdown("---")

st.subheader(
    "📊 เปรียบเทียบแนวโน้มการจัดการขยะ"
)


# สร้าง DataFrame ใหม่โดยใช้ชื่อ column ภาษาอังกฤษ
comparison_df = trend_df[
    [
        "year_be",
        "generated_ton_day",
        "recycled_ton_day",
        "disposed_correct_ton_day",
        "disposed_incorrect_ton_day"
    ]
].copy()


# เปลี่ยนชื่อเป็นภาษาไทยเฉพาะสำหรับการแสดงผล
comparison_df.columns = [
    "ปี พ.ศ.",
    "ขยะที่เกิดขึ้น",
    "นำกลับมาใช้ประโยชน์",
    "กำจัดถูกต้อง",
    "กำจัดไม่ถูกต้อง"
]


# Wide → Long
comparison_long = comparison_df.melt(
    id_vars="ปี พ.ศ.",
    var_name="ประเภท",
    value_name="ปริมาณ"
)


fig_comparison = px.line(
    comparison_long,
    x="ปี พ.ศ.",
    y="ปริมาณ",
    color="ประเภท",
    markers=True,
    labels={
        "ปี พ.ศ.": "ปี พ.ศ.",
        "ปริมาณ": "ปริมาณ (ตัน/วัน)",
        "ประเภท": "ประเภท"
    },
    title="แนวโน้มข้อมูลการจัดการขยะทุกประเภท"
)


fig_comparison.update_layout(
    height=500,
    hovermode="x unified"
)


st.plotly_chart(
    fig_comparison,
    use_container_width=True
)


# =========================================================
# HIGHEST / LOWEST YEAR
# =========================================================
st.markdown("---")

st.subheader(
    "🏆 ปีที่มีค่ามากที่สุดและน้อยที่สุด"
)


col1, col2 = st.columns(2)


# ---------------------------------------------------------
# Highest
# ---------------------------------------------------------
with col1:

    st.success(
        f"""
### 📈 ปีที่มีค่าสูงสุด

**พ.ศ. {int(max_row['year_be'])}**

{max_row[selected_metric]:,.2f} ตัน/วัน

ตัวแปร: **{selected_metric_name}**
"""
    )


# ---------------------------------------------------------
# Lowest
# ---------------------------------------------------------
with col2:

    st.info(
        f"""
### 📉 ปีที่มีค่าต่ำสุด

**พ.ศ. {int(min_row['year_be'])}**

{min_row[selected_metric]:,.2f} ตัน/วัน

ตัวแปร: **{selected_metric_name}**
"""
    )


# =========================================================
# DATA TABLE
# =========================================================
st.markdown("---")

with st.expander("📋 ดูข้อมูลรายปี"):

    display_df = trend_df.copy()

    display_df.columns = [
        "ปี พ.ศ.",
        "ขยะที่เกิดขึ้น (ตัน/วัน)",
        "นำกลับมาใช้ประโยชน์ (ตัน/วัน)",
        "กำจัดถูกต้อง (ตัน/วัน)",
        "กำจัดไม่ถูกต้อง (ตัน/วัน)"
    ]


    st.dataframe(
        display_df.style.format({
            "ขยะที่เกิดขึ้น (ตัน/วัน)": "{:,.2f}",
            "นำกลับมาใช้ประโยชน์ (ตัน/วัน)": "{:,.2f}",
            "กำจัดถูกต้อง (ตัน/วัน)": "{:,.2f}",
            "กำจัดไม่ถูกต้อง (ตัน/วัน)": "{:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# EXPLANATION
# =========================================================
st.markdown("---")

with st.expander("ℹ️ วิธีอ่านกราฟแนวโน้ม"):

    st.markdown("""
### 📈 Time-Series Analysis

กราฟแนวโน้มใช้แสดงการเปลี่ยนแปลงของข้อมูลตามปี พ.ศ.

**Year-over-Year (YoY)** ใช้เปรียบเทียบค่าของปีปัจจุบัน
กับปีก่อนหน้า

- 📈 ค่าเป็นบวก → ปริมาณเพิ่มขึ้น
- 📉 ค่าเป็นลบ → ปริมาณลดลง
- ➖ ค่าใกล้ 0 → ปริมาณเปลี่ยนแปลงน้อย

สามารถเลือกจาก Sidebar ได้ 3 ส่วน:

1. 🗺️ **ภูมิภาค**
2. 📅 **ช่วงปี**
3. 📊 **ตัวแปรที่ต้องการวิเคราะห์**

ระบบจะแสดง KPI, Trend และ YoY
ตามตัวเลือกที่กำหนด
""")


# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.caption(
    "🇹🇭 Thai MSW Analytics | Time-Series Analytics"
)