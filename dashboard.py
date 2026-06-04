import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="EcoScan Dashboard",
    page_icon="♻️",
    layout="wide"
)



st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f4fbf6 0%, #eaf7ee 100%);
}

section[data-testid="stSidebar"] {
    background-color: #f7faf8;
}

.hero {
    background: linear-gradient(90deg, #1b5e20, #43a047);
    padding: 28px;
    border-radius: 22px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 6px;
}

.hero p {
    font-size: 17px;
    margin: 0;
    opacity: 0.95;
}

.metric-card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 5px 16px rgba(0,0,0,0.08);
    text-align: center;
    min-height: 115px;
}

.metric-title {
    color: #5f7d64;
    font-size: 14px;
    margin-bottom: 8px;
}

.metric-value {
    color: #1b5e20;
    font-size: 28px;
    font-weight: 800;
}

.metric-note {
    color: #78909c;
    font-size: 13px;
    margin-top: 4px;
}

.chart-card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 5px 16px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.insight-box {
    background-color: #e8f5e9;
    border-left: 6px solid #2e7d32;
    padding: 18px 20px;
    border-radius: 14px;
    color: #1b5e20;
    font-size: 15px;
    line-height: 1.7;
    margin-top: 18px;
}

.small-caption {
    color: #6b7c6f;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)



class_data = pd.DataFrame({
    "Kategori": ["Organik", "Plastik", "Kertas", "Kaca", "Logam", "Others", "Residu"],
    "Jumlah": [3557, 3169, 3152, 2901, 2632, 2171, 1085],
})


class_data["Persentase"] = (class_data["Jumlah"] / class_data["Jumlah"].sum() * 100).round(2).astype(str) + "%"

three_r_data = pd.DataFrame({
    "3R": ["Recycle", "Reuse", "Reduce"],
    "Jumlah": [13864, 2171, 2632],
    "Persentase": [74.30, 11.60, 14.10]
})

status_data = pd.DataFrame({
    "Status": ["Dapat Dimanfaatkan", "Residu"],
    "Jumlah": [16035, 2632],
    "Persentase": [85.90, 14.10]
})

status_data["Persentase"] = status_data["Persentase"].astype(str) + "%"


def metric_card(title, value, note=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def insight(text):
    st.markdown(
        f"""
        <div class="insight-box">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )

def bar_chart(data, title):
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    colors = ["#2E7D32", "#43A047", "#66BB6A", "#81C784", "#A5D6A7", "#C8E6C9", "#9E9E9E"]

    ax.bar(data["Kategori"], data["Jumlah"], color=colors[:len(data)])
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_xlabel("Kategori", fontsize=10)
    ax.set_ylabel("Jumlah", fontsize=10)
    ax.tick_params(axis="x", labelrotation=25, labelsize=9)
    ax.tick_params(axis="y", labelsize=9)
    ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

def pie_chart(data, label_col, value_col, title):
    fig, ax = plt.subplots(figsize=(4.4, 4.4))
    colors = ["#2E7D32", "#81C784", "#F9A825"]

    ax.pie(
        data[value_col],
        labels=data[label_col],
        autopct="%1.1f%%",
        startangle=90,
        colors=colors[:len(data)],
        textprops={"fontsize": 9}
    )
    ax.set_title(title, fontsize=12, fontweight="bold")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)



st.sidebar.title("♻️ EcoScan")
st.sidebar.caption("Waste Insight Dashboard")

menu = st.sidebar.radio(
    "Pilih Analisis",
    [
        "Overview",
        "Pertanyaan 1: Distribusi & 3R",
        "Pertanyaan 2: Kategori Dominan",
        "Pertanyaan 3: Sustainability"
    ]
)



st.markdown("""
<div class="hero">
    <h1>♻️ EcoScan Dashboard</h1>
    <p>Analisis kategori sampah, potensi 3R, dan dampak sustainability berdasarkan dataset EcoScan.</p>
</div>
""", unsafe_allow_html=True)



if menu == "Overview":
    st.header("🌱 Ringkasan Utama")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Total Data", "18.667", "Gambar")
    with c2:
        metric_card("Kategori Dominan", "Organik", "19.06%")
    with c3:
        metric_card("Dapat Dimanfaatkan", "85.90%", "Reuse/Recycle")
    with c4:
        metric_card("Residu", "14.10%", "Sulit Diolah")

    st.write("")
    col1, col2 = st.columns([1.15, 0.85])

    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("📊 Distribusi Kategori Sampah")
        bar_chart(class_data, "Jumlah Data per Kategori")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("📋 Ringkasan Data")
        st.dataframe(
            class_data[["Kategori", "Jumlah", "Persentase"]],
            hide_index=True,
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    insight(
        "Mayoritas sampah dalam dataset EcoScan masih memiliki potensi untuk dimanfaatkan kembali. "
        "Hal ini menunjukkan bahwa EcoScan dapat membantu proses identifikasi sampah dan mendukung "
        "pengelolaan sampah berbasis data."
    )



elif menu == "Pertanyaan 1: Distribusi & 3R":
    st.write("Berapa persentase tiap kategori sampah serta proporsi reuse, reduce, dan recycle berdasarkan hasil klasifikasi EcoScan?")

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("♻️ Recycle", "74.30%", "13.864 Data")
    with c2:
        metric_card("🔁 Reuse", "11.60%", "2.171 Data")
    with c3:
        metric_card("⚠️ Reduce", "14.10%", "2.632 Data")

    st.write("")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("📊 Distribusi Kategori")
        bar_chart(class_data, "Distribusi Kategori Sampah")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("🍃 Proporsi 3R")
        pie_chart(three_r_data, "3R", "Jumlah", "Reuse, Reduce, dan Recycle")
        st.markdown("</div>", unsafe_allow_html=True)

    insight(
        "Recycle mendominasi sebesar 74.30%, diikuti Reuse sebesar 11.60% "
        "dan Reduce sebesar 14.10%. Artinya, sekitar 85.90% sampah dalam dataset "
        "EcoScan memiliki potensi untuk dimanfaatkan kembali melalui reuse dan recycle."
    )



elif menu == "Pertanyaan 2: Kategori Dominan":
    st.write("Kategori sampah apa yang paling dominan dan berapa proporsinya, serta bagaimana potensi pemanfaatannya untuk mengurangi volume sampah secara signifikan?")

    c1, c2 = st.columns(2)
    with c1:
        metric_card("🌿 Kategori Dominan", "Organik", "Kategori Tertinggi")
    with c2:
        metric_card("📌 Proporsi", "19.06%", "3.557 Data")

    st.write("")
    col1, col2 = st.columns([1.2, 0.8])

    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("📊 Distribusi Kategori Sampah")
        bar_chart(class_data, "Kategori Sampah Berdasarkan Jumlah Data")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("🌱 Rekomendasi Pengelolaan")
        st.markdown("""
        - Organik dapat diolah menjadi kompos.
        - Cocok untuk strategi pengurangan sampah rumah tangga.
        - Berpotensi mengurangi sampah menuju TPA.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    insight(
        "Kategori Organik menjadi kategori paling dominan dengan 3.557 data "
        "atau 19.06% dari total dataset. Sampah organik memiliki potensi tinggi untuk "
        "dimanfaatkan kembali melalui komposting, sehingga dapat menjadi prioritas utama "
        "dalam strategi pengurangan volume sampah."
    )



elif menu == "Pertanyaan 3: Sustainability":
    st.write("Seberapa besar persentase sampah yang dapat dimanfaatkan kembali dibandingkan dengan sampah residu, dan bagaimana hal ini menunjukkan potensi EcoScan dalam mendukung pengelolaan sampah berkelanjutan?")

    c1, c2 = st.columns(2)
    with c1:
        metric_card("✅ Dapat Dimanfaatkan", "85.90%", "16.035 Data")
    with c2:
        metric_card("🗑️ Residu", "14.10%", "2.632 Data")

    st.write("")
    col1, col2 = st.columns([0.9, 1.1])

    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("🍃 Proporsi Pemanfaatan")
        pie_chart(status_data, "Status", "Jumlah", "Pemanfaatan vs Residu")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("📋 Detail Status")
        st.dataframe(
            status_data[["Status", "Jumlah", "Persentase"]],
            hide_index=True,
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    insight(
        "Sebanyak 85.90% sampah dalam dataset EcoScan dapat dimanfaatkan kembali, "
        "sedangkan 14.10% termasuk residu. Hal ini menunjukkan bahwa mayoritas sampah "
        "masih memiliki nilai guna, sehingga EcoScan memiliki potensi kuat dalam mendukung "
        "pengelolaan sampah berkelanjutan."
    )

st.markdown("---")
st.caption("EcoScan Dashboard | Waste Classification & Sustainability Insight")
