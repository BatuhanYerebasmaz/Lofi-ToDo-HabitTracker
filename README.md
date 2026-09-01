# 📋 Görev & Alışkanlık Takip Programı (Lofi Habit Tracker)

Modern, estetik, oyunlaştırılmış ve yapay zeka destekli masaüstü görev ve alışkanlık takip uygulaması.

---

## ✨ Temel Özellikler

### 🎮 1. Oyunlaştırma, XP & Seviye Sistemi (Level Up)
* **⭐ Seviye & XP İlerleme Barı:** Başlığın yanında canlı seviye göstergesi ve dinamik XP çubuğu.
* **🌟 XP Kazanma Mekanikleri:**
  * Her tamamlanan standart görev: `+15 XP`
  * Sayaçlı görevler: Toplam 15 XP adım sayısına orantılı bölünür (`(adım * 15) // hedef`); her adımda payını verir ve hedefe ulaşıldığında kalanla birlikte tam `+15 XP` tamamlanır (Örn: 20 sayfalık kitapta 10. sayfada `7 XP`, 14. sayfada `10 XP`, bitişte tam `15 XP`).
  * Günlük %100 tamamlama: `+50 Bonus XP`
* **🏆 Seviye Skalası:**
  * **Lvl 1:** 🐣 Çaylak Başlangıç (0 - 49 XP)
  * **Lvl 2:** 🌿 Alışkanlık Tohumu (50 - 119 XP)
  * **Lvl 3:** ⚡ Odak Çırağı (120 - 199 XP)
  * **Lvl 4:** 🛡️ Disiplin Savaşçısı (200 - 299 XP)
  * **Lvl 5+:** 👑 Odak Efendisi (300+ XP)
* **🔥 Günlük Seri (Streak):** Düzenli tamamlanan ardışık gün sayısı takibi.
* **🛡️ Zincir Koruma Kalkanı (Streak Freeze):** Haftalık 1 kalkan hakkı ile 1 günlük aksamalarda veya ertesi sabah başlandığında serinizi kırmadan akıllı koruma.
* **🎉 Günün Zaferi Kutlaması:** Günlük tüm görevler (%100) bittiğinde özel zafer penceresi ve kutlama sesi.

---

### 🔢 2. Sayaçlı Alışkanlıklar (Counter Habits)
* **🎯 Sayısal Hedef Belirleme:** Ayarlar'dan görev eklerken isteğe bağlı hedef sayaç belirleme (Örn: *8 Bardak Su*, *20 Sayfa Kitap*, *100 Şınav*). `Enter` tuşuyla anında ekleme.
* **🖱️ Çift Yönlü Akıllı Tıklama:**
  * **Sol Tık:** Sayacı `+1` artırır (`0/8 ➔ 1/8 ➔ ... ➔ ✓8`).
  * **Sağ Tık:** Sayacı `-1` azaltır (`8/8 ➔ 7/8 ➔ ... ➔ 0/8`), normal görevlerde ise işareti kaldırır.

---

### 📊 3. Modern Lofi Dashboard & İstatistik Kartları
* **📊 Haftalık Trend (Bar Grafik):** Dolgun çubuklar, günün öne çıkarılması ve her çubuğun üzerinde tamamlanan görev sayı etiketleri (`4`, `8`, vb.).
* **🍩 Aylık Odak (Donut / Halka Grafik):** Ortasında büyük **`% Başarı Oranı`** ve `Tamamlanan/Toplam` görev sayısını gösteren modern donut grafik.
* **🏆 3 Mini İstatistik Kartı:**
  * **👑 En Uzun Seri:** Tüm zamanların en yüksek kesintisiz gün rekoru.
  * **⚡ Bu Ay Başarı:** Seçili ayda tamamlanan toplam görev ve başarı yüzdesi.
  * **🎯 En İstikrarlı:** Bu ay en çok tamamlanan favori alışkanlığınız.

---

### 📅 4. Aylık Takip Tablosu & Minimalist Gezinme
* **🎨 Pastel Aylık Matris Tablosu:** Ayın tüm günlerini (1-31) tek ekranda ultra-hızlı ve yumuşak pastel renklerle gösterir.
* **⚡ Günlük Moral & Efektiflik Takibi:** Her gün için 1-5 arası moral ve verimlilik puanlaması.
* **💊 Minimalist Ay Gezinme Kapsülü:** Tablonun hemen altındaki zarif kapsülle geçmiş ve gelecek ayların kayıtları arasında hızlıca gezinme; ay adına tıklandığında anında geçerli aya geri dönme.

---

