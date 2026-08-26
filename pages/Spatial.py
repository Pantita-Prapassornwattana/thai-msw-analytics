import streamlit as st
import pandas as pd
import plotly.express as px
from pages.Overview import load_clean_data

st.set_page_config(page_title="Spatial Analytics", page_icon="🗺️", layout="wide")
df = load_clean_data()

st.title("🗺️ การกระจายตัวเชิงพื้นที่ (Spatial Analytics)")

years = sorted(df["year_be"].dropna().unique())
selected_year = st.sidebar.selectbox("📅 เลือกปี พ.ศ.", years, index=len(years)-1)

filtered = df[df["year_be"] == selected_year]

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🌎 ปริมาณขยะแบ่งตามภูมิภาค")
    reg_df = filtered.groupby("region_display")["generated_ton_day"].sum().reset_index().sort_values("generated_ton_day", ascending=True)
    fig_reg = px.bar(reg_df[reg_df["region_display"] != "ไม่ระบุ"], x="generated_ton_day", y="region_display", orientation="h")
    st.plotly_chart(fig_reg, use_container_width=True)

with col_right:
    st.subheader("🏆 10 อันดับจังหวัดที่มีปริมาณขยะสูงสุด")
    top10 = filtered.groupby("province_display")["generated_ton_day"].sum().reset_index().sort_values("generated_ton_day", ascending=False).head(10)
    fig_top = px.bar(top10.sort_values("generated_ton_day", ascending=True), x="generated_ton_day", y="province_display", orientation="h")
    st.plotly_chart(fig_top, use_container_width=True)