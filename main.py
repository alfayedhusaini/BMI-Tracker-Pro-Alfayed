import streamlit as st
import base64
import os
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime

st.set_page_config(page_title="BMI Tracker Pro", layout="wide")

if "riwayat_data" not in st.session_state:
    st.session_state.riwayat_data = []

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

jarum_base64 = get_base64("jarum.png")
bg_header_base64 = get_base64("gambar.jpg")

header_style = f"""
<style>
    .header-container {{
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("data:image/jpg;base64,{bg_header_base64}");
        background-size: cover;
        background-position: center;
        padding: 60px 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }}
    .container-visual {{
        position: relative; width: 100%; height: 250px; margin-top: 30px;
    }}
    .bmi-bar-background {{
        position: absolute; bottom: -25px; left: 0; width: 100%; height: 20px;
        background: linear-gradient(to right, #3498db 0%, #3498db 28%, #2ecc71 28%, #2ecc71 50%, #f1c40f 50%, #f1c40f 66%, #e74c3c 66%, #e74c3c 100%);
        border-radius: 10px;
    }}
    .jarum-pointer {{
        position: absolute; bottom: -150px; width: 400px; height: 500px;
        background-image: url('data:image/png;base64,{jarum_base64}');
        background-size: contain; background-repeat: no-repeat; background-position: bottom center;
        transition: left 1s ease-in-out; transform: rotate(70deg);
        border: none !important; outline: none !important; box-shadow: none !important; background-color: transparent !important;
    }}
</style>
"""
st.markdown(header_style, unsafe_allow_html=True)

def get_bmi_details(bmi):
    if bmi < 18.5:
        return "Kurus", "#3498db", "💡 Tambah asupan protein & kalori."
    elif bmi < 25:
        return "Normal", "#2ecc71", "🎉 Pertahankan pola hidup sehat!"
    elif bmi < 30:
        return "Gemuk", "#f1c40f", "⚠️ Kurangi gula & rutin olahraga."
    else:
        return "Obesitas", "#e74c3c", "🚑 Konsultasi dokter & diet ketat."

def main():
    st.markdown(f"""
        <div class="header-container">
            <h1 style="margin:0;">BMI & IDEAL WEIGHT TRACKER</h1>
            <p style="font-size:1.2rem; opacity:0.9;">Pantau kesehatan tubuh Anda dengan mudah</p>
        </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Hitung BMI", "Riwayat", "Informasi"],
        icons=["calculator", "clock-history", "info-circle"],
        orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#EF5E1B"}, "container": {"margin-bottom": "25px"}}
    )
    
    if selected == "Hitung BMI":
        st.subheader("📊 Input Data Tubuh")
        with st.form("bmi_form"):
            nama = st.text_input("Nama")
            jk = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"], horizontal=True)
            c1, c2 = st.columns(2)
            tinggi = c1.number_input("Tinggi (cm)", value=170.0)
            berat = c2.number_input("Berat (kg)", value=65.0)
            submit = st.form_submit_button("Hitung & Simpan")
            
        if submit and nama:
            bmi = round(berat / ((tinggi/100)**2), 2)
            kategori, warna, saran = get_bmi_details(bmi)
            bb_ideal = round((tinggi - 100) - ((tinggi - 100) * (0.1 if jk == "Laki-laki" else 0.15)), 1)
            posisi = max(0, min(100, (bmi - 10) / (40 - 10) * 100))
            
            st.markdown(f"""
                <div class="container-visual">
                    <div class="jarum-pointer" style="left: calc({posisi}% - 60px);"></div>
                    <div class="bmi-bar-background"></div>
                </div>
                <h2 style='text-align:center; color:{warna}; margin-top:20px;'>{kategori}</h2>
            """, unsafe_allow_html=True)
            
            st.success(f"BMI: {bmi} | Berat Ideal: {bb_ideal} kg")
            st.info(saran)
            
            st.session_state.riwayat_data.insert(0, {
                "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Nama": nama,
                "Jenis Kelamin": jk,
                "Tinggi (cm)": tinggi,
                "Berat (kg)": berat,
                "BMI": bmi,
                "Kategori": kategori,
                "Berat Ideal (kg)": bb_ideal
            })
            
    elif selected == "Riwayat":
        st.subheader("📁 Data Tersimpan")
        if st.session_state.riwayat_data:
            df = pd.DataFrame(st.session_state.riwayat_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Belum ada data.")
            
    elif selected == "Informasi":
        st.subheader("ℹ️ Informasi Kesehatan")
        st.markdown("""
        Aplikasi ini dirancang untuk memantau perkembangan fisik berdasarkan standar internasional:
        1. *BMI (Body Mass Index):* Menggunakan rumus World Health Organization:  
            $BMI = \\frac{Berat\,Badan\,(kg)}{Tinggi\,(m)^2}$  
        2. *Berat Badan Ideal:* Berdasarkan standar Asia-Pasifik, angka BMI 22.0 dianggap sebagai titik tengah risiko kesehatan terendah.  
            Rumus: $Ideal = 22.0 \\times Tinggi(m)^2$
        3. *Sistem record:* Analisis data akan masuk ke dalam penyimpanan sementara aplikasi secara real-time.
        """)

if __name__ == "__main__":
    main()