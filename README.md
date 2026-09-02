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
* **📸 Sürükle & Bırak (Drag & Drop):** Bilgisayarınızdaki veya web'den indirdiğiniz fotoğrafları doğrudan defter sayfasına sürükleyip bırakarak albüme ekleme.
* **🧭 EXIF Oryantasyon Desteği:** Cep telefonundan (iPhone/Android) aktarılan fotoğrafların yan/ters dönmesini engelleyen otomatik yön düzeltme.
* **⚡ Ultra-Hızlı Açılış:** Polaroid önbellekleme (`_POLAROID_CACHE`) ve thumbnail ön-ölçeklendirme sayesinde onlarca fotoğrafa rağmen gecikmesiz anında açılış.

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

### 🍎 macOS Kurulumu

Uygulama Windows için yazıldı, ancak `MacOS/` klasöründeki başlatıcı sayesinde **ana kaynak koda tek satır dokunmadan** macOS'ta da çalışır.

**A) Hazır uygulama (.dmg ile kurulum — önerilen)**

1. Hazır kurulum dosyası repoda: **[`dist/Lofi-ToDo-HabitTracker.dmg`](dist/Lofi-ToDo-HabitTracker.dmg)** (~11 MB). İndirip açın ve uygulamayı **Applications** klasörüne sürükleyin.
2. İlk açılışta macOS "geliştirici doğrulanamadı" diyebilir (imzasız uygulama): uygulamaya **sağ tıklayıp → Aç** deyin.
3. İlk açılış, bilgisayarınızdaki Python 3 ile kendi sanal ortamını kurar (birkaç dakika); sonrakiler anındadır.
   Tkinter destekli bir Python 3 gerekir: [python.org](https://www.python.org/downloads/macos/).

Verileriniz `~/Library/Application Support/Lofi-ToDo-HabitTracker/data` altında tutulur — uygulamayı silmek veriyi silmez.

**B) Kaynaktan çalıştırma (geliştirme)**

1. **`MacOS/Baslat.command`** dosyasına çift tıklayın.
   - İlk açılışta kendi sanal ortamını (`MacOS/.venv`) kurar ve bağımlılıkları indirir (1-2 dk), sonraki açılışlar anındadır.
   - Veriler bu modda proje içindeki `data/` klasöründe kalır.

**C) Release paketi üretme**

```bash
bash MacOS/build_release.command      # -> dist/Lofi-ToDo-HabitTracker.app + .dmg (~11 MB)
```
İkonu yeniden çizmek için: `MacOS/.venv/bin/python MacOS/make_app_icon.py`

**Başlatıcı ne yapıyor?** Çalışma anında şu macOS uyarlamalarını yapar (dosyaya yazmaz, yalnızca bellekte):
   - **Ses:** Windows `winsound`/`winmm` yerine sahte modül + `afplay`.
   - **Görsel açma:** `os.startfile` yerine macOS `open` komutu.
   - **Sistem tepsisi:** `pystray` macOS'ta ana iş parçacığı dışında çalışamadığı için tepsi kapatılır; pencereyi kapatmak uygulamayı **Dock'a küçültür**.
   - **Kimlik:** python.org derlemesi menü çubuğunda "Python" yazdığı için uygulama adı ve Dock ikonu `NSBundle` üzerinden düzeltilir.
   - **Mimari:** universal2 Python bazen Rosetta (x86_64) ile açılıp arm64 paketlerini yükleyemediği için başlatıcı native mimariyi zorlar.

macOS'ta devre dışı kalan Windows'a özgü özellikler: global `Ctrl+Shift+T` kısayolu, köşe yuvarlatma (DWM API) ve `.ico` başlık simgesi.

---

## 📂 Proje Yapısı

```
ToDo/
├── images/                  # Uygulama ve sistem tepsisi simgeleri (.ico)
├── sounds/                  # 20 adet lofi ve mekanik ses efektleri (.wav)
├── data/                    # Görev, sayaç ve ayar veritabanı (data.json)
│   └── notes_media/         # Defter sayfalarına eklenen fotoğraflar ve polaroidler
├── MacOS/                   # macOS desteği (ana kodu değiştirmez)
│   ├── Baslat.command       # Kaynaktan çift tıkla başlat (venv kurar + açar)
│   ├── build_release.command# .app + .dmg release paketi üretir -> dist/
│   ├── make_app_icon.py     # 1024px uygulama ikonu (AppIcon.icns) üreticisi
│   ├── AppIcon.icns         # Uygulama ikonu
│   └── mac_launcher.py      # winsound stub + afplay/open/tepsi/veri yamaları
├── ToDoList.py              # Ana uygulama kaynak kodu
├── baslat.bat               # Hızlı başlatma betiği (Windows)
├── Kısayol Oluşturucu.vbs   # Evrensel Unicode masaüstü kısayol oluşturucu
├── requirements.txt         # Python kütüphane bağımlılıkları
├── .gitignore               # Git dışlama kuralları
└── README.md                # Proje dokümantasyonu
```