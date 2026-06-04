import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import uuid
import random
from datetime import datetime
import math

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





# =========================
# A/B TESTING FUNCTION
# =========================

AB_LOG_FILE = "ab_testing_log.csv"


def init_ab_testing():
    if "user_id" not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())

    if "ab_variant" not in st.session_state:
        st.session_state.ab_variant = random.choice(["A", "B"])

    if "ab_view_logged" not in st.session_state:
        st.session_state.ab_view_logged = False


def log_ab_event(event_name):
    data = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": st.session_state.user_id,
        "variant": st.session_state.ab_variant,
        "event": event_name
    }])

    if os.path.exists(AB_LOG_FILE):
        data.to_csv(AB_LOG_FILE, mode="a", header=False, index=False)
    else:
        data.to_csv(AB_LOG_FILE, index=False)


def calculate_ab_result():
    if not os.path.exists(AB_LOG_FILE):
        return None

    df_ab = pd.read_csv(AB_LOG_FILE)

    views = df_ab[df_ab["event"] == "view_recommendation"].groupby("variant")["user_id"].nunique()
    clicks = df_ab[df_ab["event"] == "click_recommendation"].groupby("variant")["user_id"].nunique()

    result = pd.DataFrame({
        "Variant": ["A", "B"],
        "Views": [
            views.get("A", 0),
            views.get("B", 0)
        ],
        "Clicks": [
            clicks.get("A", 0),
            clicks.get("B", 0)
        ]
    })

    result["Conversion Rate"] = result.apply(
        lambda row: row["Clicks"] / row["Views"] if row["Views"] > 0 else 0,
        axis=1
    )

    result["Conversion Rate (%)"] = (result["Conversion Rate"] * 100).round(2)

    return result


def two_proportion_z_test(click_a, view_a, click_b, view_b):
    if view_a == 0 or view_b == 0:
        return None, None

    p_a = click_a / view_a
    p_b = click_b / view_b

    pooled_p = (click_a + click_b) / (view_a + view_b)

    standard_error = math.sqrt(
        pooled_p * (1 - pooled_p) * ((1 / view_a) + (1 / view_b))
    )

    if standard_error == 0:
        return None, None

    z_score = (p_b - p_a) / standard_error
    p_value = math.erfc(abs(z_score) / math.sqrt(2))

    return z_score, p_value

st.sidebar.title("♻️ EcoScan")
st.sidebar.caption("Waste Insight Dashboard")

