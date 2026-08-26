import streamlit as st
import pandas as pd
import plotly.express as px
from pages.Overview import load_clean_data

st.set_page_config(page_title="Trends - Thai MSW Analytics", page_icon="📈", layout="wide")
df = load_clean_data()

st.title("📈 การวิเคราะห์แนวโน้มปริมาณขยะ (Time-Series Analytics)")

# Filters
regions = ["ทั้งหมด"] + sorted([r for r in df["region_display"].unique() if r != "ไม่ระบุ"])
selected_region = st.sidebar.selectbox("🗺️ เลือกภูมิภาค", regions)

df_filtered = df.copy()
if selected_region != "ทั้งหมด":
    df_filtered = df_filtered[df_filtered["region_display"] == selected_region]

# Trend chart
trend_df = df_filtered.groupby("year_be")[["generated_ton_day", "recycled_ton_day", "disposed_correct_ton_day"]].sum().reset_index()

fig_line = px.line(trend_df, x="year_be", y=["generated_ton_day", "recycled_ton_day", "disposed_correct_ton_day"],
                   labels={"value": "ปริมาณ (ตัน/วัน)", "year_be": "ปี พ.ศ.", "variable": "ประเภท"},
                   title=f"แนวโน้มปริมาณและการจัดการขยะ ({selected_region})", markers=True)
st.plotly_chart(fig_line, use_container_width=True)