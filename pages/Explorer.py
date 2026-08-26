import pandas as pd
import streamlit as st
from utils import load_clean_data

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Data Explorer & Export",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
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
st.title("🔍 Data Search & Export (ค้นหาและดาวน์โหลดข้อมูล)")
st.caption("ค้นหาข้อมูลดิบรายจังหวัด จัดเรียง กรองตามเงื่อนไข และดาวน์โหลดเป็นไฟล์ CSV")

# =========================================================
# SIDEBAR FILTERS
# =========================================================
with st.sidebar:
    st.header("⚙️ ตัวกรองการค้นหา")

    # Filter ปี
    years = sorted(df["year_be"].dropna().unique())
    selected_years = st.multiselect("📅 เลือกปี พ.ศ.", years, default=years)

    # Filter ภาค
    regions = sorted(df["region_display"].dropna().unique())
    selected_regions = st.multiselect("🗺️ เลือกภูมิภาค", regions, default=regions)

    # Filter จังหวัด
    available_provinces = sorted(
        df[df["region_display"].isin(selected_regions)]["province_display"]
        .dropna()
        .unique()
    )
    selected_provinces = st.multiselect("📍 เลือกจังหวัด", available_provinces, default=available_provinces)

    st.divider()

    # Search Box
    search_keyword = st.text_input("🔎 พิมพ์ค้นชื่อจังหวัด", "")

# Validation
if not selected_years or not selected_regions or not selected_provinces:
    st.warning("⚠️ กรุณาเลือกตัวกรองอย่างน้อย 1 รายการ")
    st.stop()

# Filter DataFrame
filtered_df = df[
    (df["year_be"].isin(selected_years))
    & (df["region_display"].isin(selected_regions))
    & (df["province_display"].isin(selected_provinces))
].copy()

if search_keyword:
    filtered_df = filtered_df[
        filtered_df["province_display"].str.contains(search_keyword, na=False)
    ]

if filtered_df.empty:
    st.warning("⚠️ ไม่พบข้อมูลตรงตามเงื่อนไขที่ค้นหา")
    st.stop()

# =========================================================
# METRIC SUMMARY
# =========================================================
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("📋 จำนวนแถวข้อมูลที่พบ", f"{len(filtered_df):,} รายการ")
with m2:
    st.metric("📅 จำนวนปีที่ครอบคลุม", f"{filtered_df['year_be'].nunique():,} ปี")
with m3:
    st.metric("📍 จำนวนจังหวัดที่พบ", f"{filtered_df['province_display'].nunique():,} จังหวัด")

# =========================================================
# DATA TABLE & EXPORT
# =========================================================
st.markdown("---")

column_mapping = {
    "year_be": "ปี พ.ศ.",
    "region_display": "ภูมิภาค",
    "province_display": "จังหวัด",
    "generated_ton_day": "ขยะที่เกิดขึ้น (ตัน/วัน)",
    "recycled_ton_day": "นำกลับมาใช้ประโยชน์ (ตัน/วัน)",
    "disposed_correct_ton_day": "กำจัดถูกต้อง (ตัน/วัน)",
    "disposed_incorrect_ton_day": "กำจัดไม่ถูกต้อง (ตัน/วัน)",
    "residual_ton": "ขยะตกค้างสะสม (ตัน)",
}

display_df = filtered_df[list(column_mapping.keys())].rename(columns=column_mapping)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=500,
)

# Export CSV
csv_data = display_df.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="📥 ดาวน์โหลดข้อมูลตารางนี้เป็นไฟล์ CSV",
    data=csv_data,
    file_name=f"msw_data_export_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
    type="primary",
)