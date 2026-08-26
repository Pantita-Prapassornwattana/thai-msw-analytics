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


# =========================================================
# 🛠️ ฟังก์ชันสำหรับกรองข้อมูลปี (กรองปีเฉพาะ หรือ รวมทุกปี)
# =========================================================
def filter_and_aggregate_by_year(df, selected_year, group_by_cols=None, agg_func="sum"):
    """
    ฟังก์ชันช่วยจัดการตัวเลือกปี:
    - ถ้าเลือก "ทั้งหมด" หรือมีคำว่า "ทั้งหมด": 
        * หากระบุ group_by_cols จะทำ GroupBy เพื่อหา sum หรือ mean รายจังหวัด
        * หากไม่ระบุ group_by_cols จะคืนค่า dataframe ทั้งหมด
    - ถ้าเลือกปี พ.ศ. เฉพาะ: กรองเอาข้อมูลเฉพาะปีนั้น
    """
    if df.empty:
        return df.copy()

    # เช็กเงื่อนไขว่าผู้ใช้เลือกตัวเลือก "ทั้งหมด" หรือไม่
    is_all = False
    if isinstance(selected_year, str) and "ทั้งหมด" in selected_year:
        is_all = True
    elif selected_year == "ทั้งหมด":
        is_all = True

    if is_all:
        if group_by_cols:
            # รายการคอลัมน์ตัวเลขที่ต้องการรวม/หาค่าเฉลี่ย
            num_cols = [
                "generated_ton_day", "recycled_ton_day", 
                "disposed_correct_ton_day", "disposed_incorrect_ton_day", 
                "residual_ton"
            ]
            valid_num_cols = [c for c in num_cols if c in df.columns]

            # คำนวณ Sum หรือ Mean
            if agg_func == "mean":
                agg_df = df.groupby(group_by_cols, as_index=False)[valid_num_cols].mean()
            else:
                agg_df = df.groupby(group_by_cols, as_index=False)[valid_num_cols].sum()

            # ดึงข้อมูล region_display กลับมาผูกคืนกรณี GroupBy แค่รายจังหวัด
            if "province_display" in group_by_cols and "region_display" in df.columns and "region_display" not in agg_df.columns:
                ref_map = df.drop_duplicates(subset=["province_display"])[["province_display", "region_display"]]
                agg_df = agg_df.merge(ref_map, on="province_display", how="left")

            return agg_df
        return df.copy()
    else:
        # กรณีกรองเฉพาะปี เช่น 2565
        return df[df["year_be"] == int(selected_year)].copy()