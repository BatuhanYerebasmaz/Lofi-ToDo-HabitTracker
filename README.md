# 📋 Görev & Alışkanlık Takip Programı (Lofi Habit Tracker)

Modern, estetik, oyunlaştırılmış ve yapay zeka destekli masaüstü görev ve alışkanlık takip uygulaması.

---

## ✨ Öne Çıkan Özellikler

### 🎮 1. Oyunlaştırma, XP & Seviye Sistemi (Level Up)
* **⭐ Seviye & Canlı XP Barı:** Başlığın yanında anlık seviye rozeti ve yumuşak geçişli XP ilerleme çubuğu.
* **🌟 Akıllı XP Dağıtımı:**
  * Tamamlanan her standart görev: `+15 XP`
  * **Sayaçlı görevler:** Toplam 15 XP adım sayısına orantılı bölünür (`(adım * 15) // hedef`); her adımda anlık pay verir ve hedefe ulaşıldığında tam `+15 XP` tamamlanır (Örn: 8 bardak suda her bardakta XP kazanımı).
  * Günlük %100 tamamlama: `+50 Bonus XP`
* **🏆 Seviye Skalası:**
  * **Lvl 1:** 🐣 Çaylak Başlangıç (0 - 49 XP)
  * **Lvl 2:** 🌿 Alışkanlık Tohumu (50 - 119 XP)
  * **Lvl 3:** ⚡ Odak Çırağı (120 - 199 XP)
  * **Lvl 4:** 🛡️ Disiplin Savaşçısı (200 - 299 XP)
  * **Lvl 5+:** 👑 Odak Efendisi (300+ XP)
* **🔥 Günlük Seri (Streak) & Rekor Takibi:** Düzenli tamamlanan ardışık gün sayısı takibi ve tüm zamanların en uzun seri rekoru.
* **🛡️ Zincir Koruma Kalkanı (Streak Freeze):** Haftalık 1 kalkan hakkı ile 1 günlük aksamalarda veya ertesi sabah başlandığında serinizi kırmadan akıllı koruma.
* **🎉 Günün Zaferi Kutlaması:** Günlük tüm görevler (%100) bittiğinde özel zafer penceresi ve kutlama hissi veren ses efekti.

---

### 📖 2. Otantik Defter & Polaroid Fotoğraf Scrapbook'u
* **📓 Tek Yapraklı Spiralli Kraft Defter:** Beyaz başlık çubuğu olmayan, Windows GDI destekli pürüzsüz yuvarlak köşeli (`SetWindowRgn`), serbest sürüklenebilir modern çerçevesiz tasarım.
* **📸 Sürükle & Bırak (Drag & Drop):** Bilgisayarınızdaki veya web'den indirdiğiniz fotoğrafları doğrudan defter sayfasına sürükleyip bırakarak albüme ekleme (`TkinterDnD`).
* **🎞️ Açılı Polaroid Galerisi:** Fotoğrafları doğal eğim açılarıyla, washi tape (dekoratif bant) ve beyaz polaroid çerçevesiyle sergileme.
* **🧭 EXIF Oryantasyon Desteği:** Cep telefonundan (iPhone/Android) aktarılan fotoğrafların yan/ters dönmesini engelleyen otomatik yön düzeltme.
* **⚡ Ultra-Hızlı Açılış:** Polaroid önbellekleme (`_POLAROID_CACHE`) ve thumbnail ön-ölçeklendirme sayesinde onlarca fotoğrafa rağmen gecikmesiz anında açılış.
* **✍️ 14 Punto El Yazısı & Canlı İstatistik:** `Segoe Print` fontu ile ferah el yazısı deneyimi, canlı kelime ve karakter sayacı.
* **🧹 Otomatik Depolama Temizliği:** Silinen fotoğrafları diskten anında temizleyen ve sahipsiz medya artıklarını önleyen akıllı temizleyici.

---

### 🔢 3. Sayaçlı Alışkanlıklar (Counter Habits)
* **🎯 Sayısal Hedef Belirleme:** Ayarlar'dan görev eklerken isteğe bağlı hedef sayaç belirleme (Örn: *8 Bardak Su*, *20 Sayfa Kitap*, *100 Şınav*).
* **🖱️ Çift Yönlü Akıllı Tıklama:**
  * **Sol Tık:** Sayacı `+1` artırır (`0/8 ➔ 1/8 ➔ ... ➔ ✓8`).
  * **Sağ Tık:** Sayacı `-1` azaltır (`8/8 ➔ 7/8 ➔ ... ➔ 0/8`), normal görevlerde ise işareti kaldırır.

---

### 📊 4. Modern Lofi Dashboard & Bağımsız Gezinme
* **📊 Haftalık Trend (Bar Grafik):** Dolgun çubuklar, günün öne çıkarılması ve her çubuğun üzerinde tamamlanan görev sayı etiketleri (`4`, `8`, vb.).
* **🍩 Aylık Odak (Donut / Halka Grafik):** Ortasında büyük **`% Başarı Oranı`** ve `Tamamlanan/Toplam` görev sayısını gösteren modern donut grafik.
* **🔒 Sabit ve Sarsıntısız Kart Düzeni:** Grid `uniform` kilidi sayesinde Alışkanlık Özeti içerisindeki yazı uzunlukları değişse bile sol grafiklerin yeri kesinlikle oynamaz.
* **🔄 Bağımsız Ay Gezinmesi:** Aylık Odak grafiğindeki `<` ve `>` butonları sadece grafiğin ayını değiştirir; alttaki takip tablosunun takvimini bozmaz.
* **🏆 3 Mini İstatistik Kartı:**
  * **👑 En Uzun Seri:** Tüm zamanların en yüksek kesintisiz gün rekoru.
  * **⚡ Bu Ay Başarı:** Seçili ayda tamamlanan toplam görev ve başarı yüzdesi.
  * **🎯 En İstikrarlı:** Bu ay en çok tamamlanan favori alışkanlığınız.

