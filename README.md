# 📋 Görev & Alışkanlık Takip Programı (Habit Tracker)

Modern, estetik ve yapay zeka destekli masaüstü görev ve alışkanlık takip uygulaması.

---

## ✨ Özellikler

- **🎨 20 Estetik Tema:** 10 Pastel Aydınlık (Light) ve 10 Modern Karanlık (Dark) tema.
- **🎵 Zengin Lofi & Mekanik Ses Paketi:** 20 farklı mekanik klavye, lofi pop, daktilo ve akustik ses efekti.
  - Görev tamamlama, arayüz butonları ve standart bildirimler için bağımsız ses atama.
- **🤖 Akıllı AI Darlama Motoru:** Yapılmayan görevler için bağlamsal Türkçe hatırlatmalar ve yerel LLM entegrasyonu (Ollama & LM Studio).
- **⚠️ Otantik Windows Hata Penceresi:** Bildirimler ertelendiğinde gerçek sistem hata diyalogu hissi veren dinamik arayüz.
- **📊 Canlı Grafikler:** Haftalık çubuk grafik, aylık başarı oranları ve pasta dağılım grafiği (Matplotlib).
- **🛡️ Sistem Tepsisi (Tray) & Single Instance:** Arka planda %0 CPU ile sessizce çalışır, çakışmaları engeller.

---

## 🚀 Kurulum

1. **Gereksinimleri Yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Masaüstü Kısayolu Oluşturun (İsteğe Bağlı):**
   - Klasördeki **`Kısayol Oluşturucu.vbs`** dosyasına çift tıklayarak siyah konsol penceresi açılmadan, sessizce masaüstünüze özel simgesiyle birlikte kısayol ekleyebilirsiniz.

3. **Uygulamayı Başlatın:**
   ```bash
   python ToDoList.py
   # veya doğrudan:
   baslat.bat
   ```

---

## 📂 Proje Yapısı

```
ToDo/
├── images/                  # Uygulama ve sistem tepsisi simgeleri (.ico)
├── sounds/                  # 20 adet lofi ve mekanik ses efektleri (.wav)
├── data/                    # Görev ve ayar veritabanı (data.json)
├── ToDoList.py              # Ana uygulama kaynak kodu
├── baslat.bat               # Hızlı başlatma betiği
├── Kısayol Oluşturucu.vbs   # Sessiz masaüstü kısayol oluşturucu
├── requirements.txt         # Python kütüphane bağımlılıkları
└── README.md                # Dokümantasyon
```