import pandas as pd
import streamlit as st
from utils import load_clean_data

st.set_page_config(page_title="Data Explorer", page_icon="🔍", layout="wide")

st.title("🔍 สำรวจข้อมูลขยะมูลฝอย (Data Explorer)")

df = load_clean_data()

# =========================================================
# FILTER CONTROLS (พร้อมป้องกันข้อมูลที่ไม่เชื่อมโยงกัน)
# =========================================================
st.subheader("🛠️ ตัวกรองข้อมูล")
c1, c2, c3 = st.columns(3)

# 1. กรองปี พ.ศ.
with c1:
    years = sorted(df["year_be"].dropna().unique())
    selected_years = st.multiselect("1. เลือกปี พ.ศ.", years, default=years)

# 2. กรองภูมิภาค
with c2:
    regions = sorted(df["region_display"].dropna().unique())
    selected_regions = st.multiselect(
        "2. เลือกภูมิภาค", regions, default=regions
    )

# 🛡️ ป้องกันความไม่เชื่อมโยง: ดึงเฉพาะ "จังหวัด" ที่อยู่ในภูมิภาคที่ถูกเลือกเท่านั้น
available_provinces = sorted(
    df[df["region_display"].isin(selected_regions)]["province_display"]
    .dropna()
    .unique()
)

# 3. กรองจังหวัด (ที่จะเปลี่ยนตัวเลือกอัตโนมัติตามภูมิภาคที่เลือกใน c2)
with c3:
    selected_provinces = st.multiselect(
        "3. เลือกจังหวัด", available_provinces, default=available_provinces
    )

# =========================================================
# APPLY FILTER & SORTING
# =========================================================
# กรองข้อมูลตามเงื่อนไขทั้ง 3
filtered_df = df[
    (df["year_be"].isin(selected_years))
    & (df["region_display"].isin(selected_regions))
    & (df["province_display"].isin(selected_provinces))
].copy()

# Sort ข้อมูลตามชื่อจังหวัด (ก-ฮ)
sort_order = st.radio(
    "📶 การเรียงลำดับตามชื่อจังหวัด:",
    ["น้อยไปมาก (ก-ฮ)", "มากไปน้อย (ฮ-ก)"],
    horizontal=True,
)
if sort_order == "น้อยไปมาก (ก-ฮ)":
    filtered_df = filtered_df.sort_values(
        by="province_display", ascending=True
    )
else:
    filtered_df = filtered_df.sort_values(
        by="province_display", ascending=False
    )

# =========================================================
# COLUMN RENAME (แปลงชื่อคอลัมน์เป็นภาษาไทย)
# =========================================================
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

# เลือกเฉพาะคอลัมน์สำคัญที่ต้องการแสดงและเปลี่ยนชื่อ
display_cols = [c for c in column_mapping.keys() if c in filtered_df.columns]
display_df = filtered_df[display_cols].rename(columns=column_mapping)

# =========================================================
# DISPLAY TABLE & DOWNLOAD BUTTON
# =========================================================
st.markdown("---")
st.subheader(f"📋 รายการข้อมูล (พบ {len(display_df):,} รายการ)")

# แสดงตารางข้อมูลภาษาไทย
st.dataframe(display_df, use_container_width=True, hide_index=True)

# ดาวน์โหลดไฟล์ CSV ภาษาไทย (utf-8-sig เพื่อเปิดใน Excel แล้วอ่านภาษาไทยออก)
csv = display_df.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    label="📥 ดาวน์โหลดข้อมูล (CSV)",
    data=csv,
    file_name="msw_data_filtered.csv",
    mime="text/csv",
)