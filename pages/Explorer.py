import pandas as pd
import streamlit as st
from utils import load_clean_data
from theme import inject_global_css, page_header, section_title, kpi_card, empty_state, footer, COLORS

st.set_page_config(page_title="Data Explorer & Export", page_icon="🔍", layout="wide", initial_sidebar_state="expanded")
inject_global_css()

with st.spinner("กำลังโหลดข้อมูล..."):
    df = load_clean_data()

if df.empty:
    empty_state()

page_header("🔍", "Data Search & Export (ค้นหาและดาวน์โหลดข้อมูล)", "ค้นหาข้อมูลดิบรายจังหวัด จัดเรียง กรองตามเงื่อนไข และดาวน์โหลดเป็นไฟล์ CSV")

# เตรียมข้อมูลตั้งต้น
all_years = sorted(df["year_be"].dropna().unique())
all_regions = sorted(df[df["region_display"] != "ไม่ระบุ"]["region_display"].dropna().unique())
all_provinces = sorted(df[df["province_display"] != "ไม่ระบุ"]["province_display"].dropna().unique())

# ตรวจสอบการกดปุ่มล้างตัวกรอง (เคลียร์ session_state ก่อนสร้าง Widget)
if st.session_state.get("clear_clicked", False):
    st.session_state.ex_years = []
    st.session_state.ex_regions = []
    st.session_state.ex_provinces = []
    st.session_state.clear_clicked = False

# กำหนดค่าเริ่มต้นใน Session State
if "ex_years" not in st.session_state:
    st.session_state.ex_years = all_years
if "ex_regions" not in st.session_state:
    st.session_state.ex_regions = all_regions
if "ex_provinces" not in st.session_state:
    st.session_state.ex_provinces = all_provinces

# ฟังก์ชันจัดการเมื่อเลือกภาค -> เลือกจังหวัดทั้งหมดในภาคนั้นให้
def handle_region_change():
    selected_reg = st.session_state.get("ex_regions", [])
    if selected_reg:
        provinces_in_reg = sorted(
            df[df["region_display"].isin(selected_reg)]["province_display"]
            .dropna().unique()
        )
        st.session_state.ex_provinces = provinces_in_reg
    else:
        st.session_state.ex_provinces = []

# ฟังก์ชันจัดการเมื่อเลือกจังหวัด -> อัปเดตภาคให้อัตโนมัติ
def handle_province_change():
    selected_prov = st.session_state.get("ex_provinces", [])
    if selected_prov:
        regions_in_prov = sorted(
            df[df["province_display"].isin(selected_prov)]["region_display"]
            .dropna().unique()
        )
        st.session_state.ex_regions = regions_in_prov
    else:
        st.session_state.ex_regions = []

with st.sidebar:
    st.markdown("## 🔍 Explorer")
    st.caption("ค้นหา กรอง และส่งออกข้อมูล")
    st.markdown("---")
    st.markdown("### ⚙️ ตัวกรองการค้นหา")
    
    # 1. เลือกปี พ.ศ.
    st.multiselect("📅 เลือกปี พ.ศ.", all_years, key="ex_years")

    # 2. เลือกภูมิภาค
    st.multiselect("🗺️ เลือกภูมิภาค", all_regions, key="ex_regions", on_change=handle_region_change)

    # 3. เลือกจังหวัด
    st.multiselect("📍 เลือกจังหวัด", all_provinces, key="ex_provinces", on_change=handle_province_change)
    
    st.markdown("---")
    
    # ปุ่มล้างตัวกรองทั้งหมด: ตั้งค่าสถานะ clear_clicked แล้ว rerun
    if st.button("♻️ ล้างตัวกรองทั้งหมด", use_container_width=True):
        st.session_state.clear_clicked = True
        st.rerun()

    st.caption("💡 เลือกภาคจะเลือกจังหวัดให้ทั้งหมด หรือเลือกจังหวัดจะเลือกภาคให้อัตโนมัติ")

# ดึงค่าปัจจุบันมาใช้งาน
selected_years = st.session_state.get("ex_years", [])
selected_regions = st.session_state.get("ex_regions", [])
selected_provinces = st.session_state.get("ex_provinces", [])

