import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

from utils import load_clean_data


# =========================================================
# Page Configuration
# =========================================================
st.set_page_config(
    page_title="ML Analytics",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# Title
# =========================================================
st.title("🤖 Machine Learning Analytics")
st.subheader("การวิเคราะห์และจัดกลุ่มจังหวัดด้วย K-Means Clustering")

st.markdown("""
ระบบใช้ **K-Means Clustering** เพื่อจัดกลุ่มจังหวัดที่มีลักษณะ
การเกิดขยะและการนำขยะกลับมาใช้ประโยชน์ใกล้เคียงกัน
โดยสามารถเลือกปีและจำนวนกลุ่มที่ต้องการวิเคราะห์ได้
""")

st.markdown("---")


# =========================================================
# Load Data
# =========================================================
df = load_clean_data()

if df.empty:
    st.error("❌ ไม่พบข้อมูลในระบบ")
    st.stop()


# =========================================================
# Prepare Data
# =========================================================
required_columns = [
    "generated_ton_day",
    "recycled_ton_day",
    "year_be",
    "province_display",
    "region_display"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        f"❌ ไม่พบคอลัมน์ที่จำเป็น: {', '.join(missing_columns)}"
    )
    st.stop()


valid_df = df.dropna(
    subset=[
        "generated_ton_day",
        "recycled_ton_day"
    ]
).copy()

if valid_df.empty:
    st.warning(
        "⚠️ ไม่พบข้อมูลปริมาณขยะที่สมบูรณ์ "
        "สำหรับนำมาทำ Machine Learning"
    )
    st.stop()


# =========================================================
# Sidebar
# =========================================================
st.sidebar.header("⚙️ ตั้งค่า Machine Learning")

available_years = sorted(
    valid_df["year_be"].unique(),
    reverse=True
)

selected_year = st.sidebar.selectbox(
    "📅 เลือกปี พ.ศ.",
    available_years
)

k_clusters = st.sidebar.slider(
    "🔢 จำนวนกลุ่ม (Clusters)",
    min_value=2,
    max_value=6,
    value=3
)

st.sidebar.markdown("---")

st.sidebar.markdown("""
### 📌 ตัวแปรที่ใช้

**X1:** ปริมาณขยะที่เกิดขึ้น  
**X2:** ปริมาณขยะที่นำกลับมาใช้ประโยชน์

ก่อนทำ K-Means ระบบจะทำ **Standardization**
เพื่อให้ตัวแปรทั้งสองมีสเกลที่เหมาะสม
""")


# =========================================================
# Filter Year
# =========================================================
df_ml = valid_df[
    valid_df["year_be"] == selected_year
].copy()

if len(df_ml) < k_clusters:
    st.warning(
        f"⚠️ ปี พ.ศ. {selected_year} มีข้อมูลเพียง "
        f"{len(df_ml)} จังหวัด "
        f"ซึ่งน้อยกว่าจำนวน Cluster ({k_clusters})"
    )
    st.stop()


# =========================================================
# Features
# =========================================================
features = df_ml[
    [
        "generated_ton_day",
        "recycled_ton_day"
    ]
].copy()


# =========================================================
# Standardization
# =========================================================
scaler = StandardScaler()

scaled_features = scaler.fit_transform(features)


# =========================================================
# K-Means
# =========================================================
kmeans = KMeans(
    n_clusters=k_clusters,
    random_state=42,
    n_init=10
)

cluster_numbers = kmeans.fit_predict(
    scaled_features
)

df_ml["Cluster_ID"] = cluster_numbers

df_ml["Cluster"] = (
    "กลุ่มที่ "
    + (cluster_numbers + 1).astype(str)
)


# =========================================================
# Silhouette Score
# =========================================================
if k_clusters >= 2 and len(df_ml) > k_clusters:

    silhouette = silhouette_score(
        scaled_features,
        cluster_numbers
    )

else:
    silhouette = 0


# =========================================================
# KPI
# =========================================================
st.subheader(
    f"📊 ภาพรวมการจัดกลุ่ม ปี พ.ศ. {int(selected_year)}"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🏙️ จำนวนจังหวัด",
        f"{len(df_ml):,}"
    )

with col2:
    st.metric(
        "🔢 จำนวนกลุ่ม",
        k_clusters
    )

with col3:
    st.metric(
        "♻️ ขยะเกิดเฉลี่ย",
        f"{df_ml['generated_ton_day'].mean():,.2f} ตัน/วัน"
    )

with col4:
    st.metric(
        "📈 Silhouette Score",
        f"{silhouette:.3f}"
    )


st.markdown("---")


# =========================================================
# Main Visualization
# =========================================================
st.subheader("🎯 การกระจายตัวของจังหวัดแต่ละกลุ่ม")

col1, col2 = st.columns([2.2, 1])


# ---------------------------------------------------------
# Scatter Plot
# ---------------------------------------------------------
with col1:

    fig_cluster = px.scatter(
        df_ml,
        x="generated_ton_day",
        y="recycled_ton_day",
        color="Cluster",
        hover_name="province_display",
        hover_data={
            "region_display": True,
            "generated_ton_day": ":,.2f",
            "recycled_ton_day": ":,.2f",
            "Cluster": True
        },
        labels={
            "generated_ton_day":
                "ขยะที่เกิดขึ้น (ตัน/วัน)",

            "recycled_ton_day":
                "นำกลับมาใช้ประโยชน์ (ตัน/วัน)",

            "Cluster":
                "กลุ่ม"
        },
        title=(
            f"K-Means Clustering "
            f"ปี พ.ศ. {int(selected_year)}"
        )
    )

    fig_cluster.update_traces(
        marker=dict(size=11)
    )

    fig_cluster.update_layout(
        height=520,
        legend_title="กลุ่มจังหวัด"
    )

    st.plotly_chart(
        fig_cluster,
        use_container_width=True
    )


# ---------------------------------------------------------
# Cluster Summary
# ---------------------------------------------------------
with col2:

    st.markdown("#### 📊 สรุปแต่ละกลุ่ม")

    cluster_summary = (
        df_ml
        .groupby("Cluster")
        .agg(
            จำนวนจังหวัด=(
                "province_display",
                "count"
            ),

            ขยะเกิดเฉลี่ย=(
                "generated_ton_day",
                "mean"
            ),

            รีไซเคิลเฉลี่ย=(
                "recycled_ton_day",
                "mean"
            )
        )
        .reset_index()
    )

    cluster_summary = cluster_summary.sort_values(
        "Cluster"
    )

    st.dataframe(
        cluster_summary.style.format({
            "ขยะเกิดเฉลี่ย": "{:,.2f}",
            "รีไซเคิลเฉลี่ย": "{:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# Cluster Distribution
# =========================================================
st.markdown("---")

st.subheader("📊 จำนวนจังหวัดในแต่ละกลุ่ม")

cluster_count = (
    df_ml["Cluster"]
    .value_counts()
    .reset_index()
)

cluster_count.columns = [
    "Cluster",
    "จำนวนจังหวัด"
]

cluster_count = cluster_count.sort_values(
    "Cluster"
)

fig_count = px.bar(
    cluster_count,
    x="Cluster",
    y="จำนวนจังหวัด",
    text="จำนวนจังหวัด",
    labels={
        "Cluster": "กลุ่ม",
        "จำนวนจังหวัด": "จำนวนจังหวัด"
},
    title="จำนวนจังหวัดในแต่ละ Cluster"
)

fig_count.update_traces(
    textposition="outside"
)

fig_count.update_layout(
    height=400
)

st.plotly_chart(
    fig_count,
    use_container_width=True
)



# =========================================================
# Cluster Interpretation
# =========================================================
st.markdown("---")

st.subheader("🧠 ลักษณะของแต่ละกลุ่ม")

# สร้างตารางสรุปใหม่
interpretation = (
    df_ml.groupby("Cluster")
    .agg({
        "province_display": "count",
        "generated_ton_day": "mean",
        "recycled_ton_day": "mean"
    })
    .reset_index()
)

# เปลี่ยนชื่อคอลัมน์หลังจาก aggregate
interpretation.columns = [
    "Cluster",
    "จำนวนจังหวัด",
    "ขยะเกิดเฉลี่ย",
    "รีไซเคิลเฉลี่ย"
]

# ค่าเฉลี่ยรวมของทุกจังหวัด
overall_generated = df_ml["generated_ton_day"].mean()
overall_recycled = df_ml["recycled_ton_day"].mean()


for _, row in interpretation.iterrows():

    cluster_name = row["Cluster"]

    generated = row["ขยะเกิดเฉลี่ย"]
    recycled = row["รีไซเคิลเฉลี่ย"]

    province_count = row["จำนวนจังหวัด"]

    # -----------------------------------------
    # วิเคราะห์ลักษณะของ Cluster
    # -----------------------------------------
    if (
        generated >= overall_generated
        and recycled >= overall_recycled
    ):
        description = (
            "มีปริมาณขยะเกิดขึ้นสูง "
            "และมีการนำกลับมาใช้ประโยชน์สูง"
        )

    elif (
        generated >= overall_generated
        and recycled < overall_recycled
    ):
        description = (
            "มีปริมาณขยะเกิดขึ้นสูง "
            "แต่มีการนำกลับมาใช้ประโยชน์ค่อนข้างต่ำ"
        )

    elif (
        generated < overall_generated
        and recycled >= overall_recycled
    ):
        description = (
            "มีปริมาณขยะเกิดขึ้นไม่สูงมาก "
            "แต่มีการนำกลับมาใช้ประโยชน์ในระดับสูง"
        )

    else:
        description = (
            "มีปริมาณขยะเกิดขึ้นและการนำกลับมาใช้ประโยชน์ "
            "อยู่ในระดับค่อนข้างต่ำ"
        )

    # -----------------------------------------
    # แสดงผล
    # -----------------------------------------
    st.info(
        f"**{cluster_name}** — "
        f"{description} "
        f"จำนวน {int(province_count)} จังหวัด"
    )

# =========================================================
# Province Table
# =========================================================
st.markdown("---")

st.subheader("📋 รายชื่อจังหวัดจำแนกตามกลุ่ม")


selected_cluster = st.selectbox(
    "🔎 เลือกกลุ่มที่ต้องการดู",
    ["ทั้งหมด"] + sorted(df_ml["Cluster"].unique())
)

if selected_cluster != "ทั้งหมด":

    display_df = df_ml[
        df_ml["Cluster"] == selected_cluster
    ].copy()

else:

    display_df = df_ml.copy()


display_df = display_df.sort_values(
    "generated_ton_day",
    ascending=False
)


display_df = display_df[
    [
        "province_display",
        "region_display",
        "generated_ton_day",
        "recycled_ton_day",
        "Cluster"
    ]
].copy()


display_df.columns = [
    "จังหวัด",
    "ภูมิภาค",
    "ขยะที่เกิดขึ้น (ตัน/วัน)",
    "นำกลับมาใช้ประโยชน์ (ตัน/วัน)",
    "กลุ่ม"
]


st.dataframe(
    display_df.style.format({
        "ขยะที่เกิดขึ้น (ตัน/วัน)": "{:,.2f}",
        "นำกลับมาใช้ประโยชน์ (ตัน/วัน)": "{:,.2f}"
    }),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# Explanation
# =========================================================
st.markdown("---")

with st.expander("ℹ️ K-Means ทำงานอย่างไร?"):

    st.markdown("""
### K-Means Clustering

K-Means เป็น Machine Learning แบบ **Unsupervised Learning**
ที่ใช้สำหรับแบ่งข้อมูลออกเป็นกลุ่มตามความคล้ายคลึงกัน

ในระบบนี้ใช้ตัวแปร 2 ตัว ได้แก่

- **ปริมาณขยะที่เกิดขึ้น (ตัน/วัน)**
- **ปริมาณขยะที่นำกลับมาใช้ประโยชน์ (ตัน/วัน)**

ขั้นตอนการทำงาน:

**1. เตรียมข้อมูล**  
เลือกเฉพาะจังหวัดที่มีข้อมูลครบถ้วน

**2. Standardization**  
ปรับ Scale ของข้อมูลให้เหมาะสมก่อนนำไปทำ Clustering

**3. กำหนดจำนวนกลุ่ม (K)**  
ผู้ใช้สามารถเลือกจำนวน Cluster ได้

**4. K-Means**  
โมเดลจะจัดจังหวัดที่มีลักษณะใกล้เคียงกันให้อยู่ในกลุ่มเดียวกัน

**5. วิเคราะห์ผลลัพธ์**  
แสดงผลผ่าน Scatter Plot, ตาราง และจำนวนจังหวัดในแต่ละกลุ่ม
""")


# =========================================================
# Footer
# =========================================================
st.markdown("---")

st.caption(
    "🇹🇭 Thai MSW Analytics | Machine Learning Module"
)