import pandas as pd
import plotly.express as px
import streamlit as st
from utils import load_clean_data, filter_and_aggregate_by_year

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Spatial Analytics - Thai MSW Analytics",
    page_icon="🗺️",
    layout="wide",
)

st.title("🗺️ การวิเคราะห์การกระจายตัวเชิงพื้นที่ (Spatial Analytics)")
st.caption(
    "เจาะลึกความเข้มข้นของปริมาณขยะรายภูมิภาคและรายจังหวัดด้วย Treemap"
)

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

years = sorted(
    df["year_be"].dropna().unique(),
    reverse=True
)

# 🛠️ เพิ่มตัวเลือก "ทั้งหมด" เข้าไปในลิสต์
year_options = ["ทั้งหมด"] + list(years)

selected_year = st.sidebar.selectbox(
    "📅 เลือกปี พ.ศ.",
    year_options,
    index=0
)

metric_options = {
    "🗑️ ขยะที่เกิดขึ้น": "generated_ton_day",
    "♻️ นำกลับมาใช้ประโยชน์": "recycled_ton_day",
    "✅ กำจัดถูกต้อง": "disposed_correct_ton_day",
    "⚠️ กำจัดไม่ถูกต้อง": "disposed_incorrect_ton_day",
    "📦 ขยะตกค้างสะสม": "residual_ton",
}

selected_metric_label = st.sidebar.selectbox(
    "📊 เลือกตัวแปรที่ต้องการวิเคราะห์",
    list(metric_options.keys())
)

selected_metric = metric_options[selected_metric_label]

# =========================================================
# FILTER DATA (ใช้ filter_and_aggregate_by_year)
# =========================================================
# กรองข้อมูลและ GroupBy ตามจังหวัดเมื่อเลือก "ทั้งหมด"
df_year = filter_and_aggregate_by_year(
    df[df["province_display"] != "ไม่ระบุ"],
    selected_year,
    group_by_cols=["province_display"]
)

# กำหนดข้อความแสดงปีให้รองรับ "ทั้งหมด"
if selected_year == "ทั้งหมด":
    year_label = "ทุกปีสะสม (รวมทั้งหมด)"
else:
    year_label = f"พ.ศ. {int(selected_year)}"

if df_year.empty:
    st.warning(
        f"⚠️ ไม่พบข้อมูลสำหรับตัวเลือก {selected_year}"
    )
    st.stop()

# =========================================================
# 1. SPATIAL TREEMAP
# =========================================================
st.markdown("---")

st.subheader(
    f"🧩 สัดส่วนเชิงพื้นที่: "
    f"{selected_metric_label} "
    f"({year_label})"
)

st.caption(
    "ขนาดของกล่องสี่เหลี่ยมแทนปริมาณขยะ "
    "สามารถกดคลิกที่กล่องภูมิภาคเพื่อเจาะลึกรายจังหวัดได้"
)

# =========================================================
# CREATE TREEMAP
# =========================================================
fig_treemap = px.treemap(
    df_year,
    path=[
        px.Constant("ประเทศไทย"),
        "region_display",
        "province_display"
    ],
    values=selected_metric,
    color=selected_metric,

    # =====================================================
    # SOFT GREEN COLOR SCALE
    # =====================================================
    color_continuous_scale=[
        [0.00, "#DDF3E4"],
        [0.20, "#BFE5C9"],
        [0.40, "#9BD3AD"],
        [0.60, "#70BC8D"],
        [0.80, "#45A66D"],
        [1.00, "#287A50"],
    ],

    hover_data=[selected_metric],
)

# =========================================================
# TREEMAP STYLE
# =========================================================
fig_treemap.update_traces(
    root_color="#F3F8F4",

    marker=dict(
        line=dict(
            color="#FFFFFF",
            width=1.5
        )
    ),

    textfont=dict(
        size=13
    ),

    hovertemplate=(
        "<b>%{label}</b><br>"
        "ปริมาณ: %{value:,.2f} ตัน/วัน"
        "<extra></extra>"
    ),
)

# =========================================================
# TREEMAP LAYOUT
# =========================================================
fig_treemap.update_layout(
    height=550,

    margin=dict(
        t=15,
        l=5,
        r=5,
        b=5
    ),

    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",

    coloraxis_colorbar=dict(
        title="ปริมาณ",
        thickness=12,
        len=0.65,
        outlinewidth=0,
        tickfont=dict(
            size=11
        ),
        title_font=dict(
            size=12
        ),
    ),
)

# =========================================================
# DISPLAY TREEMAP
# =========================================================
st.plotly_chart(
    fig_treemap,
    use_container_width=True
)

# =========================================================
# 2. REGIONAL COMPARISON TABLE & HOTSPOTS
# =========================================================
st.markdown("---")

col_reg, col_top = st.columns([1, 1])

# =========================================================
# REGIONAL SUMMARY
# =========================================================
with col_reg:

    st.subheader("📍 สรุปปริมาณแยกรายภาค")

    reg_summary = (
        df_year
        .groupby("region_display")[selected_metric]
        .sum()
        .reset_index()
        .sort_values(
            by=selected_metric,
            ascending=False
        )
    )

    reg_summary.columns = [
        "ภูมิภาค",
        "ปริมาณรวม (ตัน/วัน)"
    ]

    st.dataframe(
        reg_summary.style.format(
            {
                "ปริมาณรวม (ตัน/วัน)": "{:,.2f}"
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

# =========================================================
# TOP 5 HOTSPOTS
# =========================================================
with col_top:

    st.subheader(
        "🔥 5 จังหวัด Hotspot ที่มีปริมาณสูงสุด"
    )

    top5_prov = (
        df_year
        .nlargest(
            5,
            selected_metric
        )[
            [
                "province_display",
                "region_display",
                selected_metric
            ]
        ]
    )

    top5_prov.columns = [
        "จังหวัด",
        "ภูมิภาค",
        "ปริมาณ (ตัน/วัน)"
    ]

    st.dataframe(
        top5_prov.style.format(
            {
                "ปริมาณ (ตัน/วัน)": "{:,.2f}"
            }
        ),
        use_container_width=True,
        hide_index=True,
    )