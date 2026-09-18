import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_clean_data
from theme import inject_global_css, page_header, section_title, kpi_card, empty_state, footer, style_fig, COLORS

st.set_page_config(page_title="Trends - Thai MSW Analytics", page_icon="📈", layout="wide")
inject_global_css()

df = load_clean_data()
if df.empty:
    empty_state()

page_header("📈", "การวิเคราะห์แนวโน้มปริมาณขยะ (Trends)", "วิเคราะห์การเปลี่ยนแปลงปริมาณขยะในแต่ละปี พร้อมเปรียบเทียบแนวโน้มระหว่างภูมิภาค")

with st.sidebar:
    st.markdown("## 📈 Trends")
    st.markdown("---")
    st.markdown("### ⚙️ ตัวกรองข้อมูล")
    regions = ["ทั้งหมด"] + sorted([r for r in df["region_display"].dropna().unique() if r != "ไม่ระบุ"])
    selected_region = st.selectbox("🗺️ เลือกภูมิภาค", regions)
    
    df_filtered = df.copy() if selected_region == "ทั้งหมด" else df[df["region_display"] == selected_region]
    available_years = sorted(df_filtered["year_be"].dropna().unique())
    if len(available_years) < 2:
        empty_state("ข้อมูลไม่เพียงพอ", "มีข้อมูลน้อยกว่า 2 ปี จึงไม่สามารถวิเคราะห์แนวโน้มได้")
        
    selected_year_range = st.slider("📅 ช่วงปีที่ต้องการวิเคราะห์", int(min(available_years)), int(max(available_years)), (int(min(available_years)), int(max(available_years))))
    df_filtered = df_filtered[df_filtered["year_be"].between(selected_year_range[0], selected_year_range[1])]
    
    metric_options = {
        "🗑️ ขยะที่เกิดขึ้น": "generated_ton_day",
        "♻️ นำกลับมาใช้ประโยชน์": "recycled_ton_day",
        "✅ กำจัดถูกต้อง": "disposed_correct_ton_day",
        "⚠️ กำจัดไม่ถูกต้อง": "disposed_incorrect_ton_day"
    }
    selected_metric_label = st.selectbox("📊 เลือกตัวแปรหลัก", list(metric_options.keys()))
    selected_metric = metric_options[selected_metric_label]
    metric_name = selected_metric_label.split(" ", 1)[1]

trend_df = df_filtered.groupby("year_be")[list(metric_options.values())].sum().reset_index().sort_values("year_be")

first_val, last_val = trend_df[selected_metric].iloc[0], trend_df[selected_metric].iloc[-1]
change_pct = ((last_val - first_val) / first_val) * 100 if first_val else 0

section_title("📊", f"สรุปแนวโน้ม: {metric_name}")
col1, col2, col3, col4 = st.columns(4)
with col1:
    kpi_card("📅", "ปีแรกสุด", f"{first_val:,.0f} ตัน", f"พ.ศ. {int(trend_df['year_be'].iloc[0])}", color=COLORS["info"])
with col2:
    kpi_card("📅", "ปีล่าสุด", f"{last_val:,.0f} ตัน", f"พ.ศ. {int(trend_df['year_be'].iloc[-1])}", color=COLORS["info"])
with col3:
    c_color = COLORS["danger"] if change_pct > 0 and "ไม่ถูก" in metric_name else COLORS["success"]
    kpi_card("📊", "การเปลี่ยนแปลงสะสม", f"{change_pct:+.2f}%", color=c_color)
with col4:
    kpi_card("📌", "ค่าเฉลี่ยต่อปี", f"{trend_df[selected_metric].mean():,.0f} ตัน", color=COLORS["primary"])

st.write("")

tab1, tab2, tab3 = st.tabs(["🔄 เปรียบเทียบทุกมิติ (ภาพรวม)", "📈 แนวโน้มตัวแปรเดียว & YoY", "📋 ข้อมูลตารางไล่สี"])

with tab1:
    comp_df = trend_df.copy()
    comp_df.columns = ["ปี พ.ศ.", "ขยะที่เกิดขึ้น", "นำกลับมาใช้ประโยชน์", "กำจัดถูกต้อง", "กำจัดไม่ถูกต้อง"]
    comp_long = comp_df.melt(id_vars="ปี พ.ศ.", var_name="ประเภท", value_name="ปริมาณ (ตัน/วัน)")
    
    color_map = {"ขยะที่เกิดขึ้น": COLORS["purple"], "นำกลับมาใช้ประโยชน์": COLORS["success"], "กำจัดถูกต้อง": COLORS["info"], "กำจัดไม่ถูกต้อง": COLORS["danger"]}
    fig_comp = px.line(comp_long, x="ปี พ.ศ.", y="ปริมาณ (ตัน/วัน)", color="ประเภท", markers=True, color_discrete_map=color_map)
    fig_comp.update_traces(line=dict(width=3), marker=dict(size=8))
    style_fig(fig_comp, height=450, hovermode="x unified")
    st.plotly_chart(fig_comp, use_container_width=True)

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        fig_line = px.line(trend_df, x="year_be", y=selected_metric, markers=True, title=f"ปริมาณ {metric_name}")
        fig_line.update_traces(line=dict(color=COLORS["primary"], width=4), marker=dict(size=10))
        style_fig(fig_line)
        st.plotly_chart(fig_line, use_container_width=True)
    with col_b:
        trend_yoy = trend_df.copy()
        trend_yoy["yoy_change"] = trend_yoy[selected_metric].pct_change() * 100
        trend_yoy["color"] = trend_yoy["yoy_change"].apply(lambda x: "ลดลง" if x < 0 else "เพิ่มขึ้น")
        fig_yoy = px.bar(trend_yoy, x="year_be", y="yoy_change", color="color", text="yoy_change", title="อัตราการเติบโต YoY (%)", color_discrete_map={"ลดลง": COLORS["success"], "เพิ่มขึ้น": COLORS["danger"]})
        fig_yoy.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        style_fig(fig_yoy)
        st.plotly_chart(fig_yoy, use_container_width=True)

with tab3:
    st.dataframe(
        comp_df.style.background_gradient(cmap='Purples', subset=['ขยะที่เกิดขึ้น'])
               .background_gradient(cmap='Greens', subset=['นำกลับมาใช้ประโยชน์'])
               .background_gradient(cmap='Blues', subset=['กำจัดถูกต้อง'])
               .background_gradient(cmap='Reds', subset=['กำจัดไม่ถูกต้อง'])
               .format("{:,.2f}", subset=["ขยะที่เกิดขึ้น", "นำกลับมาใช้ประโยชน์", "กำจัดถูกต้อง", "กำจัดไม่ถูกต้อง"]),
        use_container_width=True, hide_index=True
    )

footer("Time-Series Analytics")