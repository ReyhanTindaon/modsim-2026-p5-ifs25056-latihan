import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ===============================
# CONFIG & THEME
# ===============================
st.set_page_config(page_title="FITE Construction Dashboard", page_icon="🏗️", layout="wide")

# Custom CSS agar tampilan modern
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    
    [data-testid="stMetricValue"] { font-size: 28px; color: #FF4B4B; }
    [data-testid="stMetric"] { 
        background-color: white; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
        border: 1px solid #f0f2f6; 
    }

    div.stButton > button:first-child { 
        background: linear-gradient(to right, #FF4B4B, #FF7676); 
        color: white; 
        border: none; 
        padding: 15px 20px; 
        border-radius: 10px; 
        font-weight: bold; 
        transition: 0.3s; 
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3); 
        width: 100%; 
    }
    div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255, 75, 75, 0.5); }
    </style>
    """, unsafe_allow_html=True)

# ===============================
# SIDEBAR (PROFIL & KONFIGURASI)
# ===============================
with st.sidebar:
    # --- Identitas Pemilik ---
    st.image("https://github.com/ReyhanTindaon.png", width=100) # Otomatis ambil foto GitHub kamu
    st.title("Reyhan Tindaon")
    st.markdown("""
        <div style="margin-top: -15px; margin-bottom: 20px;">
            <a href="https://github.com/ReyhanTindaon" target="_blank" style="text-decoration: none; color: #FF4B4B; font-weight: bold;">
                🔗 github.com/ReyhanTindaon
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("⚙️ Simulation Settings")
    jumlah_simulasi = st.select_slider("Jumlah Iterasi:", options=[1000, 5000, 10000, 20000, 50000], value=20000)
    
    st.markdown("---")
    st.subheader("📋 Project Stages (Bulan)")
    
    tahapan = [
        "Perencanaan & Desain Lab", "Pekerjaan Struktur (5 Lantai)", 
        "Material Teknis Khusus", "Instalasi MEP & Listrik", 
        "Finishing & Setting Lab", "Pengujian & Sertifikasi"
    ]
    
    default_vals = {
        "Perencanaan & Desain Lab": [2, 3, 5],
        "Pekerjaan Struktur (5 Lantai)": [8, 10, 15],
        "Material Teknis Khusus": [3, 4, 8],
        "Instalasi MEP & Listrik": [4, 5, 7],
        "Finishing & Setting Lab": [3, 4, 6],
        "Pengujian & Sertifikasi": [1, 2, 3]
    }

    user_inputs = {}
    for tahap in tahapan:
        with st.expander(f"📍 {tahap}"):
            d = default_vals.get(tahap, [1, 2, 3])
            c1, c2, c3 = st.columns(3)
            opt = c1.number_input("Optimistic", value=d[0], key=f"o_{tahap}")
            ml = c2.number_input("Most Likely", value=d[1], key=f"m_{tahap}")
            pes = c3.number_input("Pessimistic", value=d[2], key=f"p_{tahap}")
            user_inputs[tahap] = [opt, ml, pes]

    st.markdown("###")
    run_sim = st.button("🚀 JALANKAN SIMULASI")

# ===============================
# MAIN DASHBOARD
# ===============================
st.markdown("""
    <div style="background-color:#1E1E1E; padding:30px; border-radius:20px; margin-bottom:30px; text-align:center">
        <h1 style="color:white; margin:0;">🏗️ Gedung FITE Simulation</h1>
        <p style="color:#BBBBBB; font-size:1.1em;">Optimized Project Intelligence Dashboard v3.0</p>
    </div>
    """, unsafe_allow_html=True)

if run_sim:
    # --- PROSES SIMULASI ---
    df_input = pd.DataFrame.from_dict(user_inputs, orient='index', columns=["Opt", "Norm", "Pes"]).reset_index()
    
    opt_arr = df_input["Opt"].values
    norm_arr = df_input["Norm"].values
    pes_arr = df_input["Pes"].values
    
    sim_matrix = np.random.triangular(left=opt_arr, mode=norm_arr, right=pes_arr, size=(jumlah_simulasi, len(tahapan)))
    hasil = sim_matrix.sum(axis=1)

    # --- ROW 1: METRICS ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rata-rata Waktu", f"{hasil.mean():.1f} Bln")
    m2.metric("Resiko (Std Dev)", f"{hasil.std():.2f}")
    m3.metric("Tercepat (Min)", f"{hasil.min():.1f} Bln")
    m4.metric("Terlama (Max)", f"{hasil.max():.1f} Bln")

    st.markdown("###")

    # --- ROW 2: TABS ---
    t1, t2 = st.tabs(["📈 Analisis Probabilitas (Kurva S)", "⚠️ Analisis Jalur Kritis (Tornado Chart)"])

    with t1:
        c_left, c_right = st.columns([2, 1])
        with c_left:
            sorted_hasil = np.sort(hasil)
            probs = np.arange(1, jumlah_simulasi + 1) / jumlah_simulasi
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=sorted_hasil, y=probs, mode='lines', 
                                    line=dict(color='#FF4B4B', width=3), 
                                    fill='tozeroy', fillcolor='rgba(255, 75, 75, 0.1)',
                                    name='Probabilitas Kumulatif'))
            
            fig.update_layout(title="Kurva S: Probabilitas Akumulasi Penyelesaian",
                             xaxis_title="Total Bulan", yaxis_title="Peluang (%)",
                             yaxis_tickformat='.0%', template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            
        with c_right:
            st.markdown("#### Skenario Deadline")
            targets = [16, 20, 24, 28]
            for t in targets:
                p = np.mean(hasil <= t) * 100
                st.write(f"**Target {t} Bulan:**")
                color = 'green' if p >= 70 else 'orange' if p >= 30 else 'red'
                st.markdown(f"""
                    <div style="background-color: #f0f2f6; border-radius: 5px; height: 12px; margin-bottom: 5px;">
                        <div style="background-color: {color}; height: 12px; width: {p}%; border-radius: 5px;"></div>
                    </div>
                """, unsafe_allow_html=True)
                st.write(f"{p:.1f}%")

    with t2:
        risk_vals = np.std(sim_matrix, axis=0)
        df_risk = pd.DataFrame({"Tahap": tahapan, "Risk": risk_vals}).sort_values("Risk", ascending=True)
        
        # Tornado Chart yang sudah diperbaiki (Anti-Error)
        fig_tornado = px.bar(df_risk, x="Risk", y="Tahap", orientation='h',
                             title="Tornado Chart: Tahapan Paling Kritis",
                             color="Risk", color_continuous_scale="Reds",
                             template="plotly_white")
        
        fig_tornado.update_layout(showlegend=False, coloraxis_showscale=False, bargap=0.4)
        st.plotly_chart(fig_tornado, use_container_width=True)
        st.warning("Semakin merah dan panjang bar, semakin besar pengaruh tahap tersebut pada ketidakpastian durasi proyek.")

else:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Studi Kasus Gedung FITE")
        st.write("Gedung 5 lantai dengan fasilitas lab khusus VR/AR dan Game. Simulasi ini membantu memprediksi waktu penyelesaian di tengah ketidakpastian.")
    with col_b:
        st.subheader("Instruksi")
        st.write("Silakan atur durasi pengerjaan di panel kiri dan tekan tombol JALANKAN SIMULASI.")