### 🤖 5. Yapay Zeka Darlama & Hatırlatma Motoru
* **🧠 Yerel & Bulut LLM Desteği:**
  * **Google Gemini API (Ücretsiz):** Google AI Studio API anahtarıyla buluttan ışık hızında çalışan `Google Gemini 1.5 Flash (API Key Gerekli - Ücretsiz)` ve `Google Gemini 2.0 Flash (API Key Gerekli - Yeni)` modelleri.
  * **⚡ Canlı API Bağlantı Testi:** Ayarlar penceresinden `⚡ Test Et` butonuna basarak Google Gemini bağlantınızı anında doğrulama.
  * **Dahili Yerel Motor:** Harici hiçbir kurulum gerektirmeyen hazır çevrimdışı motor.
  * **Ollama & LM Studio:** Kendi bilgisayarınızdaki yerel açık kaynak modeller.
* **🎭 Farklı Kişilik Modları:** *Sert & Direkt*, *Alaycı & Esprili*, *Motivasyonel* ve *Özel Prompt*.
* **⏰ Akıllı Zamanlama:** Görevler için rastgele aralıklarla bağımsız bildirimler ve 30 saniyelik otomatik erteleme mekanizması.
* **⚠️ Otantik Windows Hata Penceresi:** Bildirimler 3 kez ertelendiğinde gerçek sistem hata diyalogu hissi veren dinamik arayüz.

---

### 📌 6. Kayan Mini Widget (Sticky Mode) & Global Kısayol
* **📌 Kayan Mini Görev Kartı (Always-on-Top):** Ekranın köşesinde her zaman üstte duran, kenar çizgisiz, yumuşak yuvarlak pastel kart tasarımı.
* **🔄 Karşılıklı Geçiş (Mutually Exclusive):**
  * Ana ekrandan `📌 Mini` butonuna basıldığında ana ekran otomatik gizlenir ve sadece mini widget ekranda kalır.
  * Mini widget üzerindeki `↗` butonuna basıldığında mini widget kapanır ve ana ekran geri gelir.
* **⌨️ Global Klavye Kısayolu (`Ctrl+Shift+T`):** Hangi uygulamada veya oyunda olursanız olun klavyeden `Ctrl+Shift+T` basarak ana ekran ile mini widget arasında anında geçiş yapma (%0 CPU).

---

### 🎨 7. Temalar & Lofi Ses Paketi
* **🎨 20 Estetik Tema:** 10 Pastel Aydınlık (Latte & Şeftali, Matcha Yeşili vb.) ve 10 Modern Karanlık (Karanlık Karbon, Gece Mavisi vb.) tema.
* **🎵 20 Farklı Mekanik & Lofi Ses Efekti:** 
  * Görev tamamlama, buton tıklama, bildirimler ve moral/efektiflik puanlama için **4 bağımsız ses kanalı**.
  * Mekanik klavyeler (Gateron Brown, Oreo Tactile), retro kasetçalar, daktilo ve yumuşak akustik tıklar.
* **🛡️ Sistem Tepsisi (Tray) & Single Instance:** Arka planda %0 CPU ile sessizce çalışır, çoklu pencere açılmasını engeller.

---

## 🚀 Hızlı Başlangıç & Kurulum

Uygulama **akıllı otomatik kurulum (self-healing)** desteğine sahiptir:

1. **⚡ Tek Tıkla Masaüstü Kısayolu:**
   - Klasördeki **`Kısayol Oluşturucu.vbs`** dosyasına çift tıklayın. Masaüstünüze doğrudan Türkçe karakterli başlatma kısayolu oluşturulur.
2. **🧩 Otomatik Kütüphane Yükleme:**
   - Gerekli Python kütüphaneleri (`customtkinter`, `matplotlib`, `pillow`, `pystray`) bilgisayarınızda eksikse, uygulama ilk açılışta bunu otomatik olarak tespit eder ve **tek tıkla arka planda kendisi indirip kurar**.
3. **💻 Manuel Kurulum (İsteğe Bağlı):**
   ```bash
   pip install -r requirements.txt
   python ToDoList.py
   ```

---

## 📂 Proje Yapısı

```
ToDo/
├── images/                  # Uygulama ve sistem tepsisi simgeleri (.ico)
├── sounds/                  # 20 adet lofi ve mekanik ses efektleri (.wav)
├── data/                    # Görev, sayaç ve ayar veritabanı (data.json)
├── ToDoList.py              # Ana uygulama kaynak kodu
├── baslat.bat               # Hızlı başlatma betiği
├── Kısayol Oluşturucu.vbs   # Evrensel Unicode masaüstü kısayol oluşturucu
├── requirements.txt         # Python kütüphane bağımlılıkları
└── README.md                # Proje dokümantasyonu
```