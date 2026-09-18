import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from utils import load_clean_data, filter_and_aggregate_by_year
from theme import inject_global_css, page_header, section_title, kpi_card, info_card, empty_state, footer, style_fig, COLORS

st.set_page_config(page_title="ML Analytics", page_icon="🤖", layout="wide")
inject_global_css()

with st.spinner("กำลังโหลดข้อมูล..."):
    df = load_clean_data()
valid_df = df.dropna(subset=["generated_ton_day", "recycled_ton_day"]).copy()

if valid_df.empty:
    empty_state("ไม่พบข้อมูลสำหรับ ML", "จำเป็นต้องมีข้อมูลขยะเกิดและรีไซเคิลครบถ้วน")

page_header("🤖", "Machine Learning Analytics", "การวิเคราะห์และจัดกลุ่มจังหวัดด้วย K-Means Clustering")

with st.sidebar:
    st.markdown("## 🤖 ML Analytics")
    st.markdown("---")
    st.markdown("### ⚙️ ตั้งค่า Machine Learning")
    years = ["ทั้งหมด (ค่าเฉลี่ยทุกปี)"] + list(sorted(valid_df["year_be"].unique(), reverse=True))
    selected_year = st.selectbox("📅 เลือกปี พ.ศ.", years)
    k_clusters = st.slider("🔢 จำนวนกลุ่ม (Clusters)", 2, 6, 3)

df_ml = filter_and_aggregate_by_year(valid_df[valid_df["province_display"] != "ไม่ระบุ"], selected_year, group_by_cols=["province_display", "region_display"], agg_func="mean")

# [ส่วนที่แก้ไข] แปลง selected_year เป็น string ก่อนใช้ .startswith() ป้องกัน Error
selected_year_str = str(selected_year)
year_label = "ค่าเฉลี่ยทุกปีสะสม" if selected_year_str.startswith("ทั้งหมด") else f"ปี พ.ศ. {int(selected_year)}"

features = df_ml[["generated_ton_day", "recycled_ton_day"]]
scaled_features = StandardScaler().fit_transform(features)
kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)
df_ml["Cluster_ID"] = kmeans.fit_predict(scaled_features)
df_ml["Cluster"] = "กลุ่มที่ " + (df_ml["Cluster_ID"] + 1).astype(str)

silhouette = silhouette_score(scaled_features, df_ml["Cluster_ID"]) if k_clusters >= 2 and len(df_ml) > k_clusters else 0

section_title("📊", f"ภาพรวมการจัดกลุ่ม · {year_label}")
c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("🏙️", "จำนวนจังหวัด", f"{len(df_ml):,}", color=COLORS["primary"])
with c2:
    kpi_card("🔢", "จำนวนกลุ่ม", str(k_clusters), color=COLORS["purple"])
with c3:
    kpi_card("♻️", "ขยะเกิดเฉลี่ย", f"{df_ml['generated_ton_day'].mean():,.2f} ตัน", color=COLORS["success"])
with c4:
    quality = "ดี" if silhouette >= 0.5 else ("ปานกลาง" if silhouette >= 0.25 else "ปรับปรุง")
    kpi_card("📈", "Silhouette Score", f"{silhouette:.3f}", quality, color=COLORS["info"])

st.write("")

tab1, tab2 = st.tabs(["🎯 กราฟกระจายตัว & การตีความ", "📋 ตารางข้อมูลจังหวัดจำแนกกลุ่ม"])

with tab1:
    col_chart, col_inter = st.columns([2.5, 1.8])
    with col_chart:
        fig = px.scatter(
            df_ml, x="generated_ton_day", y="recycled_ton_day", color="Cluster", hover_name="province_display",
            labels={"generated_ton_day": "ขยะเกิด (ตัน/วัน)", "recycled_ton_day": "รีไซเคิล (ตัน/วัน)"},
            color_discrete_sequence=px.colors.qualitative.Set1, title="การจัดกลุ่มจังหวัด (Scatter Plot)"
        )
        fig.update_traces(marker=dict(size=14, opacity=0.8, line=dict(width=1, color='white')))
        style_fig(fig, height=550, legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
        st.plotly_chart(fig, use_container_width=True)
    
    with col_inter:
        st.write("#### 🧠 การตีความลักษณะเฉพาะ")
        summary = df_ml.groupby("Cluster").agg({
            "province_display": "count", 
            "generated_ton_day": "mean", 
            "recycled_ton_day": "mean"
        }).reset_index()
        summary.columns = ["Cluster", "จำนวนจังหวัด", "ขยะเกิดเฉลี่ย", "รีไซเคิลเฉลี่ย"]
        summary = summary.sort_values("ขยะเกิดเฉลี่ย")
        
        for _, row in summary.iterrows():
            cluster_name = row["Cluster"]
            gen, rec, count = row["ขยะเกิดเฉลี่ย"], row["รีไซเคิลเฉลี่ย"], row["จำนวนจังหวัด"]
            ratio = (rec / gen * 100) if gen > 0 else 0
            
            msg = f"**{cluster_name}** ({int(count)} จ.)\n\nเกิด {gen:,.1f} ตัน | รีไซเคิล {ratio:.1f}%"
            if ratio >= 30:
                st.success(f"🌟 กลุ่มประสิทธิภาพดี:\n{msg}")
            elif ratio >= 15:
                st.info(f"🔹 กลุ่มทั่วไป:\n{msg}")
            else:
                st.warning(f"⚠️ กลุ่มที่ต้องเฝ้าระวัง (รีไซเคิลต่ำ):\n{msg}")

with tab2:
    selected_c = st.selectbox("🔎 เลือกดูกลุ่ม", ["ทั้งหมด"] + sorted(df_ml["Cluster"].unique()))
    disp_df = df_ml if selected_c == "ทั้งหมด" else df_ml[df_ml["Cluster"] == selected_c]
    disp_df = disp_df[["province_display", "region_display", "generated_ton_day", "recycled_ton_day", "Cluster"]]
    disp_df.columns = ["จังหวัด", "ภูมิภาค", "ขยะเกิด (ตัน)", "รีไซเคิล (ตัน)", "กลุ่ม"]
    
    st.dataframe(
        disp_df.sort_values("ขยะเกิด (ตัน)", ascending=False)
               .style.bar(subset=["ขยะเกิด (ตัน)"], color="#FCA5A5")
               .bar(subset=["รีไซเคิล (ตัน)"], color="#6EE7B7")
               .format({"ขยะเกิด (ตัน)": "{:,.2f}", "รีไซเคิล (ตัน)": "{:,.2f}"}),
        use_container_width=True, hide_index=True, height=500
    )

footer("ML Analytics")