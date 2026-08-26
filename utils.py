import pandas as pd
import streamlit as st

@st.cache_data
def load_clean_data():
    waste = pd.read_csv("04_fact_waste_yearly.csv")
    province = pd.read_csv("03_dim_province.csv")
    region = pd.read_csv("01_dim_region.csv")

    # 1. ลบช่องว่างชื่อคอลัมน์
    waste.columns = waste.columns.str.strip()
    province.columns = province.columns.str.strip()
    region.columns = region.columns.str.strip()

    # 2. แปลง year_be เป็นตัวเลข Integer แน่นอน
    if "year_be" in waste.columns:
        waste["year_be"] = pd.to_numeric(waste["year_be"], errors="coerce")
        # 🛠️ กรองตัดปีอนาคต (เอาเฉพาะปี พ.ศ. 2550 ถึง 2567)
        waste = waste.dropna(subset=["year_be"])
        waste = waste[(waste["year_be"] >= 2550) & (waste["year_be"] <= 2567)]
        waste["year_be"] = waste["year_be"].astype(int)

    # 3. แปลงคอลัมน์ตัวเลขอื่นๆ
    numeric_columns = [
        "generated_ton_day", "recycled_ton_day",
        "disposed_correct_ton_day", "disposed_incorrect_ton_day", "residual_ton"
    ]
    for col in numeric_columns:
        if col in waste.columns:
            waste[col] = pd.to_numeric(waste[col], errors="coerce")

    # (โค้ดการ Merge ส่วนที่เหลือคงเดิม...)

    # 🛠️ [เพิ่มจุดนี้] กรองเฉพาะปี พ.ศ. ที่ถูกต้อง (ตัดปีอนาคต หรือปีที่เป็นขยะข้อมูลออก)
    # เช่น เอาเฉพาะปี พ.ศ. ตั้งแต่ 2550 ถึงไม่เกิน 2567
    if "year_be" in waste.columns:
        waste = waste[(waste["year_be"] >= 2550) & (waste["year_be"] <= 2567)]

    # Standardize string keys
    waste["province_code"] = waste["province_code"].astype(str).str.strip()
    province["province_code"] = province["province_code"].astype(str).str.strip()

    # Merge Province
    province_name_col = next((c for c in ["province_name", "province", "province_th", "name"] if c in province.columns), None)
    province_region_code_col = next((c for c in ["region_code", "region_id"] if c in province.columns), None)

    province_cols = ["province_code", province_name_col]
    if province_region_code_col:
        province_cols.append(province_region_code_col)

    waste = waste.merge(province[province_cols].drop_duplicates(), on="province_code", how="left")
    waste["province_display"] = waste[province_name_col].fillna("จังหวัด " + waste["province_code"].astype(str))

    # Merge Region
    region_code_col = next((c for c in ["region_code", "region_id"] if c in region.columns), None)
    region_name_col = next((c for c in ["region_name", "region", "region_th", "name"] if c in region.columns), None)

    if province_region_code_col and region_code_col and region_name_col:
        waste[province_region_code_col] = waste[province_region_code_col].astype(str).str.strip()
        region[region_code_col] = region[region_code_col].astype(str).str.strip()
        waste = waste.merge(
            region[[region_code_col, region_name_col]].drop_duplicates(),
            left_on=province_region_code_col, right_on=region_code_col, how="left"
        )
        waste["region_display"] = waste[region_name_col].fillna("ไม่ระบุ")
    else:
        waste["region_display"] = "ไม่ระบุ"

    return waste