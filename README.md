# 📋 Görev & Alışkanlık Takip Programı (Lofi Habit Tracker)

Modern, estetik, oyunlaştırılmış ve yapay zeka destekli masaüstü görev ve alışkanlık takip uygulaması.

---

## ✨ Temel Özellikler

### 🎮 1. Oyunlaştırma, XP & Seviye Sistemi (Level Up)
* **⭐ Seviye & XP İlerleme Barı:** Başlığın yanında canlı seviye göstergesi ve dinamik XP çubuğu 
* **🌟 XP Kazanma Mekanikleri:**
  * Her tamamlanan standart görev: `+15 XP`
  * Sayaçlı görev adımları: `+2 XP` (hedef tamamlandığında `+10 XP`)
  * Günlük %100 tamamlama: `+50 Bonus XP`
* **🏆 Seviye & Unvan Skalası:**
* **🔥 Günlük Seri (Streak):** Düzenli tamamlanan ardışık gün sayısı takibi.
* **🛡️ Zincir Koruma Kalkanı (Streak Freeze):** Haftalık 1 kalkan hakkı ile 1 günlük aksamalarda serinizi kırmadan koruma.
* **🎉 Günün Zaferi Kutlaması:** Günlük tüm görevler (%100) bittiğinde özel zafer penceresi ve kutlama sesi.

---

### 🔢 2. Sayaçlı Alışkanlıklar (Counter Habits)
* **🎯 Sayısal Hedef Belirleme:** Ayarlar'dan görev eklerken isteğe bağlı hedef sayaç belirleme (Örn: *8 Bardak Su*, *20 Sayfa Kitap*, *100 Şınav*).
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
* **🧠 Yerel & Bulut LLM Desteği:** Dahili Baskıcı AI Motoru (hızlı/çevrimdışı), Ollama veya LM Studio yerel modelleri.
* **🎭 Farklı Kişilik Modları:** *Sert & Direkt*, *İğneleyici / Alaycı*, *Pasif Agresif*, *Motive Edici / Koçluk* ve *Özel Prompt*.
* **⏰ Akıllı Zamanlama:** Görevler için rastgele aralıklarla bağımsız bildirimler ve 30 saniyelik otomatik erteleme mekanizması.
* **⚠️ Otantik Windows Hata Penceresi:** Bildirimler 3 kez ertelendiğinde gerçek sistem hata diyalogu hissi veren dinamik arayüz.

---

### 🎨 6. Temalar & Lofi Ses Paketi
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