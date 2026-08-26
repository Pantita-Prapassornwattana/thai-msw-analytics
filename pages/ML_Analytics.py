import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from utils import load_clean_data

st.set_page_config(page_title="ML Analytics", page_icon="🤖", layout="wide")

st.title("🤖 การวิเคราะห์กลุ่มจังหวัดด้วย Machine Learning (K-Means)")

# โหลดข้อมูลผ่าน utils
df = load_clean_data()

# ตรวจสอบว่ามีข้อมูลหรือไม่
if df.empty:
    st.error("❌ ไม่พบข้อมูลในระบบ")
    st.stop()

# เลือกเฉพาะข้อมูลที่มีค่าตัวเลขครบถ้วน
valid_df = df.dropna(subset=["generated_ton_day", "recycled_ton_day"]).copy()

if valid_df.empty:
    st.warning("⚠️ ไม่พบข้อมูลปริมาณขยะที่สมบูรณ์สำหรับนำมาทำ Machine Learning")
    st.stop()

# ดึงรายการปีที่มีข้อมูลสมบูรณ์จริง
available_years = sorted(valid_df["year_be"].unique(), reverse=True)

# Sidebar สำหรับปรับแต่งโมเดล
st.sidebar.subheader("⚙️ ตั้งค่าโมเดล ML")
selected_year = st.sidebar.selectbox("📅 เลือกปี พ.ศ. ที่ต้องการวิเคราะห์", available_years)
k_clusters = st.sidebar.slider("จำนวนกลุ่ม (Clusters)", min_value=2, max_value=6, value=3)

# กรองข้อมูลตามปีที่เลือก
df_ml = valid_df[valid_df["year_be"] == selected_year].copy()

# ตรวจสอบจำนวนจังหวัดในปีนั้น
if len(df_ml) < k_clusters:
    st.warning(f"⚠️ มีข้อมูลเพียง {len(df_ml)} รายการ ซึ่งน้อยกว่าจำนวน Cluster ({k_clusters}) ที่เลือก")
    st.stop()

# ---------------------------------------------------------
# K-Means Clustering Process
# ---------------------------------------------------------
features = df_ml[["generated_ton_day", "recycled_ton_day"]]

# เทรนโมเดล
kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)
df_ml["Cluster"] = kmeans.fit_predict(features)
df_ml["Cluster"] = "กลุ่มที่ " + (df_ml["Cluster"] + 1).astype(str)

# ---------------------------------------------------------
# Visualizations
# ---------------------------------------------------------
st.subheader(f"📌 ผลการจัดกลุ่มจังหวัด (ปี พ.ศ. {int(selected_year)})")

col1, col2 = st.columns([2, 1])

with col1:
    fig_cluster = px.scatter(
        df_ml,
        x="generated_ton_day",
        y="recycled_ton_day",
        color="Cluster",
        hover_name="province_display",
        labels={
            "generated_ton_day": "ขยะที่เกิดขึ้น (ตัน/วัน)",
            "recycled_ton_day": "นำกลับมาใช้ประโยชน์ (ตัน/วัน)",
            "Cluster": "กลุ่ม"
        },
        title="แผนภาพกระจายตัว (Scatter Plot) ตามสัดส่วนขยะ"
    )
    fig_cluster.update_traces(marker=dict(size=10))
    st.plotly_chart(fig_cluster, use_container_width=True)

with col2:
    st.markdown("#### 📊 สรุปค่าเฉลี่ยแต่ละกลุ่ม")
    summary = df_ml.groupby("Cluster")[["generated_ton_day", "recycled_ton_day"]].mean().reset_index()
    summary.columns = ["กลุ่ม", "ขยะเกิดเฉลี่ย (ตัน/วัน)", "รีไซเคิลเฉลี่ย (ตัน/วัน)"]
    st.dataframe(summary.style.format({"ขยะเกิดเฉลี่ย (ตัน/วัน)": "{:,.2f}", "รีไซเคิลเฉลี่ย (ตัน/วัน)": "{:,.2f}"}), use_container_width=True)

st.markdown("---")
st.subheader("📋 ตารางรายชื่อจังหวัดจำแนกตามกลุ่ม")
st.dataframe(
    df_ml[["province_display", "region_display", "generated_ton_day", "recycled_ton_day", "Cluster"]],
    use_container_width=True
)