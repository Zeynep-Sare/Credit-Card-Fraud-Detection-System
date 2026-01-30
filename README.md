# 💳 Credit Card Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange)
![License](https://img.shields.io/badge/License-MIT-green)

Merhaba! 👋 Ben **Zeynep**.
Bu repo, **Yapay Zeka Mühendisliği** eğitimim kapsamında geliştirdiğim, dengesiz veri setlerinde (imbalanced data) dolandırıcılık tespiti yapan uçtan uca bir makine öğrenmesi projesidir.

---

## 🎯 Proje Hakkında

Kredi kartı dolandırıcılığı, finansal güvenliğin en büyük tehditlerinden biridir. Ancak veri bilimi açısından burada büyük bir zorluk vardır: **"Samanlıkta İğne Aramak"**.

Elimizdeki 284,000 işlemden sadece 492 tanesi (%0.17) dolandırıcılık içeriyor. Bu projede, modelin "Her şey yolunda" diyerek %99 doğruluk alması tuzağına düşmeden, **gerçek suçluları yakalayan (High Recall)** akıllı bir sistem geliştirdim.

### 🌟 Özellikler
* **Etkileşimli Arayüz:** Streamlit ile geliştirilmiş, senaryo bazlı simülasyon ekranı.
* **Canlı İzleme (Monitoring):** SQLite veritabanı destekli, anlık fraud takibi yapan dashboard.
* **Özelleştirilmiş Feature Engineering:** Gece işlemleri ve PCA özelliklerinin etkileşimleri gibi yeni veriler türetildi.

---

## 📊 Veri Seti ve Zorluklar

* **Kaynak:** [Kaggle - Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
* **Boyut:** 284,807 İşlem
* **Dengesizlik:** %99.83 Normal vs %0.17 Fraud ⚠️
* **Veri Tipi:** Gizlilik nedeniyle V1-V28 olarak maskelenmiş PCA çıktıları, Zaman (Time) ve Tutar (Amount).

---

## 🛠️ Teknoloji Yığını

* **Dil:** Python
* **Veri Analizi:** Pandas, NumPy
* **Görselleştirme:** Plotly, Matplotlib, Seaborn
* **Model:** Logistic Regression (Class Weight Balanced)
* **Arayüz (Frontend):** Streamlit
* **Veritabanı:** SQLite

---

## 🚀 Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için adımları izleyin:

**1. Repoyu Klonlayın (veya indirin):**
```bash
git clone [https://github.com/kullaniciadin/fraud-detection-project.git](https://github.com/kullaniciadin/fraud-detection-project.git)
cd fraud-detection-project
```

**2. Gerekli Kütüphaneleri Yükleyin:**
```bash
pip install -r requirements.txt
```
**3. Uygulamayı Başlatın:**
```bash
streamlit run app.py
```
---
## 🧠 Model Geliştirme Süreci
### Bu projede sadece model.fit() yapıp geçmedim. Süreç şu şekilde işledi:

1. Keşifçi Veri Analizi (EDA)
Verinin dağılımını incelediğimde, dolandırıcılık işlemlerinin genelde düşük tutarlarda olduğunu ve günün belirli 
2. saatlerinde yoğunlaştığını fark ettim.

2. Feature Engineering (Sihirli Dokunuş ✨)
Modelin başarısını artıran en önemli adım burasıydı. 7 yeni özellik ürettim:

Is_Night: İşlem gece mi yapıldı? (Dolandırıcılar geceyi sever mi?)

V17_V14: En belirleyici iki özelliğin etkileşimi.

Amount_Log: Tutar verisinin logaritmik dönüşümü.

3. Model Başarımı
Farklı modeller denedim (LightGBM, Random Forest vb.) ancak Logistic Regression, hem açıklanabilirliği hem de
4. dengesiz veriyle başa çıkma yeteneği (Balanced Class Weight) sayesinde en iyi sonucu verdi.

Metrik	Değer	Açıklama
ROC-AUC	0.9750	Modelin genel ayrıştırma gücü.
Recall (Duyarlılık)	%91.8	Kritik Metrik: Her 100 dolandırıcıdan 92'sini yakalıyoruz.
Precision	%5.6	Yanlış alarmlarımız var ama bankacılıkta güvenlik önceliklidir.
---

---
## Neler Öğrendim?
### Bu proje bana şunları öğretti:

1. Recall vs Precision: Bir banka için dolandırıcıyı kaçırmanın maliyeti, müşteriye yanlışlıkla SMS atmaktan çok daha
büyüktür.
Bu yüzden Recall odaklı çalıştım.

2. Deployment: Bir modeli Jupyter Notebook'tan çıkarıp, insanların dokunabileceği bir ürüne (Streamlit App) dönüştürmek
farklı bir deneyimdi.

3. Veri Hikayeleştirme: V14, V17 gibi anlamsız sayıları kullanıcıya "Hacker Senaryosu" olarak sunarak teknik karmaşıklığı 
gizlemeyi öğrendim.

---

 

