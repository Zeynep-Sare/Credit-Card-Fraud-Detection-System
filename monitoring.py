import streamlit as st
import plotly.express as px
import pandas as pd
import database as db


def show_dashboard():
    st.header("📊 Sistem İzleme Raporu")

    # İstatistikleri veritabanından çek
    stats = db.calculate_metrics()

    # 1. KPI Kartları
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Toplam İşlem", f"{stats['total']:,}")
    with col2:
        st.metric("Fraud Tespit", f"{stats['fraud']:,}")
    with col3:
        rate = (stats['fraud'] / stats['total'] * 100) if stats['total'] > 0 else 0
        st.metric("Fraud Oranı", f"%{rate:.2f}")
    with col4:
        st.metric("Ort. Risk Skoru", f"%{stats['avg_risk'] * 100:.1f}")

    st.markdown("---")

    # 2. Grafikler
    if stats['total'] > 0:
        df = db.get_history_df()

        # Tarih formatı düzeltme
        df['islem_zamani'] = pd.to_datetime(df['islem_zamani'])
        df['date'] = df['islem_zamani'].dt.date

        # Grafik 1: Günlük Fraud
        st.subheader("📈 Günlük Fraud Trendi")
        fraud_by_date = df[df['prediction'] == 1].groupby('date').size().reset_index(name='count')

        if len(fraud_by_date) > 0:
            fig1 = px.bar(fraud_by_date, x='date', y='count',
                          title='Günlük Yakalanan Fraud Sayısı',
                          color_discrete_sequence=['#FF4B4B'])
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("Henüz hiç Fraud yakalanmadı.")

        # Grafik 2 & 3
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.subheader("💰 Tutar Dağılımı")
            fig2 = px.histogram(df, x='amount', color='prediction',
                                labels={'prediction': 'Durum'},
                                color_discrete_map={0: '#00CC96', 1: '#FF4B4B'},
                                title="Tutar Analizi")
            st.plotly_chart(fig2, use_container_width=True)

        with col_g2:
            st.subheader("🕐 Saatlik Dağılım")
            fig3 = px.histogram(df, x='hour', color='prediction',
                                labels={'prediction': 'Durum'},
                                color_discrete_map={0: '#00CC96', 1: '#FF4B4B'},
                                title="Saat Analizi")
            st.plotly_chart(fig3, use_container_width=True)

        # 3. Tablo
        st.subheader("📋 Son İşlem Kayıtları")
        recent = df.head(10)[['islem_zamani', 'amount', 'hour', 'prediction', 'probability']]
        recent['prediction'] = recent['prediction'].map({0: '✅ Temiz', 1: '🚨 Fraud'})
        recent['probability'] = recent['probability'].apply(lambda x: f"%{x * 100:.2f}")
        st.dataframe(recent, use_container_width=True)

    else:
        st.warning("Veri yok. Simülasyon sekmesinden işlem yapın.")

    # Yenile Butonu
    if st.button("🔄 Verileri Yenile"):
        st.cache_data.clear()