import pandas as pd
import plotly.express as px
import streamlit as st

from utils import load_clean_data


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Overview - Thai MSW Analytics",
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
# CHECK REQUIRED COLUMNS
# =========================================================
required_columns = [
    "year_be",
    "province_display",
    "region_display",
    "generated_ton_day",
    "recycled_ton_day",
    "disposed_correct_ton_day",
    "disposed_incorrect_ton_day",
    "residual_ton"
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
st.title("🏠 ภาพรวมปริมาณขยะมูลฝอยประเทศไทย")

st.markdown("""
ภาพรวมข้อมูลขยะมูลฝอยของประเทศไทย
แสดงปริมาณขยะ การนำกลับมาใช้ประโยชน์
การกำจัดขยะ และการกระจายตัวของข้อมูลในแต่ละพื้นที่
""")


# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.header("⚙️ ตัวกรองข้อมูล")

years = sorted(
    df["year_be"].dropna().unique()
)

if not years:
    st.error("❌ ไม่พบข้อมูลปี พ.ศ. ในชุดข้อมูล")
    st.stop()


selected_year = st.sidebar.selectbox(
    "📅 เลือกปี พ.ศ.",
    years,
    index=len(years) - 1
)


# =========================================================
# FILTER DATA
# =========================================================
filtered = df[
    df["year_be"] == selected_year
].copy()


if filtered.empty:
    st.warning(
        f"⚠️ ไม่พบข้อมูลในปี พ.ศ. {int(selected_year)}"
    )
    st.stop()


# =========================================================
# CALCULATE KPI
# =========================================================
total_gen = filtered[
    "generated_ton_day"
].sum(min_count=1)

total_rec = filtered[
    "recycled_ton_day"
].sum(min_count=1)

total_cor = filtered[
    "disposed_correct_ton_day"
].sum(min_count=1)

total_inc = filtered[
    "disposed_incorrect_ton_day"
].sum(min_count=1)

total_res = filtered[
    "residual_ton"
].sum(min_count=1)


# =========================================================
# CALCULATE PERCENTAGES
# =========================================================
if (
    pd.notna(total_gen)
    and total_gen > 0
    and pd.notna(total_rec)
):
    recycle_pct = (
        total_rec / total_gen
    ) * 100
else:
    recycle_pct = None


if (
    pd.notna(total_gen)
    and total_gen > 0
    and pd.notna(total_cor)
):
    correct_pct = (
        total_cor / total_gen
    ) * 100
else:
    correct_pct = None


# =========================================================
# KPI SECTION
# =========================================================
st.subheader(
    f"📊 สรุปข้อมูลประเทศไทย ปี พ.ศ. {int(selected_year)}"
)

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    value = (
        "ไม่มีข้อมูล"
        if pd.isna(total_gen)
        else f"{total_gen:,.0f}"
    )

    st.metric(
        "🗑️ ขยะที่เกิดขึ้น",
        f"{value} ตัน/วัน"
    )


with col2:

    value = (
        "ไม่มีข้อมูล"
        if pd.isna(total_rec)
        else f"{total_rec:,.0f}"
    )

    st.metric(
        "♻️ นำกลับมาใช้ประโยชน์",
        f"{value} ตัน/วัน"
    )


with col3:

    value = (
        "ไม่มีข้อมูล"
        if correct_pct is None
        else f"{correct_pct:.1f}%"
    )

    st.metric(
        "✅ กำจัดถูกต้อง",
        value
    )


with col4:

    value = (
        "ไม่มีข้อมูล"
        if pd.isna(total_inc)
        else f"{total_inc:,.0f}"
    )

    st.metric(
        "⚠️ กำจัดไม่ถูกต้อง",
        f"{value} ตัน/วัน"
    )


with col5:

    value = (
        "ไม่มีข้อมูล"
        if pd.isna(total_res)
        else f"{total_res:,.0f}"
    )

    st.metric(
        "🏚️ ขยะตกค้างสะสม",
        f"{value} ตัน"
    )


st.markdown("---")


# =========================================================
# MANAGEMENT BREAKDOWN
# =========================================================
st.subheader(
    f"♻️ สัดส่วนการจัดการขยะ "
    f"ปี พ.ศ. {int(selected_year)}"
)

mgr_data = pd.DataFrame({
    "วิธีการจัดการ": [
        "นำกลับมาใช้ประโยชน์",
        "กำจัดถูกต้อง",
        "กำจัดไม่ถูกต้อง"
    ],
    "ปริมาณ": [
        0 if pd.isna(total_rec) else total_rec,
        0 if pd.isna(total_cor) else total_cor,
        0 if pd.isna(total_inc) else total_inc
    ]
})

col1, col2 = st.columns([1.5, 1])


# ---------------------------------------------------------
# Donut
# ---------------------------------------------------------
with col1:

    if mgr_data["ปริมาณ"].sum() > 0:

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
            textinfo="percent",
            hovertemplate=(
                "%{label}<br>"
                "ปริมาณ: %{value:,.2f} ตัน/วัน"
                "<br>สัดส่วน: %{percent}"
                "<extra></extra>"
            )
        )

        fig_pie.update_layout(
            height=430,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    else:

        st.info(
            "ℹ️ ไม่มีข้อมูลสำหรับสร้างกราฟ"
        )


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------
with col2:

    st.markdown("### 📌 สรุปการจัดการ")

    if recycle_pct is not None:

        st.metric(
            "♻️ อัตราการนำกลับมาใช้ประโยชน์",
            f"{recycle_pct:.2f}%"
        )

    if correct_pct is not None:

        st.metric(
            "✅ อัตราการกำจัดถูกต้อง",
            f"{correct_pct:.2f}%"
        )

    st.markdown("---")

    st.markdown("""
    **คำอธิบาย**

    - ♻️ นำกลับมาใช้ประโยชน์
    - ✅ กำจัดอย่างถูกต้อง
    - ⚠️ กำจัดไม่ถูกต้อง
    """)


# =========================================================
# TOP 10 PROVINCES
# =========================================================
st.markdown("---")

st.subheader(
    f"🏆 10 จังหวัดที่มีปริมาณขยะเกิดขึ้นสูงสุด "
    f"ปี พ.ศ. {int(selected_year)}"
)

top10 = (
    filtered[
        [
            "province_display",
            "region_display",
            "generated_ton_day"
        ]
    ]
    .dropna(subset=["generated_ton_day"])
    .sort_values(
        "generated_ton_day",
        ascending=False
    )
    .head(10)
)


fig_top10 = px.bar(
    top10.sort_values("generated_ton_day"),
    x="generated_ton_day",
    y="province_display",
    orientation="h",
    text="generated_ton_day",
    labels={
        "generated_ton_day": "ขยะที่เกิดขึ้น (ตัน/วัน)",
        "province_display": "จังหวัด"
    },
    title="Top 10 จังหวัดตามปริมาณขยะ"
)

fig_top10.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig_top10.update_layout(
    height=500
)

st.plotly_chart(
    fig_top10,
    use_container_width=True
)


# =========================================================
# REGIONAL ANALYSIS
# =========================================================
st.markdown("---")

st.subheader(
    f"🗺️ เปรียบเทียบปริมาณขยะตามภูมิภาค "
    f"ปี พ.ศ. {int(selected_year)}"
)

region_summary = (
    filtered
    .groupby("region_display")
    .agg(
        ขยะเกิดขึ้น=(
            "generated_ton_day",
            "sum"
        ),
        นำกลับมาใช้ประโยชน์=(
            "recycled_ton_day",
            "sum"
        )
    )
    .reset_index()
)

region_long = region_summary.melt(
    id_vars="region_display",
    var_name="ประเภท",
    value_name="ปริมาณ"
)


fig_region = px.bar(
    region_long,
    x="region_display",
    y="ปริมาณ",
    color="ประเภท",
    barmode="group",
    labels={
        "region_display": "ภูมิภาค",
        "ปริมาณ": "ตัน/วัน",
        "ประเภท": "ประเภทข้อมูล"
    },
    title="ปริมาณขยะเกิดขึ้นและนำกลับมาใช้ประโยชน์"
)

fig_region.update_layout(
    height=450
)

st.plotly_chart(
    fig_region,
    use_container_width=True
)


# =========================================================
# TREND OVER YEARS
# =========================================================
st.markdown("---")

st.subheader("📈 แนวโน้มปริมาณขยะของประเทศไทย")


trend = (
    df
    .groupby("year_be")
    .agg(
        ขยะที่เกิดขึ้น=(
            "generated_ton_day",
            "sum"
        ),
        นำกลับมาใช้ประโยชน์=(
            "recycled_ton_day",
            "sum"
        ),
        กำจัดถูกต้อง=(
            "disposed_correct_ton_day",
            "sum"
        ),
        กำจัดไม่ถูกต้อง=(
            "disposed_incorrect_ton_day",
            "sum"
        )
    )
    .reset_index()
)


trend_long = trend.melt(
    id_vars="year_be",
    var_name="ประเภท",
    value_name="ปริมาณ"
)


fig_trend = px.line(
    trend_long,
    x="year_be",
    y="ปริมาณ",
    color="ประเภท",
    markers=True,
    labels={
        "year_be": "ปี พ.ศ.",
        "ปริมาณ": "ปริมาณ (ตัน/วัน)",
        "ประเภท": "ประเภทข้อมูล"
    },
    title="แนวโน้มการจัดการขยะในประเทศไทย"
)

fig_trend.update_layout(
    height=500
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)


# =========================================================
# DATA TABLE
# =========================================================
st.markdown("---")

with st.expander("📋 ดูข้อมูลจังหวัดทั้งหมด"):

    display_df = filtered[
        [
            "province_display",
            "region_display",
            "generated_ton_day",
            "recycled_ton_day",
            "disposed_correct_ton_day",
            "disposed_incorrect_ton_day"
        ]
    ].copy()

    display_df.columns = [
        "จังหวัด",
        "ภูมิภาค",
        "ขยะเกิดขึ้น (ตัน/วัน)",
        "นำกลับมาใช้ประโยชน์ (ตัน/วัน)",
        "กำจัดถูกต้อง (ตัน/วัน)",
        "กำจัดไม่ถูกต้อง (ตัน/วัน)"
    ]

    st.dataframe(
        display_df.style.format({
            "ขยะเกิดขึ้น (ตัน/วัน)": "{:,.2f}",
            "นำกลับมาใช้ประโยชน์ (ตัน/วัน)": "{:,.2f}",
            "กำจัดถูกต้อง (ตัน/วัน)": "{:,.2f}",
            "กำจัดไม่ถูกต้อง (ตัน/วัน)": "{:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.caption(
    "🇹🇭 Thai MSW Analytics | Overview Dashboard"
)