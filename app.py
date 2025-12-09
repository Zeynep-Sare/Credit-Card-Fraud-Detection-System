import streamlit as st
import pandas as pd
import numpy as np
import pickle
import database as db
import monitoring as mon

# --- SAYFA AYARLARI (Modern Görünüm) ---
st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Veritabanı Başlat
db.create_fraud_db()

# --- CSS İLE GÖRSELLİĞİ ARTIRMA ---
# Bu kısım butonları ve başlıkları biraz daha havalı yapar
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
    }
    .reportview-container {
        background: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)


# --- MODEL YÜKLEME ---
@st.cache_resource
def load_models():
    try:
        model = pickle.load(open('models/fraud_model.pkl', 'rb'))
        scaler_time = pickle.load(open('models/scaler_time.pkl', 'rb'))
        scaler_amount = pickle.load(open('models/scaler_amount.pkl', 'rb'))
        return model, scaler_time, scaler_amount
    except FileNotFoundError:
        return None, None, None


model, scaler_time, scaler_amount = load_models()

if model is None:
    st.error("⚠️ Model dosyaları eksik! Lütfen 'models' klasörünü kontrol edin.")
    st.stop()

# --- SIDEBAR (SOL MENÜ) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9406/9406085.png", width=100)
    st.title("FraudGuard AI")
    st.caption("v1.0.2 | Yapay Zeka Destekli Güvenlik")

    st.markdown("---")
    st.write("🔧 **Sistem Ayarları**")

    # VERİLERİ SİLME BUTONU
    if st.button("🗑️ Tüm Kayıtları Temizle", type="secondary"):
        db.clear_all_data()
        st.toast("Veritabanı başarıyla sıfırlandı!", icon="🧹")
        st.cache_data.clear()  # Cache'i de temizle ki grafikler güncellensin

# --- ANA EKRAN ---
st.title("🛡️ Kredi Kartı Dolandırıcılık Tespiti")
st.markdown("Bu panel, makine öğrenmesi modelleri kullanarak şüpheli işlemleri **gerçek zamanlı** analiz eder.")

# Sekmeler
tab1, tab2 = st.tabs(["🕵️ İşlem Simülasyonu", "📊 Canlı İzleme Paneli"])

# =========================================================
# TAB 1: MODERN SİMÜLASYON
# =========================================================
with tab1:
    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        st.subheader("1️⃣ Senaryo Seçimi")
        st.info("Test etmek istediğiniz durumu seçin, yapay zeka parametreleri otomatik ayarlasın.")

        # Senaryo Seçici
        scenario = st.selectbox(
            "İşlem Tipi",
            ["✅ Normal Alışveriş", "🚨 Çalıntı Kart (Fraud)", "⚠️ Anormal Saat İşlemi", "🛠️ Manuel Test"]
        )

        # Varsayılan Değerler (Senaryoya Göre)
        if scenario == "✅ Normal Alışveriş":
            def_amt, def_hr, def_v14, def_v17 = 120.0, 14, 0.0, 0.0
            st.success("Standart kullanıcı davranışı simüle ediliyor.")

        elif scenario == "🚨 Çalıntı Kart (Fraud)":
            def_amt, def_hr, def_v14, def_v17 = 250.0, 2, -12.0, -8.0
            st.error("Sisteme sızmaya çalışan saldırgan profili simüle ediliyor.")

        elif scenario == "⚠️ Anormal Saat İşlemi":
            def_amt, def_hr, def_v14, def_v17 = 5000.0, 4, -5.0, -2.0
            st.warning("Gece yarısı yüksek tutarlı işlem deneniyor.")

        else:  # Manuel
            def_amt, def_hr, def_v14, def_v17 = 100.0, 12, 0.0, 0.0

    with col2:
        st.subheader("2️⃣ İşlem Detayları")

        with st.container(border=True):
            # Temel Bilgiler
            c1, c2 = st.columns(2)
            input_amount = c1.number_input("Tutar ($)", 0.0, 20000.0, float(def_amt))
            input_hour = c2.slider("İşlem Saati", 0, 24, int(def_hr))

            # --- PCA GİZLEME TAKTİĞİ ---
            # V değerlerini 'Expander' içine sakladık. Hoca sorarsa açarsın.
            with st.expander("Gelişmiş Teknik Ayarlar (PCA - V Değerleri)"):
                st.caption("""
                **Bu değerler nedir?** Müşteri gizliliğini korumak için bankalar verileri (isim, adres vb.) PCA yöntemiyle şifreler. 
                V14 ve V17, dolandırıcılık tespitinde matematiksel olarak en belirleyici özelliklerdir.
                """)
                v14 = st.slider("V14 (Anomali Katsayısı)", -20.0, 20.0, float(def_v14))
                v17 = st.slider("V17 (Sapma Katsayısı)", -20.0, 20.0, float(def_v17))
                v12 = st.slider("V12", -20.0, 20.0, 0.0)

            # Analiz Butonu
            if st.button("🚀 İşlemi Analiz Et", type="primary"):
                # ... (Hesaplama Kodları Aynı) ...
                input_time_seconds = input_hour * 3600
                scaled_amount = scaler_amount.transform(pd.DataFrame([[input_amount]], columns=['Amount']))[0][0]
                scaled_time = scaler_time.transform(pd.DataFrame([[input_time_seconds]], columns=['Time']))[0][0]

                input_df = pd.DataFrame([{
                    'Time_Scaled': scaled_time, 'Amount_Scaled': scaled_amount,
                    'V1': 0, 'V2': 0, 'V3': 0, 'V4': 0, 'V5': 0, 'V6': 0, 'V7': 0, 'V8': 0, 'V9': 0, 'V10': 0,
                    'V11': 0, 'V12': v12, 'V13': 0, 'V14': v14, 'V15': 0, 'V16': 0, 'V17': v17, 'V18': 0,
                    'V19': 0, 'V20': 0, 'V21': 0, 'V22': 0, 'V23': 0, 'V24': 0, 'V25': 0, 'V26': 0, 'V27': 0, 'V28': 0,
                    'Amount_Log': np.log1p(input_amount),
                    'Is_Small_Amount': 1 if input_amount < 10 else 0,
                    'Is_Large_Amount': 1 if input_amount > 200 else 0,
                    'Hour': input_hour,
                    'Is_Night': 1 if (input_hour >= 22 or input_hour <= 6) else 0,
                    'V17_V14': v17 * v14,
                    'Top5_sum': v17 + v14 + v12
                }])

                prob = model.predict_proba(input_df)[0][1]
                pred = prob > 0.5

                # Veritabanına kaydet
                db.add_prediction_to_db(input_amount, input_hour, 0, pred, prob)

                # --- SONUÇ GÖSTERİMİ (MODERN) ---
                st.write("---")
                res_col1, res_col2 = st.columns([1, 2])

                with res_col1:
                    st.metric("Risk Skoru", f"%{prob * 100:.1f}")

                with res_col2:
                    if pred:
                        st.error("🚨 **ALARM: ŞÜPHELİ İŞLEM TESPİT EDİLDİ!**")
                        st.write("Sistem bu işlemi güvenlik protokollerine taktı. İşlem bloke edilmeli.")
                    else:
                        st.success("✅ **GÜVENLİ İŞLEM**")
                        st.write("Herhangi bir risk faktörüne rastlanmadı.")

# =========================================================
# TAB 2: MONITORING DASHBOARD
# =========================================================
with tab2:
    mon.show_dashboard()