if not selected_years or not selected_regions or not selected_provinces:
    empty_state("กรุณาเลือกตัวกรองอย่างน้อย 1 รายการ", "เลือกปี ภูมิภาค หรือจังหวัดจาก Sidebar ด้านซ้ายเพื่อเริ่มค้นหา")

# Filter DataFrame ตามเงื่อนไข
filtered_df = df[
    (df["year_be"].isin(selected_years)) & 
    (df["region_display"].isin(selected_regions)) & 
    (df["province_display"].isin(selected_provinces))
].copy()

if filtered_df.empty:
    empty_state("ไม่พบข้อมูลตรงตามเงื่อนไขที่ค้นหา", "ลองลดเงื่อนไขตัวกรอง หรือตรวจสอบการเลือกข้อมูลแล้วลองใหม่อีกครั้ง")

chip = lambda text: (
    f'<span style="display:inline-block; background:var(--secondary-background-color); color:var(--text-color); '
    f'border:1px solid var(--secondary-background-color); border-radius:999px; padding:4px 12px; '
    f'font-size:12.5px; margin:2px 4px 2px 0;">{text}</span>'
)
years_txt = "ทุกปี" if len(selected_years) == len(all_years) else f"{len(selected_years)} ปี"
regions_txt = "ทุกภูมิภาค" if len(selected_regions) == len(all_regions) else f"{len(selected_regions)} ภูมิภาค"
provinces_txt = "ทุกจังหวัด" if len(selected_provinces) == len(all_provinces) else f"{len(selected_provinces)} จังหวัด"

st.markdown(chip(f"📅 {years_txt}") + chip(f"🗺️ {regions_txt}") + chip(f"📍 {provinces_txt}"), unsafe_allow_html=True)
st.write("")

m1, m2, m3 = st.columns(3)
with m1:
    kpi_card("📋", "จำนวนแถวข้อมูลที่พบ", f"{len(filtered_df):,} รายการ", color=COLORS["primary"])
with m2:
    kpi_card("📅", "จำนวนปีที่ครอบคลุม", f"{filtered_df['year_be'].nunique():,} ปี", color=COLORS["info"])
with m3:
    kpi_card("📍", "จำนวนจังหวัดที่พบ", f"{filtered_df['province_display'].nunique():,} จังหวัด", color=COLORS["success"])

section_title("📋", "ตารางข้อมูล")
column_mapping = {
    "year_be": "ปี พ.ศ.", "region_display": "ภูมิภาค", "province_display": "จังหวัด",
    "generated_ton_day": "ขยะที่เกิดขึ้น", "recycled_ton_day": "รีไซเคิล",
    "disposed_correct_ton_day": "กำจัดถูกต้อง", "disposed_incorrect_ton_day": "กำจัดไม่ถูกต้อง", "residual_ton": "ขยะตกค้างสะสม"
}
display_df = filtered_df[list(column_mapping.keys())].rename(columns=column_mapping)

styled_df = display_df.style.format({
    'ขยะที่เกิดขึ้น': "{:,.2f}", 
    'รีไซเคิล': "{:,.2f}", 
    'กำจัดถูกต้อง': "{:,.2f}", 
    'กำจัดไม่ถูกต้อง': "{:,.2f}", 
    'ขยะตกค้างสะสม': "{:,.2f}"
})

st.dataframe(styled_df, use_container_width=True, hide_index=True, height=500)

csv_data = display_df.to_csv(index=False).encode("utf-8-sig")
dl_col, cap_col = st.columns([0.3, 0.7])
with dl_col:
    st.download_button(label="📥 ดาวน์โหลด CSV", data=csv_data, file_name=f"msw_data_{pd.Timestamp.now().strftime('%Y%m%d')}.csv", mime="text/csv", type="primary", use_container_width=True)
with cap_col:
    st.caption(f"ไฟล์จะมี {len(display_df):,} แถว ตามเงื่อนไขตัวกรองปัจจุบัน · เข้ารหัสแบบ UTF-8-SIG เปิดใน Excel ได้ทันที")
footer("Data Explorer & Export")