---

### 📅 5. Aylık Takip Tablosu & Minimalist Gezinme
* **🎨 Pastel Aylık Matris Tablosu:** Ayın tüm günlerini (1-31) tek ekranda ultra-hızlı ve yumuşak pastel renklerle gösterir.
* **⚡ Günlük Moral & Efektiflik Takibi:** Her gün için 1-5 arası moral ve verimlilik puanlaması.
* **🎈 Canlı Not Önizleme (Hover Tooltip):** Tabloda not bulunan günlerin üzerine gelindiğinde not özetini ve fotoğraf sayısını gösteren şık önizleme balonu.
* **💊 Minimalist Ay Gezinme Kapsülü:** Tablonun hemen altındaki zarif kapsülle geçmiş ve gelecek ayların kayıtları arasında hızlıca gezinme; ay adına tıklandığında anında geçerli aya geri dönme.

---

### 🤖 6. Yapay Zeka Darlama & Hatırlatma Motoru
* **🧠 Yerel & Bulut LLM Desteği:**
  * **Google Gemini API (Ücretsiz):** Google AI Studio API anahtarıyla buluttan ışık hızında çalışan `Google Gemini 1.5 Flash` ve `Google Gemini 2.0 Flash` modelleri.
  * **⚡ Canlı API Bağlantı Testi:** Ayarlar penceresinden `⚡ Test Et` butonuna basarak Google Gemini bağlantınızı anında doğrulama.
  * **Dahili Yerel Motor:** Harici hiçbir kurulum gerektirmeyen hazır çevrimdışı motor.
  * **Ollama & LM Studio:** Kendi bilgisayarınızdaki yerel açık kaynak modeller.
* **🎭 Farklı Kişilik Modları:** *Sert & Direkt*, *Alaycı & Esprili*, *Motivasyonel* ve *Özel Prompt*.
* **⏰ Akıllı Zamanlama:** Görevler için rastgele aralıklarla bağımsız bildirimler ve 30 saniyelik otomatik erteleme mekanizması.

---

### 📌 7. Kayan Mini Widget (Sticky Mode) & Global Kısayol
* **📌 Kayan Mini Görev Kartı (Always-on-Top):** Ekranın köşesinde her zaman üstte duran, kenar çizgisiz, yumuşak yuvarlak pastel kart tasarımı.
* **🔄 Karşılıklı Geçiş (Mutually Exclusive):**
  * Ana ekrandan `📌 Mini` butonuna basıldığında ana ekran gizlenir ve mini widget açılır.
  * Mini widget üzerindeki `↗` butonuna basıldığında mini widget kapanır ve ana ekran geri gelir.
* **⌨️ Global Klavye Kısayolu (`Ctrl+Shift+T`):** Hangi uygulamada veya oyunda olursanız olun klavyeden `Ctrl+Shift+T` basarak ana ekran ile mini widget arasında anında geçiş yapma (%0 CPU).

---

### 🎨 8. Temalar & Lofi Ses Paketi
* **🎨 20 Estetik Tema:** 10 Pastel Aydınlık (Latte & Şeftali, Matcha Yeşili vb.) ve 10 Modern Karanlık (Karanlık Karbon, Gece Mavisi vb.) tema.
* **🎵 20 Farklı Mekanik & Lofi Ses Efekti:** 
  * Görev tamamlama, buton tıklama, bildirimler ve moral/efektiflik puanlama için **4 bağımsız ses kanalı**.
  * Mekanik klavyeler (Gateron Brown, Oreo Tactile), retro kasetçalar, daktilo ve yumuşak akustik tıklar.
* **🛡️ Windows Katı Tekil Çalışma (`SO_EXCLUSIVEADDRUSE`):** Arka planda %0 CPU ile sessizce çalışır; masaüstü kısayoluna tekrar basıldığında yeni kopya açmaz, mevcut programı anında öne getirip büyütür.

---

## 🚀 Hızlı Başlangıç & Kurulum

Uygulama **akıllı otomatik kurulum (self-healing)** desteğine sahiptir:

1. **⚡ Tek Tıkla Masaüstü Kısayolu:**
   - Klasördeki **`Kısayol Oluşturucu.vbs`** dosyasına çift tıklayın. Masaüstünüze doğrudan Türkçe karakterli başlatma kısayolu oluşturulur.
2. **🧩 Otomatik Kütüphane Yükleme:**
   - Gerekli Python kütüphaneleri (`customtkinter`, `matplotlib`, `pillow`, `pystray`, `tkinterdnd2`) bilgisayarınızda eksikse, uygulama ilk açılışta bunu otomatik tespit eder ve **tek tıkla arka planda kendisi kurar**.
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
│   └── notes_media/         # Defter sayfalarına eklenen fotoğraflar ve polaroidler
├── ToDoList.py              # Ana uygulama kaynak kodu
├── baslat.bat               # Hızlı başlatma betiği
├── Kısayol Oluşturucu.vbs   # Evrensel Unicode masaüstü kısayol oluşturucu
├── requirements.txt         # Python kütüphane bağımlılıkları
├── .gitignore               # Git dışlama kuralları
└── README.md                # Proje dokümantasyonu
```