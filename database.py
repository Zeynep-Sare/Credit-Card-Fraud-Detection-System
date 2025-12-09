import sqlite3
import pandas as pd
from datetime import datetime

# Veritabanı dosya ismimiz
DB_NAME = 'fraud_project.db'


# 1. Veritabanı Bağlantısı ve Tablo Oluşturma
# Eğer dosya yoksa oluşturur, varsa bağlanır.
def create_fraud_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        # Tabloyu oluşturuyoruz: ID, zaman, tutar ve tahmin sonuçlarını tutacak
        c.execute('''
                  CREATE TABLE IF NOT EXISTS predictions
                  (
                      id
                      INTEGER
                      PRIMARY
                      KEY
                      AUTOINCREMENT,
                      islem_zamani
                      TEXT,
                      amount
                      REAL,
                      hour
                      INTEGER,
                      is_night
                      INTEGER,
                      prediction
                      INTEGER,
                      probability
                      REAL
                  )
                  ''')
        conn.commit()
        conn.close()
        # print("Veritabanı bağlantısı başarılı.")
    except Exception as e:
        print(f"Veritabanı oluşturulurken hata çıktı: {e}")


# 2. Tahmin Sonucunu Kaydetme Fonksiyonu
def add_prediction_to_db(amount, hour, is_night, pred, prob):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute('''
              INSERT INTO predictions (islem_zamani, amount, hour, is_night, prediction, probability)
              VALUES (?, ?, ?, ?, ?, ?)
              ''', (current_time, amount, hour, is_night, int(pred), prob))

    conn.commit()
    conn.close()


# 3. Geçmiş Verileri Çekme (Tablo için)
def get_history_df():
    conn = sqlite3.connect(DB_NAME)
    # Pandas ile direkt SQL sorgusu atıp dataframe'e çeviriyoruz
    # En son eklenen veriyi en üstte görmek için ORDER BY id DESC yaptık
    try:
        df = pd.read_sql("SELECT * FROM predictions ORDER BY id DESC", conn)
    except:
        df = pd.DataFrame()
    conn.close()
    return df


# 4. Dashboard İstatistikleri Hesaplama
def calculate_metrics():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        c.execute("SELECT COUNT(*) FROM predictions")
        total_count = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM predictions WHERE prediction = 1")
        fraud_count = c.fetchone()[0]

        c.execute("SELECT AVG(probability) FROM predictions")
        avg_risk_score = c.fetchone()[0]

        if avg_risk_score is None:
            avg_risk_score = 0

    except:
        total_count = 0
        fraud_count = 0
        avg_risk_score = 0

    conn.close()

    return {
        'total': total_count,
        'fraud': fraud_count,
        'avg_risk': avg_risk_score
    }

    # database.py dosyasının EN ALTINA bunu ekle:

def clear_all_data():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM predictions")  # Tabloyu boşalt
        conn.commit()
        conn.close()