menu = st.sidebar.radio(
    "Pilih Analisis",
    [
        "Overview",
        "Pertanyaan 1: Distribusi & 3R",
        "Pertanyaan 2: Kategori Dominan",
        "Pertanyaan 3: Sustainability",
        "A/B Testing"
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



elif menu == "A/B Testing":
    init_ab_testing()

    if not st.session_state.ab_view_logged:
        log_ab_event("view_recommendation")
        st.session_state.ab_view_logged = True

    st.header("🧪 A/B Testing Rekomendasi EcoScan")

    st.write(
        "A/B Testing ini digunakan untuk membandingkan efektivitas dua jenis rekomendasi "
        "pengelolaan sampah pada EcoScan. Variant A menampilkan rekomendasi umum, "
        "sedangkan Variant B menampilkan rekomendasi spesifik berdasarkan kategori sampah."
    )

    st.markdown("""
    <div class="insight-box">
        Pengujian dilakukan dengan mencatat jumlah pengguna yang melihat rekomendasi
        dan jumlah pengguna yang menekan tombol rekomendasi. Hasilnya dihitung menggunakan
        conversion rate.
    </div>
    """, unsafe_allow_html=True)

    st.info(f"Variant yang sedang ditampilkan: {st.session_state.ab_variant}")

    st.write("")

    if st.session_state.ab_variant == "A":
        st.subheader("Variant A: Rekomendasi Umum")

        st.markdown("""
        EcoScan memberikan rekomendasi umum agar pengguna dapat memilah dan mengelola sampah
        berdasarkan prinsip reuse, reduce, dan recycle.
        """)

        st.markdown("""
        <div class="chart-card">
            <h4>Rekomendasi Umum</h4>
            <p>
                Pisahkan sampah berdasarkan jenisnya, kurangi penggunaan sampah yang sulit diolah,
                dan manfaatkan kembali sampah yang masih memiliki nilai guna.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Lihat Rekomendasi Pengelolaan"):
            log_ab_event("click_recommendation")

            st.success("Rekomendasi berhasil dibuka.")

            st.markdown("""
            ### Rekomendasi Pengelolaan Sampah

            - Pisahkan sampah organik dan anorganik.
            - Gunakan kembali sampah yang masih layak dimanfaatkan.
            - Daur ulang sampah seperti plastik, kertas, logam, dan kaca.
            - Kurangi penggunaan sampah yang sulit diolah.
            """)

    elif st.session_state.ab_variant == "B":
        st.subheader("Variant B: Rekomendasi Spesifik Berdasarkan Kategori")

        st.markdown("""
        EcoScan memberikan rekomendasi yang lebih spesifik berdasarkan kategori sampah,
        sehingga pengguna dapat memahami tindakan pengelolaan yang lebih tepat.
        """)

        st.markdown("""
        <div class="chart-card">
            <h4>Rekomendasi Spesifik</h4>
            <p>
                Setiap kategori sampah memiliki cara pengelolaan yang berbeda.
                Rekomendasi spesifik membantu pengguna mengambil keputusan yang lebih tepat.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Lihat Rekomendasi Berdasarkan Kategori"):
            log_ab_event("click_recommendation")

            st.success("Rekomendasi berhasil dibuka.")

            st.markdown("""
            ### Rekomendasi Pengelolaan Berdasarkan Kategori

            - **Organik:** dapat diolah menjadi kompos atau pupuk organik.
            - **Plastik:** dapat dipilah dan dikirim ke fasilitas daur ulang.
            - **Kertas:** dapat digunakan kembali atau didaur ulang.
            - **Kaca:** dapat digunakan ulang atau dikumpulkan untuk proses recycle.
            - **Logam:** dapat dikumpulkan dan didaur ulang menjadi bahan baru.
            - **Others:** perlu dikurangi penggunaannya apabila sulit diklasifikasikan.
            - **Residu:** sebaiknya diminimalkan karena sulit dimanfaatkan kembali.
            """)

    st.markdown("---")
    st.subheader("📊 Hasil Sementara A/B Testing")

    ab_result = calculate_ab_result()

    if ab_result is None:
        st.warning("Belum ada data A/B Testing yang tercatat.")
    else:
        st.dataframe(
            ab_result[["Variant", "Views", "Clicks", "Conversion Rate (%)"]],
            hide_index=True,
            use_container_width=True
        )

        variant_a = ab_result[ab_result["Variant"] == "A"].iloc[0]
        variant_b = ab_result[ab_result["Variant"] == "B"].iloc[0]

        z_score, p_value = two_proportion_z_test(
            variant_a["Clicks"],
            variant_a["Views"],
            variant_b["Clicks"],
            variant_b["Views"]
        )

        if z_score is not None and p_value is not None:
            st.write(f"**Z-score:** {z_score:.4f}")
            st.write(f"**P-value:** {p_value:.4f}")

            if p_value < 0.05:
                if variant_b["Conversion Rate"] > variant_a["Conversion Rate"]:
                    st.success("Variant B lebih efektif secara signifikan dibandingkan Variant A.")
                else:
                    st.success("Variant A lebih efektif secara signifikan dibandingkan Variant B.")
            else:
                st.warning("Belum terdapat perbedaan yang signifikan antara Variant A dan Variant B.")
        else:
            st.info("Data belum cukup untuk menghitung uji statistik.")

st.markdown("---")
st.caption("EcoScan Dashboard | Waste Classification & Sustainability Insight")
