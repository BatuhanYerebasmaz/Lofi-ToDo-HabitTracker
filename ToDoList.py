import sys
import subprocess
import os

# ============================================================
#  OTOMATİK BAĞIMLILIK KONTROLÜ & YÜKLEYİCİ (SELF-HEALING)
# ============================================================
REQUIRED_PACKAGES = {
    "customtkinter": "customtkinter>=5.2.0",
    "matplotlib": "matplotlib>=3.7.0",
    "PIL": "pillow>=10.0.0",
    "pystray": "pystray>=0.19.5"
}

missing_packages = []
for import_name, pkg_req in REQUIRED_PACKAGES.items():
    try:
        __import__(import_name)
    except ImportError:
        missing_packages.append(pkg_req)

if missing_packages:
    try:
        import tkinter as tk
        from tkinter import messagebox
        _root = tk.Tk()
        _root.withdraw()
        ans = messagebox.askyesno(
            "Gerekli Kütüphaneler Eksik",
            "Uygulamanın çalışması için gerekli kütüphaneler bilgisayarınızda eksik:\n\n• " +
            "\n• ".join(missing_packages) +
            "\n\nOtomatik olarak yüklenip uygulama başlatılsın mı?"
        )
        if ans:
            flags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            subprocess.run([sys.executable, "-m", "pip", "install", *missing_packages], check=True, creationflags=flags)
            messagebox.showinfo("Kurulum Tamamlandı", "Kütüphaneler başarıyla yüklendi! Uygulama başlatılıyor.")
        else:
            sys.exit(1)
        _root.destroy()
    except Exception as e:
        try:
            import tkinter as tk
            from tkinter import messagebox
            messagebox.showerror("Hata", f"Kütüphaneler yüklenirken hata oluştu:\n{e}\n\nLütfen terminalde 'pip install -r requirements.txt' komutunu çalıştırın.")
        except Exception:
            pass
        sys.exit(1)

import customtkinter as ctk
import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import calendar
import json
import random
import threading
import ctypes
import socket
import winsound
import webbrowser
import time

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
DATA_FILE = os.path.join(DATA_DIR, "data.json")

# Kök dizinde eski data.json varsa otomatik data/ içine taşı
_old_root_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
if os.path.exists(_old_root_data) and not os.path.exists(DATA_FILE):
    try:
        import shutil
        shutil.move(_old_root_data, DATA_FILE)
    except Exception:
        pass

TURKISH_MONTHS = {
    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan",
    5: "Mayıs", 6: "Haziran", 7: "Temmuz", 8: "Ağustos",
    9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
}

SHORT_DAYS = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Pzr"]

import ctypes
import threading

SOUNDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")

SOUND_OPTIONS = {
    "Mekanik & Pop İkilisi": {
        "on_file": "tactile_pop.wav",
        "off_file": "mechanical_switch.wav",
        "desc": "Açarken dokunsal pop, kapatırken tok mekanik switch sesi"
    },
    "Krem Switch (Lofi)": {
        "on_file": "lofi_keystroke.wav",
        "off_file": "lofi_keystroke.wav",
        "desc": "Orijinal yağlanmış krem mekanik klavye tuşu (Linear switch)"
    },
    "NovelKeys Cream (Lofi)": {
        "on_file": "nk_cream_press.wav",
        "off_file": "nk_cream_release.wav",
        "desc": "NovelKeys Cream yağlanmış lofi basma ve bırakma sesi"
    },
    "Topre Kapasitif Thock": {
        "on_file": "topre_capacitive.wav",
        "off_file": "topre_capacitive.wav",
        "desc": "Topre elektrostatik kapasitif tuş, yumuşak ve tok lofi vuruş"
    },
    "Yağlı Tealios (Pürüzsüz)": {
        "on_file": "lubed_tealios.wav",
        "off_file": "lubed_tealios.wav",
        "desc": "Ultra pürüzsüz lubed linear switch tuş vuruşu"
    },
    "Düşük Thock (Derin Bas)": {
        "on_file": "deep_thock.wav",
        "off_file": "deep_thock.wav",
        "desc": "Tok ve derin bas rezonanslı mekanik thock"
    },
    "Krem Tokluk (Creamy Thump)": {
        "on_file": "creamy_thump.wav",
        "off_file": "creamy_thump.wav",
        "desc": "Tok, kremsi ve tatmin edici klavye tuşu"
    },
    "Çıtır Tık": {
        "on_file": "crisp_tap.wav",
        "off_file": "crisp_tap.wav",
        "desc": "Çok net, temiz ve çıtır mikro anahtar sesi"
    },
    "Çıtır Mavi Switch (Clicky)": {
        "on_file": "cherry_blue_click.wav",
        "off_file": "cherry_blue_click.wav",
        "desc": "Belirgin mekanik klik sesi (Cherry Blue Switch)"
    },
    "Cozy Lofi Pop (Animal Pop)": {
        "on_file": "cozy_animal_pop.wav",
        "off_file": "cozy_animal_pop.wav",
        "desc": "Animal Crossing tarzı sevimli ve sıcak tuş sesi"
    },
    "Ahşap Blok & Bambu": {
        "on_file": "zen_wood_block.wav",
        "off_file": "zen_wood_block.wav",
        "desc": "Organik, tok ve dinlendirici ahşap vuruş sesi"
    },
    "Tatlı Kabarcık (Bubble Pop)": {
        "on_file": "bubble_pop.wav",
        "off_file": "bubble_pop.wav",
        "desc": "Ferahlatıcı su damlası ve kabarcık patlama sesi"
    },
    "Kaset & Walkman Tuşu": {
        "on_file": "tape_deck_click.wav",
        "off_file": "tape_deck_click.wav",
        "desc": "Retro kasetçalar / Walkman mekanik tuş sesi"
    },
    "Oreo Dokunsal Switch": {
        "on_file": "oreo_switch.wav",
        "off_file": "oreo_switch.wav",
        "desc": "Everglide Oreo tok dokunsal switch vuruşu"
    },
    "Akustik Tık": {
        "on_file": "acoustic_tick.wav",
        "off_file": "acoustic_tick.wav",
        "desc": "Doğal ve berrak akustik mikro tık sesi"
    },
    "Yumuşak Toggle": {
        "on_file": "soft_toggle.wav",
        "off_file": "soft_toggle.wav",
        "desc": "Zarif ve dinlendirici yumuşak anahtar sesi"
    },
    "Minimalist UI Tık": {
        "on_file": "minimal_ui_tick.wav",
        "off_file": "minimal_ui_tick.wav",
        "desc": "Zarif, temiz ve modern arayüz tık sesi"
    },
    "Vintage Klavye": {
        "on_file": "vintage_key.wav",
        "off_file": "vintage_key.wav",
        "desc": "Retro daktilo / eski mekanik klavye tuş vuruşu"
    },
    "Hafif Mouse": {
        "on_file": "mouse_click.wav",
        "off_file": "mouse_release.wav",
        "desc": "Sessiz ofis faresi basma ve bırakma sesi"
    },
    "Sessiz": {
        "on_file": None,
        "off_file": None,
        "desc": "Ses efektlerini tamamen kapat"
    }
}


class SoundEngine:
    """Çok kanallı, üst üste basıldığında kesilmeyen sıfır gecikmeli ses motoru."""
    _id = 0
    _lock = threading.Lock()

    @classmethod
    def play(cls, file_name):
        if not file_name:
            return
        file_path = os.path.join(SOUNDS_DIR, file_name)
        if not os.path.exists(file_path):
            return
        with cls._lock:
            cls._id = (cls._id + 1) % 16
            ch = f"snd_ch_{cls._id}"

        def _p():
            try:
                winmm = ctypes.windll.winmm
                winmm.mciSendStringW(f"close {ch}", None, 0, 0)
                p = os.path.abspath(file_path).replace("\\", "/")
                winmm.mciSendStringW(f'open "{p}" type waveaudio alias {ch}', None, 0, 0)
                winmm.mciSendStringW(f"play {ch} from 0 wait", None, 0, 0)
                winmm.mciSendStringW(f"close {ch}", None, 0, 0)
            except Exception:
                pass

        threading.Thread(target=_p, daemon=True).start()


def play_task_sound(is_checking=True):
    """Görev kutucuğu işaretlendiğinde veya kaldırıldığında ses çalar."""
    try:
        cur_sound = "Mekanik & Pop İkilisi"
        if hasattr(HabitTrackerApp, "CURRENT_INSTANCE") and HabitTrackerApp.CURRENT_INSTANCE:
            cur_sound = HabitTrackerApp.CURRENT_INSTANCE.settings.get("task_sound", "Mekanik & Pop İkilisi")
        if cur_sound == "Sessiz":
            return
        info = SOUND_OPTIONS.get(cur_sound)
        if info:
            SoundEngine.play(info["on_file"] if is_checking else info["off_file"])
    except Exception:
        pass


def play_button_sound():
    """Menü ve arayüz butonlarına basıldığında ses çalar."""
    try:
        cur_sound = "Krem Switch (Lofi)"
        if hasattr(HabitTrackerApp, "CURRENT_INSTANCE") and HabitTrackerApp.CURRENT_INSTANCE:
            cur_sound = HabitTrackerApp.CURRENT_INSTANCE.settings.get("button_sound", "Krem Switch (Lofi)")
        if cur_sound == "Sessiz":
            return
        info = SOUND_OPTIONS.get(cur_sound)
        if info and info["on_file"]:
            SoundEngine.play(info["on_file"])
    except Exception:
        pass


def play_notification_sound():
    """Standart görev hatırlatma bildirimleri ekrana geldiğinde seçili sesi çalar."""
    try:
        cur_sound = "Cozy Lofi Pop (Animal Pop)"
        if hasattr(HabitTrackerApp, "CURRENT_INSTANCE") and HabitTrackerApp.CURRENT_INSTANCE:
            cur_sound = HabitTrackerApp.CURRENT_INSTANCE.settings.get("notification_sound", "Cozy Lofi Pop (Animal Pop)")
        if cur_sound == "Sessiz":
            return
        info = SOUND_OPTIONS.get(cur_sound)
        if info and info["on_file"]:
            SoundEngine.play(info["on_file"])
    except Exception:
        pass


def play_rating_sound():
    """Moral ve Efektiflik puanlama kutucuklarına basıldığında seçili sesi çalar."""
    try:
        cur_sound = "Minimalist UI Tık"
        if hasattr(HabitTrackerApp, "CURRENT_INSTANCE") and HabitTrackerApp.CURRENT_INSTANCE:
            cur_sound = HabitTrackerApp.CURRENT_INSTANCE.settings.get("rating_sound", "Minimalist UI Tık")
        if cur_sound == "Sessiz":
            return
        info = SOUND_OPTIONS.get(cur_sound)
        if info and info["on_file"]:
            SoundEngine.play(info["on_file"])
    except Exception:
        pass


# ============================================================
#  OYUNLAŞTIRMA (XP & SEVİYE SİSTEMİ)
# ============================================================
LEVEL_RANKS = [
    (1, "🐣", "Çaylak"),
    (2, "🌱", "Hevesli"),
    (3, "⚡", "Odak Çırağı"),
    (5, "🎯", "Disiplin Yolcusu"),
    (8, "🔥", "İrade Savaşçısı"),
    (10, "⚔️", "Alışkanlık Ustası"),
    (15, "🛡️", "İrade Muhafızı"),
    (20, "🏆", "Odak Şampiyonu"),
    (30, "👑", "Disiplin Şövalyesi"),
    (50, "🧘", "Lofi Gurusu")
]


def get_level_info(xp):
    """Verilen toplam XP'ye göre seviye, mevcut seviye XP'si, sonraki seviye hedefi, yüzde ve unvan döndürür."""
    level = 1
    xp_remaining = max(0, int(xp))
    while True:
        needed_for_next = 80 + (level * 40)
        if xp_remaining < needed_for_next:
            break
        xp_remaining -= needed_for_next
        level += 1

    needed_for_next = 80 + (level * 40)
    progress_ratio = min(1.0, max(0.0, xp_remaining / needed_for_next))

    rank_icon, rank_title = "🐣", "Çaylak"
    for req_lvl, icon, title in LEVEL_RANKS:
        if level >= req_lvl:
            rank_icon, rank_title = icon, title
        else:
            break

    return {
        "level": level,
        "current_xp": xp_remaining,
        "next_xp": needed_for_next,
        "total_xp": max(0, int(xp)),
        "ratio": progress_ratio,
        "icon": rank_icon,
        "title": rank_title
    }


# ============================================================
#  SİSTEM TEPSİSİ & YEREL AI DARLAMA MOTORU
# ============================================================
import urllib.request
import urllib.error
import subprocess
from PIL import Image, ImageDraw
import pystray

ICON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "ToDo.ico")
if not os.path.exists(ICON_FILE):
    ICON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ToDo.ico")


def create_tray_icon_image():
    """Sistem tepsisi için varsa ToDo.ico dosyasını açar, yoksa zarif mor ikon üretir."""
    if os.path.exists(ICON_FILE):
        try:
            return Image.open(ICON_FILE)
        except Exception:
            pass
    img = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([4, 4, 60, 60], radius=16, fill="#7C3AED")
    d.line([(18, 33), (28, 44), (46, 20)], fill="#FFFFFF", width=6)
    return img


DEFAULT_AI_MODEL = "Dahili Baskıcı AI Motoru (Yerel/Hızlı)"


def scan_local_ai_models():
    """Google Gemini, Ollama ve LM Studio modellerini tarar ve listeler."""
    models = [
        DEFAULT_AI_MODEL,
        "Google Gemini (1.5 Flash - Hızlı & Ücretsiz)",
        "Google Gemini (2.0 Flash - Yeni)",
    ]
    found_set = set(models)

    # 1. Ollama Disk Manifest Taraması (Ollama servisi kapalı olsa dahi diskteki modelleri 1ms'de bulur)
    ollama_dir = os.path.expanduser("~/.ollama/models/manifests/registry.ollama.ai")
    if os.path.exists(ollama_dir):
        for root, dirs, files in os.walk(ollama_dir):
            if files:
                rel = os.path.relpath(root, ollama_dir).replace("\\", "/").replace("library/", "")
                for f in files:
                    tag = f if f != "latest" else ""
                    m_name = f"{rel}:{f}" if tag else rel
                    label = f"[Ollama] {m_name}"
                    if label not in found_set:
                        found_set.add(label)
                        models.append(label)

    # 2. LM Studio Disk Taraması (GGUF modelleri)
    lm_dir = os.path.expanduser("~/.lmstudio/models")
    if os.path.exists(lm_dir):
        for root, dirs, files in os.walk(lm_dir):
            for f in files:
                if f.lower().endswith((".gguf", ".bin")):
                    name = f.replace(".gguf", "").replace(".bin", "")
                    label = f"[LM Studio] {name}"
                    if label not in found_set:
                        found_set.add(label)
                        models.append(label)

    # 3. Canlı Ollama / LM Studio API Taraması (Aktif çalışıyorsa anlık 127.0.0.1 çeker)
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
        with urllib.request.urlopen(req, timeout=0.15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for m in data.get("models", []):
                name = m.get("name")
                if name:
                    label = f"[Ollama] {name}"
                    if label not in found_set:
                        found_set.add(label)
                        models.append(label)
    except Exception:
        pass

    try:
        req = urllib.request.Request("http://127.0.0.1:1234/v1/models")
        with urllib.request.urlopen(req, timeout=0.15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for m in data.get("data", []):
                mid = m.get("id")
                if mid:
                    label = f"[LM Studio] {mid}"
                    if label not in found_set:
                        found_set.add(label)
                        models.append(label)
    except Exception:
        pass

    return models


# Görev anahtar kelimelerine göre zengin bağlamsal mesaj havuzu
TASK_CONTEXT_MESSAGES = {
    ("kod", "yazılım", "python", "program", "script", "develop", "bug"): {
        "Sert & Direkt": [
            "Hani kod yazacaktın? Editör açılmayı bekliyor, sen değil.",
            "Kodlama günün geçiyor, klavyeye dokunmadın bile. Başla artık.",
            "Bugün bir satır bile kod yazmadın. Açıklaması ne?",
            "Kod yazmak için 'yarın' diye bir gün yok. Şimdi başla.",
        ],
        "Alaycı & Esprili": [
            "Hani kod yazacaktın? Yoksa bug'lar seni korkuttu mu?",
            "Kodlama görevini görünce kaçtın galiba, klavye seni özledi.",
            "Stack Overflow'a bakmak kod yazmak sayılmıyor, aç editörü.",
            "Bilgisayarın senden daha çok çalıştı bugün, en azından o açık kaldı.",
        ],
        "Motivasyonel": [
            "Her büyük proje tek bir satır kodla başlar. Bugün o satırı yaz!",
            "Kodlama kasını güçlendirmenin tek yolu pratik. Bugün birkaç satır yaz!",
            "Bugün yazdığın kod, gelecekteki senin teşekkür edeceği bir yatırım.",
        ],
    },
    ("oyun", "game", "gamer", "play", "konsol"): {
        "Sert & Direkt": [
            "Hani oyun oynayacaktın? Geri adım mı atıyorsun?",
            "Oyun vaktin geldi geçiyor, controller'ı al ve başla.",
            "Kendine ayırdığın oyun molasını bile erteliyorsun, geç kalma.",
        ],
        "Alaycı & Esprili": [
            "Oyun oynayacaktın ama oyun oynamayı bile erteliyorsun, hayırdır?",
            "Oyun oynamaya bile üşeniyorsan cidden durum vahim demektir.",
            "Boss savaşından mı kaçıyorsun, neden oyuna girmedin?",
        ],
        "Motivasyonel": [
            "Eğlence de dinlenmenin bir parçası. Hak ettiğin molayı al ve oyna!",
            "Zihnini dağıtmak için oyun harika bir mola. Oyna ve tadını çıkar!",
        ],
    },
    ("spor", "gym", "fitness", "antrenman", "egzersiz", "şınav", "mekik"): {
        "Sert & Direkt": [
            "Spor yapacaktın, ne oldu? Koltuktan kalkamadın mı?",
            "Bugün spor günüydü ama sen oturarak geçirdin. Kalk hareket et.",
            "Spora başlamak için mükemmel anı bekleme, şimdi kalk.",
        ],
        "Alaycı & Esprili": [
            "Spor yerine kumandayı kaldırmak spor sayılmıyor maalesef.",
            "Hani spor yapacaktın? Buzdolabına yürümek antrenman değil.",
            "Kas ağrısı çekmekten mi korkuyorsun yoksa tembellikten mi?",
        ],
        "Motivasyonel": [
            "30 dakika spor, 24 saat iyi hissettirir. Bugün o 30 dakikayı ayır!",
            "Bedenin sana teşekkür edecek. Kalk ve hareket et!",
            "Spor yaptıktan sonraki o enerji için değer. Başla!",
        ],
    },
    ("yürü", "yürüyüş", "koş", "adım", "walk", "run"): {
        "Sert & Direkt": [
            "Yürüyüşe çıkacaktın, hâlâ içerdesin. Ayakkabılarını giy ve çık.",
            "Bugün adım sayın sıfır. Kalk ve yürüyüşe çık.",
        ],
        "Alaycı & Esprili": [
            "Yürüyüş hedefin var ama bacakların izin günü almış galiba.",
            "Adım sayacın seni merak ediyor, bugün hiç sinyal almadı.",
        ],
        "Motivasyonel": [
            "Kısa bir yürüyüş bile zihnini temizler. Hadi çık biraz!",
            "Her adım sağlığa bir adım. Bugün kaç adım atacaksın?",
        ],
    },
    ("oku", "kitap", "makale", "sayfa", "read", "book"): {
        "Sert & Direkt": [
            "Okuma hedefin vardı, kitap rafta toz topluyor. Aç ve oku.",
            "Bugün bir sayfa bile okumadın. Telefonu bırak, kitabı aç.",
        ],
        "Alaycı & Esprili": [
            "Sosyal medya scroll'u okuma sayılmıyor, gerçek kitap aç biraz.",
            "Kitapların senden daha sabırlı, hâlâ bekliyorlar ama sonsuza kadar değil.",
        ],
        "Motivasyonel": [
            "Her gün 10 sayfa oku, yılda 12 kitap bitirir. Bugün başla!",
            "Okumak zihnin egzersizi. Bugün birkaç sayfa ayır kendine.",
        ],
    },
    ("ders", "ödev", "sınav", "çalış", "kurs", "etüt", "test"): {
        "Sert & Direkt": [
            "Ders çalışma vaktin geldi geçiyor. Masanın başına otur ve başla.",
            "Sınavlar ve hedefler ertelemeyi beklemez. Şimdi odaklan.",
            "Bugün çalışmazsan yarın iki katı yükün olacak. Başla.",
        ],
        "Alaycı & Esprili": [
            "Bilgiler ozmoz yoluyla beynine girmeyecek, mecburen açıp çalışacaksın.",
            "Masanın başında telefonla oynamak ders çalışmak sayılmıyor.",
            "Ders çalışmaktan kaçış hızın ışık hızını geçti tebrikler.",
        ],
        "Motivasyonel": [
            "Bugün gösterdiğin çaba, yarınki başarının temeli. Masaya geç ve parılda!",
            "Zor olan başlamaktır, 15 dakika odaklan gerisi kendiliğinden gelir!",
        ],
    },
    ("ingilizce", "dil", "almanca", "kelime", "duolingo", "vocab"): {
        "Sert & Direkt": [
            "Dil pratiğini bugün yapmadın. Her gün tekrar etmezsen unutursun.",
            "Yabancı dil çalışması aksatılmaz. Aç ve 15 dakika pratik yap.",
        ],
        "Alaycı & Esprili": [
            "Yes no goodbye diyerek akıcı olamazsın, aç şu dersi çalış.",
            "Duolingo kuşu kapına dayanmadan önce gir de dersini yap.",
        ],
        "Motivasyonel": [
            "Günde sadece 10 yeni kelime yılda 3500 kelime yapar. Pratiğe başla!",
        ],
    },
    ("kalk", "uyan", "sabah", "alarm", "erken"): {
        "Sert & Direkt": [
            "Erken kalkma hedefini yine kaçırdın. Yarın alarmı kur ve bu sefer kalk.",
            "Yataktan zamanında kalkamıyorsan hedeflerine nasıl ulaşacaksın?",
        ],
        "Alaycı & Esprili": [
            "Alarm çaldı, sen erteledin, yine aynı hikâye. Kaçıncı tekrar bu?",
            "Yastığınla aşk yaşaman güzel ama hedeflerin seni bekliyor.",
        ],
        "Motivasyonel": [
            "Erken kalkan yol alır. Yarın o alarmla birlikte kalk, farkı hissedeceksin!",
            "Sabahları kazanmak günü kazanmaktır. Yarın dene!",
        ],
    },
    ("su", "hidrasyon", "water"): {
        "Sert & Direkt": [
            "Bugün yeterince su içtin mi? Vücudun susuz kalmayı hak etmiyor.",
            "Su içmeyi unutma, bu kadar basit bir şeyi bile erteleme.",
        ],
        "Alaycı & Esprili": [
            "Çay ve kahve su sayılmıyor, kalk bir bardak su iç.",
            "Kaktüs değilsin, suya ihtiyacın var. Git doldur bardağını.",
        ],
        "Motivasyonel": [
            "Bir bardak su iç, bedenin ve zihnin anında tazelensin!",
        ],
    },
    ("temizl", "topla", "oda", "çamaşır", "bulaşık", "düzen"): {
        "Sert & Direkt": [
            "Temizlik yapacaktın, etraf kendini toplamayacak. Başla.",
            "Dağınıklık arttıkça motivasyon düşer. Hemen toparla.",
        ],
        "Alaycı & Esprili": [
            "Temizlik perileri gelmeyecek, odayı sen toplayacaksın.",
            "Etraf o kadar karışık ki yeni bir medeniyet doğabilir.",
        ],
        "Motivasyonel": [
            "Temiz ve düzenli bir alan, huzurlu bir zihin demektir. 10 dakikanı ayır!",
        ],
    },
    ("yaz", "not", "günlük", "blog", "yazı"): {
        "Sert & Direkt": [
            "Yazma hedefin vardı, bir kelime bile yazmadın. Aç ve yaz.",
            "Yazı kendini yazmaz. Otur ve ilk cümleyi kur.",
        ],
        "Alaycı & Esprili": [
            "İlhamın gökten düşmesini mi bekliyorsun? Yazmaya başla gelir.",
            "Boş sayfa sana bakıyor sen sayfaya... Yaz artık bir şeyler.",
        ],
        "Motivasyonel": [
            "Her büyük eser tek bir cümleyle başladı. Bugün o cümleyi yaz!",
        ],
    },
}

# Genel fallback mesajları (bağlam bulunamazsa)
GENERAL_MESSAGES = {
    "Sert & Direkt": [
        "Bugün '{task}' için bir şey yapmadın. Ertelemenin sonu yok, başla.",
        "'{task}' hâlâ bekliyor. Ne zaman halledeceksin?",
        "'{task}' görevi kendi kendine bitmeyecek. Şimdi harekete geç.",
        "{days_info} Bugünü sakın kaçırma.",
        "Yarın yaparım demeyi bırak, '{task}' şimdi yapılacak.",
    ],
    "Alaycı & Esprili": [
        "'{task}' görevini yine atlayıp geçtin, tebrikler rekor kırıyorsun.",
        "'{task}' seni beklemekten bıktı ama sen rahatına bak tabii.",
        "Bugün de '{task}' yapılmadı, şaşırdık mı? Tabii ki hayır.",
        "'{task}' görevine gerçek bir sahip arıyoruz, ilgilenen?",
        "{days_info} Hâlâ bekliyor, komik değil mi?",
    ],
    "Motivasyonel": [
        "'{task}' için bugün küçük bir adım at, büyük fark yaratır!",
        "Hadi! '{task}' görevini bitirdiğinde ne kadar iyi hissedeceğini düşün.",
        "Bugün '{task}' için 5 dakika bile ayırsan ilerleme kaydedersin!",
        "'{task}' seni bekliyor. Başlamak bitimenin yarısıdır!",
        "Disiplin motivasyondan güçlüdür. '{task}' şimdi yap, sonra rahatla!",
    ],
}


def tr_lower(text):
    """Türkçe İ/I, Ş, Ğ, Ü, Ö, Ç karakterlerini doğru ve uyumlu küçük harfe dönüştürür."""
    if not text:
        return ""
    mapping = {
        "İ": "i", "I": "ı", "Ş": "ş", "Ğ": "ğ",
        "Ü": "ü", "Ö": "ö", "Ç": "ç"
    }
    for upper_c, lower_c in mapping.items():
        text = text.replace(upper_c, lower_c)
    return text.lower()


def query_ollama(model_name, prompt):
    """Ollama API veya CLI üzerinden hızlıca yanıt alır."""
    # 1. HTTP API (Ollama servisi çalışıyorsa en hızlı ve güvenli yol)
    try:
        url = "http://127.0.0.1:11434/api/generate"
        payload = json.dumps({
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.85, "num_predict": 75}
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=20.0) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            res = data.get("response", "").strip()
            if res:
                return res
    except Exception as e:
        print(f"Ollama HTTP hatası: {e}")

    # 2. Doğrudan CLI Fallback
    try:
        flags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
        res = subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True, text=True, timeout=20, encoding='utf-8',
            creationflags=flags
        )
        if res.stdout and res.stdout.strip():
            return res.stdout.strip()
    except Exception as e:
        print(f"Ollama CLI hatası: {e}")

    return None


def query_lm_studio(model_name, prompt):
    """LM Studio API'sine istek atar."""
    try:
        url = "http://127.0.0.1:1234/v1/chat/completions"
        payload = json.dumps({
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 75,
            "temperature": 0.85
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=20.0) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            res = data["choices"][0]["message"]["content"].strip()
            if res:
                return res
    except Exception as e:
        print(f"LM Studio API hatası: {e}")
    return None


def query_gemini(api_key, model_name, prompt):
    """Google Gemini REST API'sine (gemini-1.5-flash / gemini-2.0-flash) istek atar."""
    if not api_key or not api_key.strip():
        return None
    try:
        endpoint_model = "gemini-1.5-flash"
        if "2.0" in model_name:
            endpoint_model = "gemini-2.0-flash"
        elif "pro" in model_name.lower():
            endpoint_model = "gemini-1.5-pro"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{endpoint_model}:generateContent?key={api_key.strip()}"
        payload = json.dumps({
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.85,
                "maxOutputTokens": 100
            }
        }).encode('utf-8')

        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            candidates = data.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip()
    except Exception as e:
        print(f"Gemini API Hatası: {e}")
    return None


def _find_task_context(task_name):
    """Görev adındaki anahtar kelimeleri Türkçe harf uyumlu analiz edip bağlamsal mesaj havuzunu bulur."""
    task_clean = tr_lower(task_name)
    for keywords, messages in TASK_CONTEXT_MESSAGES.items():
        if any(tr_lower(kw) in task_clean for kw in keywords):
            return messages
    return None


def generate_ai_roast(task_name, days_missed=0, personality="Sert & Direkt", model_choice="", custom_prompt=""):
    """Seçilen AI modeli veya akıllı dahili motor ile görev-bağlamsal Türkçe hatırlatma üretir."""
    days_info = f"{days_missed} gündür '{task_name}' yapılmıyor!" if days_missed > 1 else f"Bugün '{task_name}' hâlâ yapılmadı!"
    streak_info = "Yine zinciri kırdın!" if days_missed > 1 else "Günün bitmesine az kaldı!"
    timing_desc = f"{days_missed} gündür aksatılıyor" if days_missed > 1 else "bugün henüz yapılmadı"

    # 0. Google Gemini Bulut Modeli
    if model_choice.startswith("Google Gemini"):
        api_key = ""
        if hasattr(HabitTrackerApp, "CURRENT_INSTANCE") and HabitTrackerApp.CURRENT_INSTANCE:
            api_key = HabitTrackerApp.CURRENT_INSTANCE.settings.get("gemini_api_key", "")
        if api_key:
            system_style = custom_prompt if (personality == "Özel" and custom_prompt) else {
                "Sert & Direkt": "Sen sert, direkt ve net konuşan bir Türkçe görev takip koçusun. Görevi anla ve kullanıcıya özel kısa (tek cümle), vurucu ve harekete geçirici bir hatırlatma yap.",
                "Alaycı & Esprili": "Sen esprili, iğneleyici ve hafif alaycı bir Türkçe görev takip asistanısın. Görevi anla ve kullanıcıya komik, laf sokan ama tatlı tek cümlelik bir hatırlatma yap.",
                "Motivasyonel": "Sen pozitif, motive edici bir Türkçe yaşam koçusun. Görevi anla ve kullanıcıya tek cümlelik cesaretlendirici, ilham verici bir mesaj yaz."
            }.get(personality, "Kısa ve net bir görev hatırlatması yap.")

            prompt = f"{system_style}\n\nGörev: '{task_name}'. Bu görev {timing_desc}. Kullanıcıya hitaben doğal, samimi ve Türkçe tek bir kısa cümle yaz (tırnak işareti olmadan):"
            res = query_gemini(api_key, model_choice, prompt)
            if res:
                return res.strip('"').strip("'").strip()

    # 1. Ollama modeli
    elif model_choice.startswith("[Ollama] "):
        m_name = model_choice.replace("[Ollama] ", "").strip()
        system_style = custom_prompt if (personality == "Özel" and custom_prompt) else {
            "Sert & Direkt": "Sen sert, direkt ve net konuşan bir Türkçe görev takip asistanısın. Görevin ne olduğunu anla ve ona özel kısa, vurucu bir hatırlatma yap.",
            "Alaycı & Esprili": "Sen alaycı, esprili ve iğneleyici bir Türkçe görev takip asistanısın. Görevin ne olduğunu anla ve ona özel komik, laf sokan bir hatırlatma yap.",
            "Motivasyonel": "Sen pozitif, motive edici bir Türkçe görev takip asistanısın. Görevin ne olduğunu anla ve ona özel cesaretlendirici bir mesaj yaz."
        }.get(personality, "Kısa ve net bir görev hatırlatması yap.")

        prompt = f"{system_style}\nGörev: '{task_name}'. Bu görev {timing_desc}. Bu göreve özel, doğal ve samimi tek cümlelik Türkçe bir hatırlatma yaz:"
        res = query_ollama(m_name, prompt)
        if res:
            return res.strip('"').strip("'")

    # 2. LM Studio modeli
    elif model_choice.startswith("[LM Studio] "):
        m_name = model_choice.replace("[LM Studio] ", "").strip()
        system_style = custom_prompt if (personality == "Özel" and custom_prompt) else "Sen görev hatırlatma yapan bir Türkçe AI asistanısın. Görevi anla ve ona özel doğal bir hatırlatma yaz."
        prompt = f"{system_style}\nGörev: '{task_name}'. Bu görev {timing_desc}. Bu göreve özel tek cümlelik doğal bir hatırlatma yaz:"
        res = query_lm_studio(m_name, prompt)
        if res:
            return res.strip('"').strip("'")

    # 3. Akıllı Dahili Motor (Görev bağlamı anlayan)
    if personality == "Özel" and custom_prompt:
        return f"{custom_prompt.strip()} ('{task_name}' görevi hala bekliyor!)"

    # Görev adından bağlam bul
    context_pool = _find_task_context(task_name)
    if context_pool and personality in context_pool:
        return random.choice(context_pool[personality])

    # Genel havuzdan seç
    pool = GENERAL_MESSAGES.get(personality, GENERAL_MESSAGES["Sert & Direkt"])
    msg = random.choice(pool)
    return msg.format(task=task_name, days_info=days_info, streak_info=streak_info)


def draw_round_rect(canvas, x1, y1, x2, y2, r=4, **kwargs):
    """Tkinter Canvas üzerinde pürüzsüz ve yuvarlak köşeli kutu/hap çizer."""
    points = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


# ============================================================
#  TEMA TANIMLARI (10 Zengin Pastel Light + 10 Modern Aesthetic Dark)
# ============================================================
THEMES = {
    "light": {
        "Matcha & Adaçayı": {
            "bg": "#EFECE6", "card": "#F7F5F0", "card_alt": "#EDE9E1",
            "today_col": "#DEE8DF", "today_header": "#4D7A56",
            "weekend_col": "#F4EDE8", "done": "#84B082",
            "checkbox_bg": "#F7F5F0", "checkbox_border": "#C5D6C5",
            "moral_color": "#D98A48", "efektiflik_color": "#957DC7",
            "accent": "#C96868", "text": "#243026", "text_secondary": "#637065",
            "separator": "#DCD7CC", "header_text": "#38523E",
            "chart_bg": "#F7F5F0", "chart_bar1": "#A2C5A1", "chart_bar2": "#84B082",
            "chart_pie_done": "#84B082", "chart_pie_remain": "#DCD7CC",
            "chart_text": "#243026", "chart_grid": "#E4E0D7",
            "btn_primary": "#B0D2AF", "btn_primary_hover": "#92BF91",
            "btn_danger": "#E89A9A", "btn_danger_hover": "#DB7E7E",
            "btn_settings": "#E8C9A3", "btn_settings_hover": "#DBB585",
            "entry_bg": "#F7F5F0", "entry_border": "#C5D6C5",
            "progress_bg": "#DCD7CC", "progress_fg": "#84B082",
            "switch_on": "#84B082", "switch_off": "#DCD7CC",
            "switch_btn": "#F7F5F0", "switch_btn_hover": "#FFFFFF",
        },
        "Latte & Şeftali": {
            "bg": "#F5EBE1", "card": "#FAF3EC", "card_alt": "#EFE2D5",
            "today_col": "#FDE2D2", "today_header": "#D96B43",
            "weekend_col": "#F8E7DF", "done": "#EFA07A",
            "checkbox_bg": "#FAF3EC", "checkbox_border": "#E5C4B0",
            "moral_color": "#D96B43", "efektiflik_color": "#9D79B2",
            "accent": "#D96B43", "text": "#36281F", "text_secondary": "#7A665A",
            "separator": "#E5D3C3", "header_text": "#593E2F",
            "chart_bg": "#FAF3EC", "chart_bar1": "#F6BC9B", "chart_bar2": "#EFA07A",
            "chart_pie_done": "#EFA07A", "chart_pie_remain": "#E5D3C3",
            "chart_text": "#36281F", "chart_grid": "#EDE0D4",
            "btn_primary": "#F4B392", "btn_primary_hover": "#EC9970",
            "btn_danger": "#E89A9A", "btn_danger_hover": "#DB7E7E",
            "btn_settings": "#E8C9A3", "btn_settings_hover": "#DBB585",
            "entry_bg": "#FAF3EC", "entry_border": "#E5C4B0",
            "progress_bg": "#E5D3C3", "progress_fg": "#EFA07A",
            "switch_on": "#EFA07A", "switch_off": "#E5D3C3",
            "switch_btn": "#FAF3EC", "switch_btn_hover": "#FFFFFF",
        },
        "Lavanta Rüyası": {
            "bg": "#EFE9F7", "card": "#F6F2FC", "card_alt": "#E8E0F3",
            "today_col": "#E2D6F5", "today_header": "#7B52BE",
            "weekend_col": "#F3E8F5", "done": "#A98CDE",
            "checkbox_bg": "#F6F2FC", "checkbox_border": "#D2C0EC",
            "moral_color": "#E5914E", "efektiflik_color": "#7B52BE",
            "accent": "#D86289", "text": "#2B203B", "text_secondary": "#695B7E",
            "separator": "#DDD2EE", "header_text": "#49326A",
            "chart_bg": "#F6F2FC", "chart_bar1": "#C6B2EC", "chart_bar2": "#A98CDE",
            "chart_pie_done": "#A98CDE", "chart_pie_remain": "#DDD2EE",
            "chart_text": "#2B203B", "chart_grid": "#E4DBF2",
            "btn_primary": "#BEA4EA", "btn_primary_hover": "#A583DF",
            "btn_danger": "#E89A9A", "btn_danger_hover": "#DB7E7E",
            "btn_settings": "#E8C9A3", "btn_settings_hover": "#DBB585",
            "entry_bg": "#F6F2FC", "entry_border": "#D2C0EC",
            "progress_bg": "#DDD2EE", "progress_fg": "#A98CDE",
            "switch_on": "#A98CDE", "switch_off": "#DDD2EE",
            "switch_btn": "#F6F2FC", "switch_btn_hover": "#FFFFFF",
        },
        "Okyanus Esintisi": {
            "bg": "#E4F0F6", "card": "#EFF7FB", "card_alt": "#DBEBF3",
            "today_col": "#CDE7F5", "today_header": "#1E7EA7",
            "weekend_col": "#EBF3F8", "done": "#48B8AC",
            "checkbox_bg": "#EFF7FB", "checkbox_border": "#B6D8E8",
            "moral_color": "#DE8E48", "efektiflik_color": "#7E6DB8",
            "accent": "#E26868", "text": "#182835", "text_secondary": "#516A7E",
            "separator": "#CFE2ED", "header_text": "#1A536F",
            "chart_bg": "#EFF7FB", "chart_bar1": "#7DC1E2", "chart_bar2": "#48B8AC",
            "chart_pie_done": "#48B8AC", "chart_pie_remain": "#CFE2ED",
            "chart_text": "#182835", "chart_grid": "#D6E7F0",
            "btn_primary": "#6CBDE0", "btn_primary_hover": "#4EAECF",
            "btn_danger": "#E89A9A", "btn_danger_hover": "#DB7E7E",
            "btn_settings": "#E8C9A3", "btn_settings_hover": "#DBB585",
            "entry_bg": "#EFF7FB", "entry_border": "#B6D8E8",
            "progress_bg": "#CFE2ED", "progress_fg": "#48B8AC",
            "switch_on": "#48B8AC", "switch_off": "#CFE2ED",
            "switch_btn": "#EFF7FB", "switch_btn_hover": "#FFFFFF",
        },
        "Sakura & Gül": {
            "bg": "#F9EBF0", "card": "#FCF3F6", "card_alt": "#F4DFE7",
            "today_col": "#F9D6E3", "today_header": "#CB4576",
            "weekend_col": "#FAEDF2", "done": "#EA7EA4",
            "checkbox_bg": "#FCF3F6", "checkbox_border": "#F0C2D3",
            "moral_color": "#DC7D47", "efektiflik_color": "#9368B8",
            "accent": "#CB4576", "text": "#351E28", "text_secondary": "#775163",
            "separator": "#EDD0DC", "header_text": "#6A2640",
            "chart_bg": "#FCF3F6", "chart_bar1": "#F2A1BE", "chart_bar2": "#EA7EA4",
            "chart_pie_done": "#EA7EA4", "chart_pie_remain": "#EDD0DC",
            "chart_text": "#351E28", "chart_grid": "#F3DCE5",
            "btn_primary": "#EE94B4", "btn_primary_hover": "#E3739B",
            "btn_danger": "#E89A9A", "btn_danger_hover": "#DB7E7E",
            "btn_settings": "#E8C9A3", "btn_settings_hover": "#DBB585",
            "entry_bg": "#FCF3F6", "entry_border": "#F0C2D3",
            "progress_bg": "#EDD0DC", "progress_fg": "#EA7EA4",
            "switch_on": "#EA7EA4", "switch_off": "#EDD0DC",
            "switch_btn": "#FCF3F6", "switch_btn_hover": "#FFFFFF",
        },
        "Retro Kağıt & Sepya": {
            "bg": "#F5EFEB", "card": "#FAF7F2", "card_alt": "#EBE3D9",
            "today_col": "#DFD4C5", "today_header": "#8C6239",
            "weekend_col": "#F0E8DD", "done": "#C89666",
            "checkbox_bg": "#FAF7F2", "checkbox_border": "#D2C3B2",
            "moral_color": "#C87D55", "efektiflik_color": "#7A6C9B",
            "accent": "#A45D5D", "text": "#2B2621", "text_secondary": "#6E6257",
            "separator": "#DDD2C4", "header_text": "#5C4033",
            "chart_bg": "#FAF7F2", "chart_bar1": "#DDB995", "chart_bar2": "#C89666",
            "chart_pie_done": "#C89666", "chart_pie_remain": "#DDD2C4",
            "chart_text": "#2B2621", "chart_grid": "#E6DCD0",
            "btn_primary": "#D4A373", "btn_primary_hover": "#C08A58",
            "btn_danger": "#E89A9A", "btn_danger_hover": "#DB7E7E",
            "btn_settings": "#D4A373", "btn_settings_hover": "#C08A58",
            "entry_bg": "#FAF7F2", "entry_border": "#D2C3B2",
            "progress_bg": "#DDD2C4", "progress_fg": "#C89666",
            "switch_on": "#C89666", "switch_off": "#DDD2C4",
            "switch_btn": "#FAF7F2", "switch_btn_hover": "#FFFFFF",
        },
        "Nordik Kar & Sis": {
            "bg": "#F1F5F9", "card": "#FFFFFF", "card_alt": "#E2E8F0",
            "today_col": "#CBD5E1", "today_header": "#0369A1",
            "weekend_col": "#EAEFF5", "done": "#0284C7",
            "checkbox_bg": "#FFFFFF", "checkbox_border": "#94A3B8",
            "moral_color": "#F59E0B", "efektiflik_color": "#8B5CF6",
            "accent": "#EF4444", "text": "#0F172A", "text_secondary": "#475569",
            "separator": "#CBD5E1", "header_text": "#0369A1",
            "chart_bg": "#FFFFFF", "chart_bar1": "#38BDF8", "chart_bar2": "#0284C7",
            "chart_pie_done": "#0284C7", "chart_pie_remain": "#CBD5E1",
            "chart_text": "#0F172A", "chart_grid": "#E2E8F0",
            "btn_primary": "#38BDF8", "btn_primary_hover": "#0284C7",
            "btn_danger": "#F87171", "btn_danger_hover": "#EF4444",
            "btn_settings": "#F59E0B", "btn_settings_hover": "#D97706",
            "entry_bg": "#FFFFFF", "entry_border": "#94A3B8",
            "progress_bg": "#CBD5E1", "progress_fg": "#0284C7",
            "switch_on": "#0284C7", "switch_off": "#CBD5E1",
            "switch_btn": "#FFFFFF", "switch_btn_hover": "#F8FAFC",
        },
        "Güneş Işığı & Papatya": {
            "bg": "#FCF9EE", "card": "#FFFCF5", "card_alt": "#F5EFCF",
            "today_col": "#FDEAA8", "today_header": "#B45309",
            "weekend_col": "#FAF4DC", "done": "#E5A93C",
            "checkbox_bg": "#FFFCF5", "checkbox_border": "#E8D49E",
            "moral_color": "#D97706", "efektiflik_color": "#8C6BC1",
            "accent": "#E05353", "text": "#382B15", "text_secondary": "#786548",
            "separator": "#ECE0BA", "header_text": "#78350F",
            "chart_bg": "#FFFCF5", "chart_bar1": "#F8C76A", "chart_bar2": "#E5A93C",
            "chart_pie_done": "#E5A93C", "chart_pie_remain": "#ECE0BA",
            "chart_text": "#382B15", "chart_grid": "#F3E7C9",
            "btn_primary": "#F5BE58", "btn_primary_hover": "#E5A93C",
            "btn_danger": "#E89A9A", "btn_danger_hover": "#DB7E7E",
            "btn_settings": "#F5BE58", "btn_settings_hover": "#E5A93C",
            "entry_bg": "#FFFCF5", "entry_border": "#E8D49E",
            "progress_bg": "#ECE0BA", "progress_fg": "#E5A93C",
            "switch_on": "#E5A93C", "switch_off": "#ECE0BA",
            "switch_btn": "#FFFCF5", "switch_btn_hover": "#FFFFFF",
        },
        "Nane & Ferah Okaliptüs": {
            "bg": "#E8F5F1", "card": "#F3FAF7", "card_alt": "#DAEEE7",
            "today_col": "#C5E6DC", "today_header": "#0F766E",
            "weekend_col": "#E2F1EC", "done": "#14B8A6",
            "checkbox_bg": "#F3FAF7", "checkbox_border": "#A7D7CB",
            "moral_color": "#E67E22", "efektiflik_color": "#7C5AC2",
            "accent": "#E74C3C", "text": "#13352F", "text_secondary": "#4D736C",
            "separator": "#C4E5DB", "header_text": "#115E59",
            "chart_bg": "#F3FAF7", "chart_bar1": "#5EEAD4", "chart_bar2": "#14B8A6",
            "chart_pie_done": "#14B8A6", "chart_pie_remain": "#C4E5DB",
            "chart_text": "#13352F", "chart_grid": "#D2ECE4",
            "btn_primary": "#2DD4BF", "btn_primary_hover": "#0D9488",
            "btn_danger": "#E89A9A", "btn_danger_hover": "#DB7E7E",
            "btn_settings": "#E8C9A3", "btn_settings_hover": "#DBB585",
            "entry_bg": "#F3FAF7", "entry_border": "#A7D7CB",
            "progress_bg": "#C4E5DB", "progress_fg": "#14B8A6",
            "switch_on": "#14B8A6", "switch_off": "#C4E5DB",
            "switch_btn": "#F3FAF7", "switch_btn_hover": "#FFFFFF",
        },
        "Pastel Günbatımı": {
            "bg": "#FDF0EE", "card": "#FFF7F5", "card_alt": "#F8E2DE",
            "today_col": "#F9D0C8", "today_header": "#C2410C",
            "weekend_col": "#FAECE9", "done": "#F97316",
            "checkbox_bg": "#FFF7F5", "checkbox_border": "#E8B9AF",
            "moral_color": "#D97706", "efektiflik_color": "#9333EA",
            "accent": "#E11D48", "text": "#381D1A", "text_secondary": "#7C504A",
            "separator": "#EED0C9", "header_text": "#9A3412",
            "chart_bg": "#FFF7F5", "chart_bar1": "#FB923C", "chart_bar2": "#F97316",
            "chart_pie_done": "#F97316", "chart_pie_remain": "#EED0C9",
            "chart_text": "#381D1A", "chart_grid": "#F5DDD8",
            "btn_primary": "#FB923C", "btn_primary_hover": "#EA580C",
            "btn_danger": "#E89A9A", "btn_danger_hover": "#DB7E7E",
            "btn_settings": "#FB923C", "btn_settings_hover": "#EA580C",
            "entry_bg": "#FFF7F5", "entry_border": "#E8B9AF",
            "progress_bg": "#EED0C9", "progress_fg": "#F97316",
            "switch_on": "#F97316", "switch_off": "#EED0C9",
            "switch_btn": "#FFF7F5", "switch_btn_hover": "#FFFFFF",
        },
    },
    "dark": {
        "Gece Yarısı": {
            "bg": "#0B1120", "card": "#1E293B", "card_alt": "#162032",
            "today_col": "#1E3A5F", "today_header": "#38BDF8",
            "weekend_col": "#161F30", "done": "#38BDF8",
            "checkbox_bg": "#1E293B", "checkbox_border": "#334155",
            "moral_color": "#FBBF24", "efektiflik_color": "#C084FC",
            "accent": "#FB7185", "text": "#F8FAFC", "text_secondary": "#94A3B8",
            "separator": "#334155", "header_text": "#38BDF8",
            "chart_bg": "#1E293B", "chart_bar1": "#38BDF8", "chart_bar2": "#38BDF8",
            "chart_pie_done": "#38BDF8", "chart_pie_remain": "#334155",
            "chart_text": "#F8FAFC", "chart_grid": "#334155",
            "btn_primary": "#0284C7", "btn_primary_hover": "#0369A1",
            "btn_danger": "#E11D48", "btn_danger_hover": "#BE123C",
            "btn_settings": "#D97706", "btn_settings_hover": "#B45309",
            "entry_bg": "#0F172A", "entry_border": "#334155",
            "progress_bg": "#334155", "progress_fg": "#38BDF8",
            "switch_on": "#0284C7", "switch_off": "#334155",
            "switch_btn": "#F8FAFC", "switch_btn_hover": "#FFFFFF",
        },
        "Karanlık Karbon": {
            "bg": "#121214", "card": "#1C1C20", "card_alt": "#17171A",
            "today_col": "#2A303C", "today_header": "#60A5FA",
            "weekend_col": "#19191C", "done": "#60A5FA",
            "checkbox_bg": "#1C1C20", "checkbox_border": "#2E2E35",
            "moral_color": "#FB923C", "efektiflik_color": "#A78BFA",
            "accent": "#F87171", "text": "#F4F4F5", "text_secondary": "#A1A1AA",
            "separator": "#2E2E35", "header_text": "#60A5FA",
            "chart_bg": "#1C1C20", "chart_bar1": "#60A5FA", "chart_bar2": "#60A5FA",
            "chart_pie_done": "#60A5FA", "chart_pie_remain": "#2E2E35",
            "chart_text": "#F4F4F5", "chart_grid": "#2E2E35",
            "btn_primary": "#3B82F6", "btn_primary_hover": "#2563EB",
            "btn_danger": "#EF4444", "btn_danger_hover": "#DC2626",
            "btn_settings": "#F97316", "btn_settings_hover": "#EA580C",
            "entry_bg": "#121214", "entry_border": "#2E2E35",
            "progress_bg": "#2E2E35", "progress_fg": "#60A5FA",
            "switch_on": "#3B82F6", "switch_off": "#2E2E35",
            "switch_btn": "#F4F4F5", "switch_btn_hover": "#FFFFFF",
        },
        "Kuzey Ormanı": {
            "bg": "#0B1510", "card": "#14251C", "card_alt": "#101D16",
            "today_col": "#1E3B2C", "today_header": "#5EEAD4",
            "weekend_col": "#122018", "done": "#4EBA6F",
            "checkbox_bg": "#14251C", "checkbox_border": "#233F30",
            "moral_color": "#F59E0B", "efektiflik_color": "#C084FC",
            "accent": "#F87171", "text": "#ECFDF5", "text_secondary": "#86EFAC",
            "separator": "#233F30", "header_text": "#5EEAD4",
            "chart_bg": "#14251C", "chart_bar1": "#5EEAD4", "chart_bar2": "#4EBA6F",
            "chart_pie_done": "#4EBA6F", "chart_pie_remain": "#233F30",
            "chart_text": "#ECFDF5", "chart_grid": "#233F30",
            "btn_primary": "#059669", "btn_primary_hover": "#047857",
            "btn_danger": "#EF4444", "btn_danger_hover": "#DC2626",
            "btn_settings": "#D97706", "btn_settings_hover": "#B45309",
            "entry_bg": "#0B1510", "entry_border": "#233F30",
            "progress_bg": "#233F30", "progress_fg": "#4EBA6F",
            "switch_on": "#059669", "switch_off": "#233F30",
            "switch_btn": "#ECFDF5", "switch_btn_hover": "#FFFFFF",
        },
        "Espresso & Moka": {
            "bg": "#140F0D", "card": "#211815", "card_alt": "#1B1310",
            "today_col": "#38251E", "today_header": "#F6AD55",
            "weekend_col": "#1D1512", "done": "#E07A5F",
            "checkbox_bg": "#211815", "checkbox_border": "#3B2A24",
            "moral_color": "#F6AD55", "efektiflik_color": "#D6BCFA",
            "accent": "#FEB2B2", "text": "#FAF5F0", "text_secondary": "#BCAAA4",
            "separator": "#3B2A24", "header_text": "#F6AD55",
            "chart_bg": "#211815", "chart_bar1": "#F6AD55", "chart_bar2": "#E07A5F",
            "chart_pie_done": "#E07A5F", "chart_pie_remain": "#3B2A24",
            "chart_text": "#FAF5F0", "chart_grid": "#3B2A24",
            "btn_primary": "#C05621", "btn_primary_hover": "#9C4221",
            "btn_danger": "#E53E3E", "btn_danger_hover": "#C53030",
            "btn_settings": "#D69E2E", "btn_settings_hover": "#B7791F",
            "entry_bg": "#140F0D", "entry_border": "#3B2A24",
            "progress_bg": "#3B2A24", "progress_fg": "#E07A5F",
            "switch_on": "#C05621", "switch_off": "#3B2A24",
            "switch_btn": "#FAF5F0", "switch_btn_hover": "#FFFFFF",
        },
        "Karanlık Ametist": {
            "bg": "#0F0B18", "card": "#1A132B", "card_alt": "#140F22",
            "today_col": "#2D1D4A", "today_header": "#C084FC",
            "weekend_col": "#161025", "done": "#A855F7",
            "checkbox_bg": "#1A132B", "checkbox_border": "#312351",
            "moral_color": "#FBBF24", "efektiflik_color": "#E879F9",
            "accent": "#F472B6", "text": "#F5F3FF", "text_secondary": "#A78BFA",
            "separator": "#312351", "header_text": "#C084FC",
            "chart_bg": "#1A132B", "chart_bar1": "#C084FC", "chart_bar2": "#A855F7",
            "chart_pie_done": "#A855F7", "chart_pie_remain": "#312351",
            "chart_text": "#F5F3FF", "chart_grid": "#312351",
            "btn_primary": "#7C3AED", "btn_primary_hover": "#6D28D9",
            "btn_danger": "#E11D48", "btn_danger_hover": "#BE123C",
            "btn_settings": "#D97706", "btn_settings_hover": "#B45309",
            "entry_bg": "#0F0B18", "entry_border": "#312351",
            "progress_bg": "#312351", "progress_fg": "#A855F7",
            "switch_on": "#7C3AED", "switch_off": "#312351",
            "switch_btn": "#F5F3FF", "switch_btn_hover": "#FFFFFF",
        },
        "Cyberpunk Neon & Tokyo": {
            "bg": "#080811", "card": "#121124", "card_alt": "#0E0D1C",
            "today_col": "#25123A", "today_header": "#F43F5E",
            "weekend_col": "#0D0C1A", "done": "#06B6D4",
            "checkbox_bg": "#121124", "checkbox_border": "#2D2852",
            "moral_color": "#F59E0B", "efektiflik_color": "#C084FC",
            "accent": "#F43F5E", "text": "#F8FAFC", "text_secondary": "#94A3B8",
            "separator": "#2D2852", "header_text": "#06B6D4",
            "chart_bg": "#121124", "chart_bar1": "#F43F5E", "chart_bar2": "#06B6D4",
            "chart_pie_done": "#06B6D4", "chart_pie_remain": "#2D2852",
            "chart_text": "#F8FAFC", "chart_grid": "#2D2852",
            "btn_primary": "#E11D48", "btn_primary_hover": "#BE123C",
            "btn_danger": "#EF4444", "btn_danger_hover": "#DC2626",
            "btn_settings": "#06B6D4", "btn_settings_hover": "#0891B2",
            "entry_bg": "#080811", "entry_border": "#2D2852",
            "progress_bg": "#2D2852", "progress_fg": "#06B6D4",
            "switch_on": "#E11D48", "switch_off": "#2D2852",
            "switch_btn": "#F8FAFC", "switch_btn_hover": "#FFFFFF",
        },
        "Dracula & Vampir": {
            "bg": "#1E1F29", "card": "#282A36", "card_alt": "#21222C",
            "today_col": "#3A3C4E", "today_header": "#BD93F9",
            "weekend_col": "#242531", "done": "#50FA7B",
            "checkbox_bg": "#282A36", "checkbox_border": "#44475A",
            "moral_color": "#FFB86C", "efektiflik_color": "#FF79C6",
            "accent": "#FF5555", "text": "#F8F8F2", "text_secondary": "#6272A4",
            "separator": "#44475A", "header_text": "#BD93F9",
            "chart_bg": "#282A36", "chart_bar1": "#BD93F9", "chart_bar2": "#50FA7B",
            "chart_pie_done": "#50FA7B", "chart_pie_remain": "#44475A",
            "chart_text": "#F8F8F2", "chart_grid": "#44475A",
            "btn_primary": "#BD93F9", "btn_primary_hover": "#A776F6",
            "btn_danger": "#FF5555", "btn_danger_hover": "#E04040",
            "btn_settings": "#FFB86C", "btn_settings_hover": "#F1A04B",
            "entry_bg": "#1E1F29", "entry_border": "#44475A",
            "progress_bg": "#44475A", "progress_fg": "#50FA7B",
            "switch_on": "#BD93F9", "switch_off": "#44475A",
            "switch_btn": "#F8F8F2", "switch_btn_hover": "#FFFFFF",
        },
        "Nordik Fiyort & Gece": {
            "bg": "#0B132B", "card": "#1C2541", "card_alt": "#151C33",
            "today_col": "#2A3D66", "today_header": "#48CAE4",
            "weekend_col": "#17203B", "done": "#00F5D4",
            "checkbox_bg": "#1C2541", "checkbox_border": "#3A506B",
            "moral_color": "#F77F00", "efektiflik_color": "#9D4EDD",
            "accent": "#FF0054", "text": "#E0FBFC", "text_secondary": "#8DA9C4",
            "separator": "#3A506B", "header_text": "#48CAE4",
            "chart_bg": "#1C2541", "chart_bar1": "#48CAE4", "chart_bar2": "#00F5D4",
            "chart_pie_done": "#00F5D4", "chart_pie_remain": "#3A506B",
            "chart_text": "#E0FBFC", "chart_grid": "#3A506B",
            "btn_primary": "#00B4D8", "btn_primary_hover": "#0096C7",
            "btn_danger": "#E63946", "btn_danger_hover": "#D62828",
            "btn_settings": "#F77F00", "btn_settings_hover": "#D66B00",
            "entry_bg": "#0B132B", "entry_border": "#3A506B",
            "progress_bg": "#3A506B", "progress_fg": "#00F5D4",
            "switch_on": "#00B4D8", "switch_off": "#3A506B",
            "switch_btn": "#E0FBFC", "switch_btn_hover": "#FFFFFF",
        },
        "Retro Synthwave 80s": {
            "bg": "#13091F", "card": "#201235", "card_alt": "#190E2B",
            "today_col": "#381D5E", "today_header": "#EC4899",
            "weekend_col": "#1B0E2E", "done": "#F43F5E",
            "checkbox_bg": "#201235", "checkbox_border": "#4A2875",
            "moral_color": "#F97316", "efektiflik_color": "#A855F7",
            "accent": "#06B6D4", "text": "#FDF4FF", "text_secondary": "#D8B4FE",
            "separator": "#4A2875", "header_text": "#EC4899",
            "chart_bg": "#201235", "chart_bar1": "#EC4899", "chart_bar2": "#F43F5E",
            "chart_pie_done": "#F43F5E", "chart_pie_remain": "#4A2875",
            "chart_text": "#FDF4FF", "chart_grid": "#4A2875",
            "btn_primary": "#D946EF", "btn_primary_hover": "#C026D3",
            "btn_danger": "#EF4444", "btn_danger_hover": "#DC2626",
            "btn_settings": "#F97316", "btn_settings_hover": "#EA580C",
            "entry_bg": "#13091F", "entry_border": "#4A2875",
            "progress_bg": "#4A2875", "progress_fg": "#F43F5E",
            "switch_on": "#D946EF", "switch_off": "#4A2875",
            "switch_btn": "#FDF4FF", "switch_btn_hover": "#FFFFFF",
        },
        "Monokrom Mat Siyah": {
            "bg": "#000000", "card": "#121212", "card_alt": "#0A0A0A",
            "today_col": "#242424", "today_header": "#E4E4E7",
            "weekend_col": "#0F0F0F", "done": "#E4E4E7",
            "checkbox_bg": "#121212", "checkbox_border": "#3F3F46",
            "moral_color": "#E4E4E7", "efektiflik_color": "#A1A1AA",
            "accent": "#EF4444", "text": "#FAFAFA", "text_secondary": "#A1A1AA",
            "separator": "#27272A", "header_text": "#FAFAFA",
            "chart_bg": "#121212", "chart_bar1": "#71717A", "chart_bar2": "#D4D4D8",
            "chart_pie_done": "#D4D4D8", "chart_pie_remain": "#27272A",
            "chart_text": "#FAFAFA", "chart_grid": "#27272A",
            "btn_primary": "#3F3F46", "btn_primary_hover": "#52525B",
            "btn_danger": "#7F1D1D", "btn_danger_hover": "#991B1B",
            "btn_settings": "#3F3F46", "btn_settings_hover": "#52525B",
            "entry_bg": "#000000", "entry_border": "#3F3F46",
            "progress_bg": "#27272A", "progress_fg": "#D4D4D8",
            "switch_on": "#52525B", "switch_off": "#27272A",
            "switch_btn": "#FAFAFA", "switch_btn_hover": "#FFFFFF",
        },
    },
}


# ============================================================
#  BİLDİRİM POPUP (5 DK DARLAMA & DİNAMİK BUTONLAR)
# ============================================================
class NotificationPopup(ctk.CTkToplevel):
    def __init__(self, parent, task_name, message, theme, is_ai=True, personality="", snooze_count=0):
        super().__init__(parent)
        self.parent = parent
        self.task_name = task_name
        self.snooze_count = snooze_count

        is_dark = (self.parent.settings.get("mode", "light") == "dark") if hasattr(self.parent, "settings") else False
        is_error_style = (snooze_count >= 1)

        if is_error_style:
            # Gerçek Windows Hata Penceresi görünümü
            self.title("Windows - Sistem Uyarısı")
            # Sol üstteki tüm yapay simgeleri kaldırır, gerçek sistem diyalog başlığı yapar
            try:
                self.attributes("-toolwindow", True)
            except Exception:
                pass
            self.attributes("-topmost", True)
            self.resizable(False, False)

            popup_width = 460 if snooze_count >= 2 else 430
            popup_height = 165
            self.geometry(f"{popup_width}x{popup_height}")

            bg_main = "#202020" if is_dark else "#FFFFFF"
            bg_bar = "#2B2B2B" if is_dark else "#F0F0F0"
            text_head = "#FFFFFF" if is_dark else "#000000"
            text_body = "#CCCCCC" if is_dark else "#333333"
            btn_bg = "#333333" if is_dark else "#E1E1E1"
            btn_hover = "#444444" if is_dark else "#E5F1FB"
            btn_border = "#555555" if is_dark else "#ADADAD"
            btn_text = "#FFFFFF" if is_dark else "#000000"

            self.configure(fg_color=bg_main)
            self.protocol("WM_DELETE_WINDOW", self._on_snooze)

            self.update_idletasks()
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            cx = (sw - popup_width) // 2
            cy = (sh - popup_height) // 2
            quadrants = [
                (-220, -120), (220, -120),
                (-220, 120), (220, 120),
                (0, -140), (0, 140),
                (-240, 0), (240, 0)
            ]
            qx, qy = random.choice(quadrants)
            rand_x = qx + random.randint(-35, 35)
            rand_y = qy + random.randint(-25, 25)
            sx = max(40, min(sw - popup_width - 40, cx + rand_x))
            sy = max(40, min(sh - popup_height - 60, cy + rand_y))
            self.geometry(f"{popup_width}x{popup_height}+{sx}+{sy}")

            # Üst İçerik Alanı
            c_frame = ctk.CTkFrame(self, fg_color=bg_main, corner_radius=0)
            c_frame.pack(fill="both", expand=True, padx=16, pady=(16, 8))

            # Sol Kırmızı Hata İkonu (Canvas ile çizilen orijinal Windows Hata İkonu)
            canvas = tk.Canvas(c_frame, width=38, height=38, bg=bg_main, highlightthickness=0)
            canvas.pack(side="left", anchor="n", padx=(0, 14))
            canvas.create_oval(2, 2, 36, 36, fill="#E81123", outline="")
            canvas.create_line(12, 12, 26, 26, fill="#FFFFFF", width=3, capstyle="round")
            canvas.create_line(26, 12, 12, 26, fill="#FFFFFF", width=3, capstyle="round")

            # Sağ Metin Alanı
            t_frame = ctk.CTkFrame(c_frame, fg_color="transparent")
            t_frame.pack(side="left", fill="both", expand=True)

            ctk.CTkLabel(t_frame, text=f"'{task_name}' görevi ertelenmeye devam ediyor.",
                         font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                         text_color=text_head, anchor="w", justify="left").pack(fill="x", pady=(0, 4))

            ctk.CTkLabel(t_frame, text=message,
                         font=ctk.CTkFont(family="Segoe UI", size=10),
                         text_color=text_body, wraplength=popup_width - 90, justify="left", anchor="w").pack(fill="x")

            # Alt Windows Buton Çubuğu
            b_bar = ctk.CTkFrame(self, fg_color=bg_bar, height=44, corner_radius=0)
            b_bar.pack(fill="x", side="bottom")

            b_box = ctk.CTkFrame(b_bar, fg_color="transparent")
            b_box.pack(side="right", padx=12, pady=8)

            ctk.CTkButton(b_box, text="Tamam", width=80, height=25, corner_radius=3,
                          fg_color=btn_bg, hover_color=btn_hover, text_color=btn_text,
                          border_width=1, border_color=btn_border,
                          font=ctk.CTkFont(family="Segoe UI", size=10),
                          command=self._on_done).pack(side="left", padx=3)

            ctk.CTkButton(b_box, text="Sonra yaparım", width=95, height=25, corner_radius=3,
                          fg_color=btn_bg, hover_color=btn_hover, text_color=btn_text,
                          border_width=1, border_color=btn_border,
                          font=ctk.CTkFont(family="Segoe UI", size=10),
                          command=self._on_snooze).pack(side="left", padx=3)

            if snooze_count >= 2:
                ctk.CTkButton(b_box, text="Bugün Hatırlatma", width=115, height=25, corner_radius=3,
                              fg_color=btn_bg, hover_color=btn_hover, text_color=btn_text,
                              border_width=1, border_color=btn_border,
                              font=ctk.CTkFont(family="Segoe UI", size=10),
                              command=self._on_dismiss_today).pack(side="left", padx=3)

            try:
                winsound.MessageBeep(winsound.MB_ICONHAND)
            except Exception:
                pass

        else:
            # Standart Tema Görünümü (İlk Bildirim)
            if is_ai and personality:
                title_map = {
                    "Sert & Direkt": "⚡ Görev Uyarısı",
                    "Alaycı & Esprili": "😏 Görev Hatırlatma",
                    "Motivasyonel": "💪 Motivasyon",
                    "Özel": "📢 Bildirim",
                }
                win_title = title_map.get(personality, "📋 Görev Hatırlatma")
            elif is_ai:
                win_title = "📋 Görev Hatırlatma"
            else:
                win_title = "🔔 Hatırlatma"

            self.title(win_title)
            popup_width = 460 if snooze_count >= 2 else 430
            popup_height = 190
            self.geometry(f"{popup_width}x{popup_height}")
            self.resizable(False, False)
            self.attributes("-topmost", True)
            self.configure(fg_color=theme["bg"])
            self.protocol("WM_DELETE_WINDOW", self._on_snooze)

            self.update_idletasks()
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            cx = (sw - popup_width) // 2
            cy = (sh - popup_height) // 2
            quadrants = [
                (-220, -120), (220, -120),
                (-220, 120), (220, 120),
                (0, -140), (0, 140),
                (-240, 0), (240, 0)
            ]
            qx, qy = random.choice(quadrants)
            rand_x = qx + random.randint(-35, 35)
            rand_y = qy + random.randint(-25, 25)
            sx = max(40, min(sw - popup_width - 40, cx + rand_x))
            sy = max(40, min(sh - popup_height - 60, cy + rand_y))
            self.geometry(f"{popup_width}x{popup_height}+{sx}+{sy}")

            border_c = theme.get("accent", "#FB7185") if is_ai else theme["done"]
            frame = ctk.CTkFrame(self, fg_color=theme["card"], corner_radius=14,
                                 border_width=2, border_color=border_c)
            frame.pack(fill="both", expand=True, padx=6, pady=6)

            header_frame = ctk.CTkFrame(frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=14, pady=(10, 4))

            header_color = theme.get("accent", "#FB7185") if is_ai else theme["text"]
            ctk.CTkLabel(header_frame, text="📋  Görev Hatırlatma",
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=header_color).pack(side="left")

            task_badge = ctk.CTkFrame(header_frame, fg_color=theme["card_alt"], corner_radius=8)
            task_badge.pack(side="right")
            ctk.CTkLabel(task_badge, text=f"📌 {task_name}", font=ctk.CTkFont(size=10, weight="bold"),
                         text_color=theme["text"]).pack(padx=8, pady=2)

            ctk.CTkLabel(frame, text=message,
                         font=ctk.CTkFont(size=11),
                         text_color=theme["text"],
                         wraplength=popup_width - 50, justify="center").pack(fill="both", expand=True, padx=14, pady=(4, 8))

            btn_box = ctk.CTkFrame(frame, fg_color="transparent")
            btn_box.pack(fill="x", padx=12, pady=(0, 10))

            ctk.CTkButton(btn_box, text="✓ Tamam", height=28, corner_radius=10,
                          fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"],
                          text_color=theme["text"], font=ctk.CTkFont(size=11, weight="bold"),
                          command=self._on_done).pack(side="left", fill="x", expand=True, padx=3)

            ctk.CTkButton(btn_box, text="Sonra yaparım", height=28, corner_radius=10,
                          fg_color=theme["card_alt"], hover_color=theme["checkbox_border"],
                          text_color=theme["text"], font=ctk.CTkFont(size=11),
                          command=self._on_snooze).pack(side="left", fill="x", expand=True, padx=3)

            if snooze_count >= 2:
                ctk.CTkButton(btn_box, text="🚫 Bugün Hatırlatma", height=28, corner_radius=10,
                              fg_color=theme.get("btn_danger", "#EF4444"), hover_color=theme.get("btn_danger_hover", "#DC2626"),
                              text_color="#FFFFFF", font=ctk.CTkFont(size=10, weight="bold"),
                              command=self._on_dismiss_today).pack(side="left", fill="x", expand=True, padx=3)

            play_notification_sound()
            self.protocol("WM_DELETE_WINDOW", self._on_close_window)

        self._auto_close_job = self.after(30000, self._on_snooze)

    def _cancel_auto_close(self):
        if hasattr(self, "_auto_close_job") and self._auto_close_job:
            try:
                self.after_cancel(self._auto_close_job)
            except Exception:
                pass
            self._auto_close_job = None

    def destroy(self):
        self._cancel_auto_close()
        if hasattr(self, "parent") and hasattr(self.parent, "active_popups") and self.task_name in self.parent.active_popups:
            if self.parent.active_popups.get(self.task_name) is self:
                self.parent.active_popups.pop(self.task_name, None)
        try:
            super().destroy()
        except Exception:
            pass

    def _on_close_window(self):
        self._cancel_auto_close()
        self.destroy()

    def _on_done(self):
        self._cancel_auto_close()
        play_button_sound()
        if hasattr(self.parent, "task_snooze_counts") and self.task_name in self.parent.task_snooze_counts:
            self.parent.task_snooze_counts[self.task_name] = 0
        self.destroy()

    def _on_snooze(self):
        """5 dakika sonra tekrar darlamak üzere erteler."""
        self._cancel_auto_close()
        play_button_sound()
        if hasattr(self.parent, "task_snooze_counts"):
            self.parent.task_snooze_counts[self.task_name] = self.parent.task_snooze_counts.get(self.task_name, 0) + 1
        if hasattr(self.parent, "after"):
            # 5 dakika (300.000 ms) sonra aynı görevi tekrar darlamak için tetikle
            self.parent.after(300000, lambda t=self.task_name: self.parent.trigger_ai_notification(specific_task=t))
        self.destroy()

    def _on_dismiss_today(self):
        """Bu görevi bugün için tamamen susturur."""
        self._cancel_auto_close()
        play_button_sound()
        if hasattr(self.parent, "today_dismissed_tasks"):
            self.parent.today_dismissed_tasks.add(self.task_name)
        if hasattr(self.parent, "task_snooze_counts") and self.task_name in self.parent.task_snooze_counts:
            del self.parent.task_snooze_counts[self.task_name]
        self.destroy()


# ============================================================
#  GLOBAL KISAYOL (CTRL+SHIFT+T) - NATIVE WINDOWS HOTKEY
# ============================================================
class GlobalHotkeyManager:
    """Windows ctypes RegisterHotKey ile sıfır CPU harcayan arka plan global kısayol yöneticisi."""
    HOTKEY_ID = 101
    MOD_CONTROL = 0x0002
    MOD_SHIFT = 0x0004
    VK_T = 0x54

    def __init__(self, callback):
        self.callback = callback
        self.running = True
        self.thread = threading.Thread(target=self._msg_loop, daemon=True)
        self.thread.start()

    def _msg_loop(self):
        try:
            user32 = ctypes.windll.user32
            # Hotkey kaydet: Ctrl + Shift + T
            if not user32.RegisterHotKey(None, self.HOTKEY_ID, self.MOD_CONTROL | self.MOD_SHIFT, self.VK_T):
                return

            import ctypes.wintypes
            msg = ctypes.wintypes.MSG()
            while self.running:
                # GetMessageW tuşa basılana kadar 0 CPU ile bekler
                res = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
                if res == 0 or res == -1 or not self.running:
                    break
                if msg.message == 0x0312:  # WM_HOTKEY
                    if msg.wParam == self.HOTKEY_ID:
                        if self.callback and self.running:
                            self.callback()
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        except Exception:
            pass
        finally:
            try:
                ctypes.windll.user32.UnregisterHotKey(None, self.HOTKEY_ID)
            except Exception:
                pass

    def stop(self):
        self.running = False
        try:
            ctypes.windll.user32.UnregisterHotKey(None, self.HOTKEY_ID)
            ctypes.windll.user32.PostQuitMessage(0)
        except Exception:
            pass


# ============================================================
#  KAYAN MİNİ WİDGET (STICKY MODE - ALWAYS ON TOP)
# ============================================================
class StickyWidget(ctk.CTkToplevel):
    """Her zaman üstte duran, pürüzsüz yuvarlak köşeli, sürüklenebilir kompakt lofi mini görev widget'ı."""
    TRANS_COLOR = "#000001"

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("📌 Mini Görevler")
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        # Windows'ta köşeli beyaz çıkıntıları yok edip gerçek yuvarlak pencere yapmak için saydam renk
        try:
            self.wm_attributes("-transparentcolor", self.TRANS_COLOR)
        except Exception:
            pass
        self.configure(fg_color=self.TRANS_COLOR)

        screen_w = self.winfo_screenwidth()
        x = self.parent.settings.get("sticky_x", screen_w - 280)
        y = self.parent.settings.get("sticky_y", 80)
        self.geometry(f"260x340+{max(0, x)}+{max(0, y)}")

        self._drag_start_x = 0
        self._drag_start_y = 0

        self.setup_ui()
        self.bind_events()

    def setup_ui(self):
        theme = self.parent.get_theme()

        # Dış Yuvarlak Kart (Köşeleri saydam arka planda mükemmel yuvarlak görünür)
        self.card = ctk.CTkFrame(
            self, fg_color=theme["card"], corner_radius=16,
            border_width=1.5, border_color=theme.get("accent", "#7C3AED")
        )
        self.card.pack(fill="both", expand=True, padx=4, pady=4)

        # Başlık Çubuğu (Sürüklenebilir)
        self.header = ctk.CTkFrame(self.card, fg_color=theme["card_alt"], height=34, corner_radius=12)
        self.header.pack(fill="x", padx=6, pady=(6, 4))
        self.header.pack_propagate(False)

        # Başlık İkon & Metin
        self.title_lbl = ctk.CTkLabel(
            self.header, text="📌 Bugün", font=ctk.CTkFont(size=11, weight="bold"),
            text_color=theme["text"]
        )
        self.title_lbl.pack(side="left", padx=(10, 4))

        # İlerleme Rozeti (Pill)
        done, total = self.parent.get_today_progress()
        self.progress_frame = ctk.CTkFrame(self.header, fg_color=theme["card"], corner_radius=6)
        self.progress_frame.pack(side="left", padx=4)

        self.progress_lbl = ctk.CTkLabel(
            self.progress_frame, text=f"{done}/{total}", font=ctk.CTkFont(size=10, weight="bold"),
            text_color=theme.get("accent", "#FB7185")
        )
        self.progress_lbl.pack(padx=6, pady=1)

        # Kapat / Gizle Butonu
        self.close_btn = ctk.CTkButton(
            self.header, text="✕", width=22, height=22,
            fg_color="transparent", hover_color=theme["btn_danger"],
            text_color=theme["text"], corner_radius=11, font=ctk.CTkFont(size=10, weight="bold"),
            command=self.hide_widget
        )
        self.close_btn.pack(side="right", padx=(2, 6))

        # Ana Pencereyi Aç / Büyüt Butonu
        self.expand_btn = ctk.CTkButton(
            self.header, text="📂", width=22, height=22,
            fg_color="transparent", hover_color=theme["btn_primary_hover"],
            text_color=theme["text"], corner_radius=11, font=ctk.CTkFont(size=10),
            command=self.restore_main_window
        )
        self.expand_btn.pack(side="right", padx=2)

        # Görevler Kaydırılabilir Listesi
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.card, fg_color="transparent",
            scrollbar_button_color=theme["btn_primary"],
            scrollbar_button_hover_color=theme["btn_primary_hover"]
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=4, pady=(2, 6))

        self.render_tasks()

    def render_tasks(self):
        if not hasattr(self, "scroll_frame") or not self.scroll_frame.winfo_exists():
            return
        for w in self.scroll_frame.winfo_children():
            try:
                w.destroy()
            except Exception:
                pass

        theme = self.parent.get_theme()
        today = self.parent.today

        if not self.parent.tasks:
            ctk.CTkLabel(
                self.scroll_frame, text="Henüz görev eklenmemiş",
                font=ctk.CTkFont(size=11), text_color=theme["text_secondary"]
            ).pack(pady=25)
            return

        for task in self.parent.tasks:
            target = self.parent.get_task_target(task)
            is_done = self.parent.get_task_state(today, task)

            row = ctk.CTkFrame(self.scroll_frame, fg_color=theme["card_alt"], corner_radius=8, height=30)
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)

            if target > 1:
                cnt = self.parent.get_task_count(today, task)
                badge_text = f"✓{target}" if is_done else f"{cnt}/{target}"
                badge_color = theme.get("done", "#789262") if is_done else theme["btn_primary"]

                cnt_btn = ctk.CTkButton(
                    row, text=badge_text, width=42, height=22,
                    fg_color=badge_color, hover_color=theme["btn_primary_hover"],
                    text_color="#FFFFFF" if is_done else theme["text"],
                    corner_radius=6, font=ctk.CTkFont(size=9, weight="bold"),
                    command=lambda t=task: self.on_task_click(t)
                )
                cnt_btn.pack(side="left", padx=(6, 4))
                cnt_btn.bind("<Button-3>", lambda e, t=task: self.on_task_right_click(t))
            else:
                chk_text = "✓" if is_done else " "
                chk_color = theme.get("done", "#789262") if is_done else theme["card"]
                border_col = theme.get("done", "#789262") if is_done else theme.get("border", theme.get("entry_border", "#D1D5DB"))
                chk_btn = ctk.CTkButton(
                    row, text=chk_text, width=22, height=22,
                    fg_color=chk_color, hover_color=theme["btn_primary_hover"],
                    border_width=1.5, border_color=border_col,
                    text_color="#FFFFFF", corner_radius=6, font=ctk.CTkFont(size=11, weight="bold"),
                    command=lambda t=task: self.on_task_click(t)
                )
                chk_btn.pack(side="left", padx=(6, 4))
                chk_btn.bind("<Button-3>", lambda e, t=task: self.on_task_right_click(t))

            # Görev Adı
            lbl = ctk.CTkLabel(
                row, text=task, anchor="w",
                font=ctk.CTkFont(size=10, overstrike=is_done),
                text_color=theme["text_secondary"] if is_done else theme["text"]
            )
            lbl.pack(side="left", fill="x", expand=True, padx=(2, 6))
            lbl.bind("<Button-1>", lambda e, t=task: self.on_task_click(t))
            lbl.bind("<Button-3>", lambda e, t=task: self.on_task_right_click(t))

        # Başlıktaki ilerleme sayısını güncelle
        done, total = self.parent.get_today_progress()
        self.progress_lbl.configure(text=f"{done}/{total}")

    def on_task_click(self, task_name):
        target = self.parent.get_task_target(task_name)
        if target > 1:
            self.parent.increment_task(self.parent.today, task_name)
        else:
            self.parent.toggle_task(self.parent.today, task_name)
        self.render_tasks()
        self.parent.render_table()
        self.parent.update_charts()
        self.parent.update_progress()
        self.parent.check_daily_completion()

    def on_task_right_click(self, task_name):
        target = self.parent.get_task_target(task_name)
        if target > 1:
            self.parent.decrement_task(self.parent.today, task_name)
        else:
            self.parent.set_task_state(self.parent.today, task_name, False)
            play_task_sound(is_checking=False)
        self.render_tasks()
        self.parent.render_table()
        self.parent.update_charts()
        self.parent.update_progress()

    def apply_theme(self):
        theme = self.parent.get_theme()
        try:
            self.wm_attributes("-transparentcolor", self.TRANS_COLOR)
        except Exception:
            pass
        self.configure(fg_color=self.TRANS_COLOR)
        self.card.configure(fg_color=theme["card"], border_color=theme.get("accent", "#7C3AED"))
        self.header.configure(fg_color=theme["card_alt"])
        self.progress_frame.configure(fg_color=theme["card"])
        self.title_lbl.configure(text_color=theme["text"])
        self.progress_lbl.configure(text_color=theme.get("accent", "#FB7185"))
        self.close_btn.configure(text_color=theme["text"])
        self.expand_btn.configure(text_color=theme["text"])
        self.scroll_frame.configure(
            scrollbar_button_color=theme["btn_primary"],
            scrollbar_button_hover_color=theme["btn_primary_hover"]
        )
        self.render_tasks()

    def bind_events(self):
        for w in (self.header, self.title_lbl, self.progress_lbl, self.progress_frame):
            w.bind("<Button-1>", self._start_drag)
            w.bind("<B1-Motion>", self._on_drag)
            w.bind("<ButtonRelease-1>", self._stop_drag)

    def _start_drag(self, event):
        self._drag_start_x = event.x_root - self.winfo_x()
        self._drag_start_y = event.y_root - self.winfo_y()

    def _on_drag(self, event):
        x = event.x_root - self._drag_start_x
        y = event.y_root - self._drag_start_y
        self.geometry(f"+{x}+{y}")

    def _stop_drag(self, event):
        self.parent.settings["sticky_x"] = self.winfo_x()
        self.parent.settings["sticky_y"] = self.winfo_y()
        self.parent.save_data()

    def hide_widget(self):
        play_button_sound()
        self.withdraw()

    def show_widget(self):
        self.deiconify()
        self.lift()
        self.render_tasks()

    def restore_main_window(self):
        play_button_sound()
        self.parent.restore_from_tray()


# ============================================================
#  AYARLAR PENCERESİ
# ============================================================
class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        theme = parent.get_theme()

        self.title("⚙  Ayarlar")
        self.geometry("540x600")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color=theme["bg"])

        if os.path.exists(ICON_FILE):
            try:
                self.iconbitmap(ICON_FILE)
            except Exception:
                pass

        # Ana pencereye göre pürüzsüz ortalama
        try:
            px = parent.winfo_x() + (parent.winfo_width() - 540) // 2
            py = parent.winfo_y() + (parent.winfo_height() - 600) // 2
            self.geometry(f"540x600+{max(0, px)}+{max(0, py)}")
        except Exception:
            pass

        self.tabview = ctk.CTkTabview(self, fg_color=theme["card"],
                                      corner_radius=14,
                                      segmented_button_selected_color=theme["btn_primary"],
                                      segmented_button_selected_hover_color=theme["btn_primary_hover"])
        self.tabview.pack(fill="both", expand=True, padx=14, pady=14)

        self.tab_tasks = self.tabview.add("📋 Görevler")
        self.tab_theme = self.tabview.add("🎨 Tema")
        self.tab_sound = self.tabview.add("🔊 Ses")
        self.tab_ai = self.tabview.add("🤖 AI Darlama")
        self.tab_widget = self.tabview.add("📌 Kayan Widget")

        self.setup_tasks_tab(theme)
        self.setup_theme_tab(theme)
        self.setup_sound_tab(theme)
        self.setup_ai_notifications_tab(theme)
        self.setup_widget_tab(theme)

    # ---------- GÖREVLER ----------
    def setup_tasks_tab(self, theme):
        add_frame = ctk.CTkFrame(self.tab_tasks, corner_radius=12, fg_color=theme["card_alt"])
        add_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(add_frame, text="Yeni Görev Ekle",
                     font=ctk.CTkFont(weight="bold", size=14),
                     text_color=theme["text"]).pack(anchor="w", padx=12, pady=(10, 4))
        ctk.CTkLabel(add_frame, text="Sayaçlı görevler için hedef sayı yazabilirsiniz (örn: 8 bardak su, 20 sayfa)",
                     font=ctk.CTkFont(size=10),
                     text_color=theme["text_secondary"]).pack(anchor="w", padx=12, pady=(0, 6))

        inp = ctk.CTkFrame(add_frame, fg_color="transparent")
        inp.pack(fill="x", padx=12, pady=(0, 10))

        self.task_entry = ctk.CTkEntry(inp, placeholder_text="Görev adı yazın...", width=210,
                                       corner_radius=10,
                                       fg_color=theme["entry_bg"], border_color=theme["entry_border"],
                                       text_color=theme["text"])
        self.task_entry.pack(side="left", padx=(0, 6))

        self.target_entry = ctk.CTkEntry(inp, placeholder_text="Hedef (1)", width=80,
                                         corner_radius=10,
                                         fg_color=theme["entry_bg"], border_color=theme["entry_border"],
                                         text_color=theme["text"])
        self.target_entry.pack(side="left", padx=(0, 6))

        ctk.CTkButton(inp, text="Ekle", width=75, corner_radius=10,
                      fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"],
                      text_color=theme["text"], font=ctk.CTkFont(weight="bold"),
                      command=self.add_task).pack(side="left")

        list_frame = ctk.CTkFrame(self.tab_tasks, corner_radius=12, fg_color=theme["card_alt"])
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        ctk.CTkLabel(list_frame, text="Mevcut Görevler",
                     font=ctk.CTkFont(weight="bold", size=14),
                     text_color=theme["text"]).pack(anchor="w", padx=12, pady=10)

        self.scroll_frame = ctk.CTkScrollableFrame(list_frame, fg_color=theme["card_alt"], corner_radius=10)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.render_task_list()

    def render_task_list(self):
        theme = self.parent.get_theme()
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        if not self.parent.tasks:
            ctk.CTkLabel(self.scroll_frame, text="Henüz görev eklenmemiş.",
                         text_color=theme["text_secondary"]).pack(pady=20)
            return

        for task in self.parent.tasks:
            row = ctk.CTkFrame(self.scroll_frame, fg_color=theme["card"], corner_radius=10)
            row.pack(fill="x", pady=3, padx=4)

            target = self.parent.get_task_target(task)
            ctk.CTkLabel(row, text=task, anchor="w", font=ctk.CTkFont(size=12),
                         text_color=theme["text"]).pack(side="left", padx=12, fill="x", expand=True)

            if target > 1:
                badge = ctk.CTkFrame(row, fg_color=theme["card_alt"], corner_radius=6)
                badge.pack(side="right", padx=6)
                ctk.CTkLabel(badge, text=f"🔢 {target}x Sayaç", font=ctk.CTkFont(size=10, weight="bold"),
                             text_color=theme.get("accent", "#FB7185")).pack(padx=6, pady=2)

            ctk.CTkButton(row, text="Sil", width=55,
                          fg_color=theme["btn_danger"], hover_color=theme["btn_danger_hover"],
                          text_color="#FFFFFF", corner_radius=10,
                          command=lambda t=task: self.delete_task(t)).pack(side="right", padx=6, pady=5)

    def add_task(self):
        play_button_sound()
        new_task = self.task_entry.get().strip()
        if new_task and new_task not in self.parent.tasks:
            t_str = self.target_entry.get().strip()
            target_val = int(t_str) if (t_str.isdigit() and int(t_str) > 1) else 1
            if not hasattr(self.parent, "task_targets"):
                self.parent.task_targets = {}
            self.parent.task_targets[new_task] = target_val

            self.parent.tasks.append(new_task)
            if "ai_target_tasks" in self.parent.settings and new_task not in self.parent.settings["ai_target_tasks"]:
                self.parent.settings["ai_target_tasks"].append(new_task)
            self.parent.save_data()
            self.parent.render_table()
            self.parent.update_charts()
            self.parent.update_progress()
            self.task_entry.delete(0, "end")
            self.target_entry.delete(0, "end")
            self.render_task_list()
            self.render_ai_target_tasks()

    def delete_task(self, task_name):
        play_button_sound()
        if task_name in self.parent.tasks:
            self.parent.tasks.remove(task_name)
            if hasattr(self.parent, "task_targets"):
                self.parent.task_targets.pop(task_name, None)
            if "ai_target_tasks" in self.parent.settings and task_name in self.parent.settings["ai_target_tasks"]:
                self.parent.settings["ai_target_tasks"].remove(task_name)
            if hasattr(self.parent, "task_scheduled_times"):
                self.parent.task_scheduled_times.pop(task_name, None)
            if hasattr(self.parent, "task_snooze_counts"):
                self.parent.task_snooze_counts.pop(task_name, None)
            if hasattr(self.parent, "active_popups") and task_name in self.parent.active_popups:
                try:
                    self.parent.active_popups[task_name].destroy()
                except Exception:
                    pass
            self.parent.save_data()
            self.parent.render_table()
            self.parent.update_charts()
            self.parent.update_progress()
            self.render_task_list()
            self.render_ai_target_tasks()

    # ---------- TEMA ----------
    def setup_theme_tab(self, theme):
        scroll = ctk.CTkScrollableFrame(self.tab_theme, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        # Light temalar
        ctk.CTkLabel(scroll, text="☀️  Pastel Aydınlık Temalar",
                     font=ctk.CTkFont(weight="bold", size=14),
                     text_color=theme["text"]).pack(anchor="w", padx=8, pady=(8, 4))

        curr_light = self.parent.settings.get("light_theme", "Matcha & Adaçayı")
        if curr_light not in THEMES["light"]:
            curr_light = "Matcha & Adaçayı"
        self.light_var = ctk.StringVar(value=curr_light)

        for name, colors in THEMES["light"].items():
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", padx=8, pady=3)

            ctk.CTkRadioButton(row, text=name, variable=self.light_var, value=name,
                               command=self.on_theme_change,
                               text_color=theme["text"],
                               fg_color=colors["btn_primary"],
                               hover_color=colors["btn_primary_hover"]).pack(side="left", padx=(0, 12))

            for ck in ["bg", "card", "done", "moral_color", "efektiflik_color"]:
                sw = ctk.CTkFrame(row, width=15, height=15, corner_radius=7, fg_color=colors[ck])
                sw.pack(side="left", padx=2)
                sw.pack_propagate(False)

        ctk.CTkFrame(scroll, height=2, fg_color=theme["separator"]).pack(fill="x", padx=10, pady=12)

        # Dark temalar
        ctk.CTkLabel(scroll, text="🌙  Aesthetic Karanlık Temalar",
                     font=ctk.CTkFont(weight="bold", size=14),
                     text_color=theme["text"]).pack(anchor="w", padx=8, pady=(4, 4))

        curr_dark = self.parent.settings.get("dark_theme", "Gece Yarısı")
        if curr_dark not in THEMES["dark"]:
            curr_dark = "Gece Yarısı"
        self.dark_var = ctk.StringVar(value=curr_dark)

        for name, colors in THEMES["dark"].items():
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", padx=8, pady=3)

            ctk.CTkRadioButton(row, text=name, variable=self.dark_var, value=name,
                               command=self.on_theme_change,
                               text_color=theme["text"],
                               fg_color=colors["btn_primary"],
                               hover_color=colors["btn_primary_hover"]).pack(side="left", padx=(0, 12))

            for ck in ["bg", "card", "done", "moral_color", "efektiflik_color"]:
                sw = ctk.CTkFrame(row, width=15, height=15, corner_radius=7, fg_color=colors[ck])
                sw.pack(side="left", padx=2)
                sw.pack_propagate(False)

    def on_theme_change(self):
        play_button_sound()
        self.parent.settings["light_theme"] = self.light_var.get()
        self.parent.settings["dark_theme"] = self.dark_var.get()
        self.parent.save_data()
        self.parent.apply_theme(mode_changed=False)

        t = self.parent.get_theme()
        self.configure(fg_color=t["bg"])
        self.tabview.configure(fg_color=t["card"],
                               segmented_button_selected_color=t["btn_primary"],
                               segmented_button_selected_hover_color=t["btn_primary_hover"])

    # ---------- SES SEÇİMİ (GÖREV, BUTON & BİLDİRİM AYRI) ----------
    def setup_sound_tab(self, theme):
        scroll = ctk.CTkScrollableFrame(self.tab_sound, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=8, pady=8)

        sound_list = list(SOUND_OPTIONS.keys())

        # 1. KART: Görev & Kutucuk Sesi
        curr_task = self.parent.settings.get("task_sound", "Mekanik & Pop İkilisi")
        if curr_task not in SOUND_OPTIONS:
            curr_task = "Mekanik & Pop İkilisi"
        self.task_sound_var = ctk.StringVar(value=curr_task)

        c1 = ctk.CTkFrame(scroll, fg_color=theme["card_alt"], corner_radius=14)
        c1.pack(fill="x", padx=4, pady=6)

        c1_head = ctk.CTkFrame(c1, fg_color="transparent")
        c1_head.pack(fill="x", padx=14, pady=(12, 4))
        ctk.CTkLabel(c1_head, text="📋  Görev Tamamlama Sesi", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=theme["text"]).pack(side="left")

        ctk.CTkLabel(c1, text="Tablodaki görev kutucuklarını işaretlerken veya kaldırırken çalar.",
                     font=ctk.CTkFont(size=10), text_color=theme["text_secondary"]).pack(anchor="w", padx=14, pady=(0, 8))

        c1_row = ctk.CTkFrame(c1, fg_color="transparent")
        c1_row.pack(fill="x", padx=14, pady=(0, 8))

        self.task_menu = ctk.CTkOptionMenu(
            c1_row, values=sound_list, variable=self.task_sound_var,
            width=280, height=32, corner_radius=10,
            fg_color=theme["btn_primary"], button_color=theme["btn_primary_hover"],
            button_hover_color=theme["btn_primary"], text_color=theme["text"],
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.on_task_sound_change
        )
        self.task_menu.pack(side="left", padx=(0, 10))

        ctk.CTkButton(c1_row, text="▶ Dinle", width=75, height=32, corner_radius=10,
                      fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"],
                      text_color=theme["text"], font=ctk.CTkFont(size=11, weight="bold"),
                      command=lambda: self.preview_task_sound(self.task_sound_var.get())).pack(side="left")

        self.task_desc_lbl = ctk.CTkLabel(c1, text=SOUND_OPTIONS.get(curr_task, {}).get("desc", ""),
                                          font=ctk.CTkFont(size=10, slant="italic"), text_color=theme["text_secondary"])
        self.task_desc_lbl.pack(anchor="w", padx=14, pady=(0, 12))

        # 2. KART: Menü & Arayüz Buton Sesi
        curr_btn = self.parent.settings.get("button_sound", "Krem Switch (Lofi)")
        if curr_btn not in SOUND_OPTIONS:
            curr_btn = "Krem Switch (Lofi)"
        self.btn_sound_var = ctk.StringVar(value=curr_btn)

        c2 = ctk.CTkFrame(scroll, fg_color=theme["card_alt"], corner_radius=14)
        c2.pack(fill="x", padx=4, pady=6)

        c2_head = ctk.CTkFrame(c2, fg_color="transparent")
        c2_head.pack(fill="x", padx=14, pady=(12, 4))
        ctk.CTkLabel(c2_head, text="🔘  Menü & Arayüz Buton Sesi", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=theme["text"]).pack(side="left")

        ctk.CTkLabel(c2, text="Hafta/Ay değiştirme, ayarlar ve tema butonlarına basıldığında çalar.",
                     font=ctk.CTkFont(size=10), text_color=theme["text_secondary"]).pack(anchor="w", padx=14, pady=(0, 8))

        c2_row = ctk.CTkFrame(c2, fg_color="transparent")
        c2_row.pack(fill="x", padx=14, pady=(0, 8))

        self.btn_menu = ctk.CTkOptionMenu(
            c2_row, values=sound_list, variable=self.btn_sound_var,
            width=280, height=32, corner_radius=10,
            fg_color=theme["btn_primary"], button_color=theme["btn_primary_hover"],
            button_hover_color=theme["btn_primary"], text_color=theme["text"],
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.on_btn_sound_change
        )
        self.btn_menu.pack(side="left", padx=(0, 10))

        ctk.CTkButton(c2_row, text="▶ Dinle", width=75, height=32, corner_radius=10,
                      fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"],
                      text_color=theme["text"], font=ctk.CTkFont(size=11, weight="bold"),
                      command=lambda: self.preview_btn_sound(self.btn_sound_var.get())).pack(side="left")

        self.btn_desc_lbl = ctk.CTkLabel(c2, text=SOUND_OPTIONS.get(curr_btn, {}).get("desc", ""),
                                         font=ctk.CTkFont(size=10, slant="italic"), text_color=theme["text_secondary"])
        self.btn_desc_lbl.pack(anchor="w", padx=14, pady=(0, 12))

        # 3. KART: Standart Bildirim Sesi
        curr_notif = self.parent.settings.get("notification_sound", "Cozy Lofi Pop (Animal Pop)")
        if curr_notif not in SOUND_OPTIONS:
            curr_notif = "Cozy Lofi Pop (Animal Pop)"
        self.notif_sound_var = ctk.StringVar(value=curr_notif)

        c3 = ctk.CTkFrame(scroll, fg_color=theme["card_alt"], corner_radius=14)
        c3.pack(fill="x", padx=4, pady=6)

        c3_head = ctk.CTkFrame(c3, fg_color="transparent")
        c3_head.pack(fill="x", padx=14, pady=(12, 4))
        ctk.CTkLabel(c3_head, text="🔔  Standart Bildirim Sesi", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=theme["text"]).pack(side="left")

        ctk.CTkLabel(c3, text="Normal görev hatırlatma pencereleri ekrana geldiğinde çalar (Windows Hata Modu hariç).",
                     font=ctk.CTkFont(size=10), text_color=theme["text_secondary"]).pack(anchor="w", padx=14, pady=(0, 8))

        c3_row = ctk.CTkFrame(c3, fg_color="transparent")
        c3_row.pack(fill="x", padx=14, pady=(0, 8))

        self.notif_menu = ctk.CTkOptionMenu(
            c3_row, values=sound_list, variable=self.notif_sound_var,
            width=280, height=32, corner_radius=10,
            fg_color=theme["btn_primary"], button_color=theme["btn_primary_hover"],
            button_hover_color=theme["btn_primary"], text_color=theme["text"],
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.on_notif_sound_change
        )
        self.notif_menu.pack(side="left", padx=(0, 10))

        ctk.CTkButton(c3_row, text="▶ Dinle", width=75, height=32, corner_radius=10,
                      fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"],
                      text_color=theme["text"], font=ctk.CTkFont(size=11, weight="bold"),
                      command=lambda: self.preview_btn_sound(self.notif_sound_var.get())).pack(side="left")

        self.notif_desc_lbl = ctk.CTkLabel(c3, text=SOUND_OPTIONS.get(curr_notif, {}).get("desc", ""),
                                           font=ctk.CTkFont(size=10, slant="italic"), text_color=theme["text_secondary"])
        self.notif_desc_lbl.pack(anchor="w", padx=14, pady=(0, 12))

        # 4. KART: Moral & Efektiflik Puanlama Sesi
        curr_rating = self.parent.settings.get("rating_sound", "Minimalist UI Tık")
        if curr_rating not in SOUND_OPTIONS:
            curr_rating = "Minimalist UI Tık"
        self.rating_sound_var = ctk.StringVar(value=curr_rating)

        c4 = ctk.CTkFrame(scroll, fg_color=theme["card_alt"], corner_radius=14)
        c4.pack(fill="x", padx=4, pady=6)

        c4_head = ctk.CTkFrame(c4, fg_color="transparent")
        c4_head.pack(fill="x", padx=14, pady=(12, 4))
        ctk.CTkLabel(c4_head, text="⚡  Moral & Efektiflik Puanlama Sesi", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=theme["text"]).pack(side="left")

        ctk.CTkLabel(c4, text="Tablonun altındaki Moral ve Efektiflik puan kutucuklarına tıklandığında çalar.",
                     font=ctk.CTkFont(size=10), text_color=theme["text_secondary"]).pack(anchor="w", padx=14, pady=(0, 8))

        c4_row = ctk.CTkFrame(c4, fg_color="transparent")
        c4_row.pack(fill="x", padx=14, pady=(0, 8))

        self.rating_menu = ctk.CTkOptionMenu(
            c4_row, values=sound_list, variable=self.rating_sound_var,
            width=280, height=32, corner_radius=10,
            fg_color=theme["btn_primary"], button_color=theme["btn_primary_hover"],
            button_hover_color=theme["btn_primary"], text_color=theme["text"],
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.on_rating_sound_change
        )
        self.rating_menu.pack(side="left", padx=(0, 10))

        ctk.CTkButton(c4_row, text="▶ Dinle", width=75, height=32, corner_radius=10,
                      fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"],
                      text_color=theme["text"], font=ctk.CTkFont(size=11, weight="bold"),
                      command=lambda: self.preview_btn_sound(self.rating_sound_var.get())).pack(side="left")

        self.rating_desc_lbl = ctk.CTkLabel(c4, text=SOUND_OPTIONS.get(curr_rating, {}).get("desc", ""),
                                            font=ctk.CTkFont(size=10, slant="italic"), text_color=theme["text_secondary"])
        self.rating_desc_lbl.pack(anchor="w", padx=14, pady=(0, 12))

    def preview_task_sound(self, sound_name):
        info = SOUND_OPTIONS.get(sound_name)
        if info and info["on_file"]:
            SoundEngine.play(info["on_file"])
            if info["off_file"] and info["off_file"] != info["on_file"]:
                self.after(140, lambda: SoundEngine.play(info["off_file"]))

    def preview_btn_sound(self, sound_name):
        info = SOUND_OPTIONS.get(sound_name)
        if info and info["on_file"]:
            SoundEngine.play(info["on_file"])

    def on_task_sound_change(self, value=None):
        s_name = self.task_sound_var.get()
        self.parent.settings["task_sound"] = s_name
        self.parent.save_data()
        self.task_desc_lbl.configure(text=SOUND_OPTIONS.get(s_name, {}).get("desc", ""))
        self.preview_task_sound(s_name)

    def on_btn_sound_change(self, value=None):
        s_name = self.btn_sound_var.get()
        self.parent.settings["button_sound"] = s_name
        self.parent.save_data()
        self.btn_desc_lbl.configure(text=SOUND_OPTIONS.get(s_name, {}).get("desc", ""))
        self.preview_btn_sound(s_name)

    def on_notif_sound_change(self, value=None):
        s_name = self.notif_sound_var.get()
        self.parent.settings["notification_sound"] = s_name
        self.parent.save_data()
        self.notif_desc_lbl.configure(text=SOUND_OPTIONS.get(s_name, {}).get("desc", ""))
        self.preview_btn_sound(s_name)

    def on_rating_sound_change(self, value=None):
        s_name = self.rating_sound_var.get()
        self.parent.settings["rating_sound"] = s_name
        self.parent.save_data()
        self.rating_desc_lbl.configure(text=SOUND_OPTIONS.get(s_name, {}).get("desc", ""))
        self.preview_btn_sound(s_name)

    # ---------- AI BİLDİRİMLER ----------
    def setup_ai_notifications_tab(self, theme):
        scroll = ctk.CTkScrollableFrame(self.tab_ai, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        # 1. Ana Açma / Kapatma
        top_box = ctk.CTkFrame(scroll, fg_color=theme["card_alt"], corner_radius=12)
        top_box.pack(fill="x", padx=6, pady=4)

        t_inner = ctk.CTkFrame(top_box, fg_color="transparent")
        t_inner.pack(fill="x", padx=12, pady=(10, 6))

        ctk.CTkLabel(t_inner, text="Otomatik Bildirimler",
                     font=ctk.CTkFont(weight="bold", size=14),
                     text_color=theme["text"]).pack(side="left")

        is_enabled = self.parent.settings.get("ai_notifications_enabled", True)
        self.ai_enable_var = ctk.BooleanVar(value=is_enabled)
        self.ai_switch = ctk.CTkSwitch(t_inner, text="Aktif" if is_enabled else "Kapalı",
                                       variable=self.ai_enable_var,
                                       command=self.on_ai_toggle,
                                       font=ctk.CTkFont(size=12, weight="bold"),
                                       fg_color=theme["switch_off"], progress_color=theme["switch_on"],
                                       button_color=theme["switch_btn"], button_hover_color=theme["switch_btn_hover"])
        self.ai_switch.pack(side="right")

        # Hızlı Test Butonları (Doğrudan en üstte, hiç kaydırmadan anında görünür!)
        test_top_row = ctk.CTkFrame(top_box, fg_color="transparent")
        test_top_row.pack(fill="x", padx=12, pady=(4, 10))

        ctk.CTkButton(test_top_row, text="⚡ Normal Bildirim Testi", height=30, corner_radius=8,
                      fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"],
                      text_color=theme["text"], font=ctk.CTkFont(size=11, weight="bold"),
                      command=self.trigger_test_roast).pack(side="left", fill="x", expand=True, padx=(0, 4))

        ctk.CTkButton(test_top_row, text="🛑 Windows Hata Testi", height=30, corner_radius=8,
                      fg_color="#EF4444", hover_color="#DC2626",
                      text_color="#FFFFFF", font=ctk.CTkFont(size=11, weight="bold"),
                      command=self.trigger_test_error).pack(side="right", fill="x", expand=True, padx=(4, 0))

        # 2. Model Seçimi
        m_box = ctk.CTkFrame(scroll, fg_color=theme["card_alt"], corner_radius=12)
        m_box.pack(fill="x", padx=6, pady=4)

        ctk.CTkLabel(m_box, text="AI Motoru",
                     font=ctk.CTkFont(weight="bold", size=13),
                     text_color=theme["text"]).pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(m_box, text="Yerel AI modeli seç veya dahili motoru kullan",
                     font=ctk.CTkFont(size=11),
                     text_color=theme["text_secondary"]).pack(anchor="w", padx=12, pady=(0, 6))

        m_row = ctk.CTkFrame(m_box, fg_color="transparent")
        m_row.pack(fill="x", padx=12, pady=(0, 10))

        saved_models = self.parent.settings.get("detected_ai_models", [
            DEFAULT_AI_MODEL,
        ])
        cur_model = self.parent.settings.get("ai_model", DEFAULT_AI_MODEL)
        if cur_model not in saved_models:
            saved_models.append(cur_model)

        self.model_var = ctk.StringVar(value=cur_model)
        self.model_menu = ctk.CTkOptionMenu(m_row, variable=self.model_var, values=saved_models,
                                            width=260, height=28, corner_radius=8,
                                            fg_color=theme["entry_bg"], button_color=theme["btn_primary"],
                                            button_hover_color=theme["btn_primary_hover"],
                                            text_color=theme["text"],
                                            command=self.on_model_change)
        self.model_menu.pack(side="left", padx=(0, 8))

        self.scan_btn = ctk.CTkButton(m_row, text="🔄 Tara", width=90, height=28, corner_radius=8,
                                      fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"],
                                      text_color=theme["text"], font=ctk.CTkFont(size=11, weight="bold"),
                                      command=self.refresh_ai_models)
        self.m_box = m_box

        # Gemini API Key Kartı
        self.gemini_box = ctk.CTkFrame(scroll, fg_color=theme["card_alt"], corner_radius=12)
        if "gemini" in cur_model.lower():
            self.gemini_box.pack(fill="x", padx=6, pady=4)

        ctk.CTkLabel(self.gemini_box, text="🔑 Google Gemini API Anahtarı",
                     font=ctk.CTkFont(weight="bold", size=13),
                     text_color=theme["text"]).pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(self.gemini_box, text="Google AI Studio'dan aldığınız ücretsiz API anahtarınızı girin",
                     font=ctk.CTkFont(size=11),
                     text_color=theme["text_secondary"]).pack(anchor="w", padx=12, pady=(0, 6))

        g_row = ctk.CTkFrame(self.gemini_box, fg_color="transparent")
        g_row.pack(fill="x", padx=12, pady=(0, 4))

        self.gemini_key_entry = ctk.CTkEntry(g_row, placeholder_text="AIzaSy...",
                                             width=280, height=28, corner_radius=8,
                                             fg_color=theme["entry_bg"], border_color=theme["entry_border"],
                                             text_color=theme["text"], show="*")
        self.gemini_key_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.gemini_key_entry.insert(0, self.parent.settings.get("gemini_api_key", ""))
        self.gemini_key_entry.bind("<KeyRelease>", lambda e: self.on_gemini_key_change())

        self.gemini_show_btn = ctk.CTkButton(g_row, text="👁️", width=34, height=28, corner_radius=8,
                                             fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"],
                                             text_color=theme["text"], command=self.toggle_gemini_key_visibility)
        self.gemini_show_btn.pack(side="left", padx=(0, 6))

        g_btn_row = ctk.CTkFrame(self.gemini_box, fg_color="transparent")
        g_btn_row.pack(fill="x", padx=12, pady=(4, 10))

        ctk.CTkButton(g_btn_row, text="🔑 Ücretsiz API Key Al (AI Studio)", height=26, corner_radius=8,
                      fg_color=theme.get("accent", "#7C3AED"), hover_color=theme["btn_primary_hover"],
                      text_color="#FFFFFF", font=ctk.CTkFont(size=10, weight="bold"),
                      command=lambda: webbrowser.open("https://aistudio.google.com/app/apikey")).pack(side="left", padx=(0, 6))

        # 3. Mesaj Tarzı
        p_box = ctk.CTkFrame(scroll, fg_color=theme["card_alt"], corner_radius=12)
        p_box.pack(fill="x", padx=6, pady=4)

        ctk.CTkLabel(p_box, text="Mesaj Tarzı",
                     font=ctk.CTkFont(weight="bold", size=13),
                     text_color=theme["text"]).pack(anchor="w", padx=12, pady=(10, 6))

        cur_personality = self.parent.settings.get("ai_personality", "Sert & Direkt")
        # Eski key'leri yeni isimlere migrasyon
        migration_map = {"Zorba": "Sert & Direkt", "Çavuş": "Sert & Direkt", "Pasif-Agresif": "Alaycı & Esprili"}
        if cur_personality in migration_map:
            cur_personality = migration_map[cur_personality]
            self.parent.settings["ai_personality"] = cur_personality
        self.personality_var = ctk.StringVar(value=cur_personality)

        pers_options = [
            ("Sert & Direkt", "Sert ve direkt hatırlatmalar. Lafı dolandırmaz, net konuşur."),
            ("Alaycı & Esprili", "Esprili ve iğneleyici ton. Güldürürken hatırlatır."),
            ("Motivasyonel", "Pozitif ve cesaretlendirici. Motive ederek harekete geçirir."),
            ("Özel", "Kendi mesaj tarzını ve talimatını belirle.")
        ]

        for p_key, p_desc in pers_options:
            p_row = ctk.CTkFrame(p_box, fg_color="transparent")
            p_row.pack(fill="x", padx=12, pady=2)

            ctk.CTkRadioButton(p_row, text=p_key, variable=self.personality_var, value=p_key,
                               font=ctk.CTkFont(weight="bold", size=12),
                               command=self.on_personality_change,
                               text_color=theme["text"],
                               fg_color=theme["btn_primary"],
                               hover_color=theme["btn_primary_hover"]).pack(side="left")
            ctk.CTkLabel(p_row, text=f"  —  {p_desc}", font=ctk.CTkFont(size=10),
                         text_color=theme["text_secondary"]).pack(side="left", padx=(4, 0))

        # Özel Prompt Girişi
        self.custom_prompt_frame = ctk.CTkFrame(p_box, fg_color="transparent")
        if cur_personality == "Özel":
            self.custom_prompt_frame.pack(fill="x", padx=12, pady=(4, 10))

        self.custom_prompt_entry = ctk.CTkEntry(self.custom_prompt_frame,
                                               placeholder_text="Örnek: Kısa ve sert, patronvari bir hatırlatma yap...",
                                               width=420, height=28, corner_radius=8,
                                               fg_color=theme["entry_bg"], border_color=theme["entry_border"],
                                               text_color=theme["text"])
        self.custom_prompt_entry.pack(fill="x", pady=(0, 4))
        self.custom_prompt_entry.insert(0, self.parent.settings.get("ai_custom_prompt", ""))
        self.custom_prompt_entry.bind("<KeyRelease>", lambda e: self.on_custom_prompt_change())

        # 4. Bildirim Sıklığı
        int_box = ctk.CTkFrame(scroll, fg_color=theme["card_alt"], corner_radius=12)
        int_box.pack(fill="x", padx=6, pady=4)

        ctk.CTkLabel(int_box, text="Bildirim Sıklığı",
                     font=ctk.CTkFont(weight="bold", size=13),
                     text_color=theme["text"]).pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(int_box, text="Yapılmamış görevler için bildirim aralığı",
                     font=ctk.CTkFont(size=11),
                     text_color=theme["text_secondary"]).pack(anchor="w", padx=12, pady=(0, 6))

        cur_interval = self.parent.settings.get("ai_interval", "30 Dk")
        self.interval_var = ctk.StringVar(value=cur_interval)
        self.interval_seg = ctk.CTkSegmentedButton(int_box, values=["15 Dk", "30 Dk", "45 Dk", "1 Saat", "2 Saat"],
                                                   variable=self.interval_var,
                                                   command=self.on_interval_change,
                                                   selected_color=theme["btn_primary"],
                                                   selected_hover_color=theme["btn_primary_hover"],
                                                   unselected_color=theme["entry_bg"],
                                                   unselected_hover_color=theme["card"])
        self.interval_seg.pack(fill="x", padx=12, pady=(0, 12))

        # 5. Bildirim Görevleri
        t_box = ctk.CTkFrame(scroll, fg_color=theme["card_alt"], corner_radius=12)
        t_box.pack(fill="x", padx=6, pady=4)

        ctk.CTkLabel(t_box, text="Bildirim Görevleri",
                     font=ctk.CTkFont(weight="bold", size=13),
                     text_color=theme["text"]).pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(t_box, text="Hangi görevler için bildirim gönderilsin?",
                     font=ctk.CTkFont(size=11),
                     text_color=theme["text_secondary"]).pack(anchor="w", padx=12, pady=(0, 6))

        self.ai_target_tasks_box = ctk.CTkFrame(t_box, fg_color="transparent")
        self.ai_target_tasks_box.pack(fill="x", padx=12, pady=(0, 10))
        self.render_ai_target_tasks()

        # Alt kaydırma boşluğu
        ctk.CTkFrame(scroll, height=20, fg_color="transparent").pack()

    def render_ai_target_tasks(self):
        """AI Darlama sekmesindeki hedef görev seçim kutucuklarını güncel görev listesine göre yeniden çizer."""
        if not hasattr(self, "ai_target_tasks_box") or not self.ai_target_tasks_box.winfo_exists():
            return

        for w in self.ai_target_tasks_box.winfo_children():
            w.destroy()

        theme = self.parent.get_theme()
        target_tasks = self.parent.settings.get("ai_target_tasks", list(self.parent.tasks))
        self.task_check_vars = {}

        for task_name in self.parent.tasks:
            t_row = ctk.CTkFrame(self.ai_target_tasks_box, fg_color="transparent")
            t_row.pack(fill="x", pady=2)

            var = ctk.BooleanVar(value=(task_name in target_tasks))
            self.task_check_vars[task_name] = var

            cb = ctk.CTkCheckBox(t_row, text=task_name, variable=var,
                                 font=ctk.CTkFont(size=12),
                                 command=self.on_target_tasks_change,
                                 text_color=theme["text"],
                                 fg_color=theme["btn_primary"],
                                 hover_color=theme["btn_primary_hover"])
            cb.pack(side="left")

        if not self.parent.tasks:
            ctk.CTkLabel(self.ai_target_tasks_box, text="Henüz görev eklenmemiş.",
                         font=ctk.CTkFont(size=11),
                         text_color=theme["text_secondary"]).pack(pady=8)

    def on_ai_toggle(self):
        play_button_sound()
        val = self.ai_enable_var.get()
        self.ai_switch.configure(text="Aktif" if val else "Kapalı")
        self.parent.settings["ai_notifications_enabled"] = val
        self.parent.save_data()

    def on_model_change(self, choice):
        play_button_sound()
        self.parent.settings["ai_model"] = choice
        self.parent.save_data()
        if hasattr(self, "gemini_box") and self.gemini_box.winfo_exists():
            if "gemini" in choice.lower():
                self.gemini_box.pack(fill="x", padx=6, pady=4, after=self.m_box)
            else:
                self.gemini_box.pack_forget()

    def on_gemini_key_change(self):
        try:
            if hasattr(self, "gemini_key_entry") and self.gemini_key_entry.winfo_exists():
                val = self.gemini_key_entry.get().strip()
                self.parent.settings["gemini_api_key"] = val
                self.parent.save_data()
        except Exception:
            pass

    def toggle_gemini_key_visibility(self):
        play_button_sound()
        try:
            cur_show = self.gemini_key_entry.cget("show")
            if cur_show == "*":
                self.gemini_key_entry.configure(show="")
                self.gemini_show_btn.configure(text="🔒")
            else:
                self.gemini_key_entry.configure(show="*")
                self.gemini_show_btn.configure(text="👁️")
        except Exception:
            pass

    def setup_widget_tab(self, theme):
        scroll = ctk.CTkScrollableFrame(self.tab_widget, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        # 1. Kayan Mini Widget Kontrol Kartı
        c1 = ctk.CTkFrame(scroll, fg_color=theme["card_alt"], corner_radius=12)
        c1.pack(fill="x", padx=6, pady=6)

        ctk.CTkLabel(c1, text="📌 Kayan Mini Widget (Sticky Mode)",
                     font=ctk.CTkFont(weight="bold", size=14),
                     text_color=theme["text"]).pack(anchor="w", padx=12, pady=(12, 4))
        ctk.CTkLabel(c1, text="Ekranın köşesinde her zaman üstte duran, şeffaf ve minimalist kompakt görev kartı.",
                     font=ctk.CTkFont(size=11), text_color=theme["text_secondary"]).pack(anchor="w", padx=12, pady=(0, 8))

        c1_btns = ctk.CTkFrame(c1, fg_color="transparent")
        c1_btns.pack(fill="x", padx=12, pady=(4, 12))

        ctk.CTkButton(
            c1_btns, text="📌 Kayan Mini Modu Aç", height=32, corner_radius=10,
            fg_color=theme.get("accent", "#7C3AED"), hover_color=theme["btn_primary_hover"],
            text_color="#FFFFFF", font=ctk.CTkFont(size=11, weight="bold"),
            command=self.parent.open_sticky_widget
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            c1_btns, text="✕ Gizle / Kapat", height=32, corner_radius=10,
            fg_color=theme["card"], hover_color=theme["btn_danger"],
            text_color=theme["text"], font=ctk.CTkFont(size=11),
            command=self.parent.hide_sticky_widget
        ).pack(side="left")

        # 2. Global Kısayol Kartı
        c2 = ctk.CTkFrame(scroll, fg_color=theme["card_alt"], corner_radius=12)
        c2.pack(fill="x", padx=6, pady=6)

        ctk.CTkLabel(c2, text="⌨️ Global Klavye Kısayolu",
                     font=ctk.CTkFont(weight="bold", size=14),
                     text_color=theme["text"]).pack(anchor="w", padx=12, pady=(12, 4))
        ctk.CTkLabel(c2, text="Hangi uygulamada veya oyunda olursanız olun klavyenizden kısayola basarak uygulamayı veya mini widget'ı anında açıp gizleyebilirsiniz.",
                     font=ctk.CTkFont(size=11), text_color=theme["text_secondary"], wraplength=460, justify="left").pack(anchor="w", padx=12, pady=(0, 8))

        hk_row = ctk.CTkFrame(c2, fg_color="transparent")
        hk_row.pack(fill="x", padx=12, pady=(4, 12))

        hk_badge = ctk.CTkFrame(hk_row, fg_color=theme["card"], corner_radius=8, border_width=1, border_color=theme.get("accent", "#7C3AED"))
        hk_badge.pack(side="left", padx=(0, 10))
        ctk.CTkLabel(hk_badge, text="Ctrl + Shift + T", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=theme.get("accent", "#7C3AED")).pack(padx=12, pady=6)

        ctk.CTkLabel(hk_row, text="✅ Sistemde Aktif (%0 CPU)", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=theme.get("done", "#789262")).pack(side="left")

    def refresh_ai_models(self):
        play_button_sound()
        self.scan_btn.configure(text="⏳ Taranıyor...", state="disabled")

        def _scan():
            models = scan_local_ai_models()

            def _update():
                self.parent.settings["detected_ai_models"] = models
                self.model_menu.configure(values=models)
                if self.model_var.get() not in models:
                    self.model_var.set(models[0])
                    self.parent.settings["ai_model"] = models[0]
                self.parent.save_data()
                self.scan_btn.configure(text="✓ Güncellendi", state="normal")
                self.after(2000, lambda: self.scan_btn.configure(text="🔄 Modelleri Tara"))

            self.after(0, _update)

        threading.Thread(target=_scan, daemon=True).start()

    def on_personality_change(self):
        play_button_sound()
        pers = self.personality_var.get()
        self.parent.settings["ai_personality"] = pers
        self.parent.save_data()

        if pers == "Özel":
            self.custom_prompt_frame.pack(fill="x", padx=12, pady=(4, 10))
        else:
            self.custom_prompt_frame.pack_forget()

    def on_custom_prompt_change(self):
        # 500ms debounce: her tuş basışında değil, yazmayı bıraktıktan 500ms sonra kaydet
        if hasattr(self, "_prompt_save_job") and self._prompt_save_job:
            self.after_cancel(self._prompt_save_job)
        self._prompt_save_job = self.after(500, self._save_custom_prompt)

    def _save_custom_prompt(self):
        self._prompt_save_job = None
        try:
            if hasattr(self, "custom_prompt_entry") and self.custom_prompt_entry.winfo_exists():
                val = self.custom_prompt_entry.get()
                self.parent.settings["ai_custom_prompt"] = val
                self.parent.save_data()
        except Exception:
            pass

    def on_interval_change(self, val):
        play_button_sound()
        self.parent.settings["ai_interval"] = val
        self.parent.save_data()
        self.parent._schedule_tasks_independently(force_reset=True)

    def on_target_tasks_change(self):
        play_button_sound()
        selected = [t for t, var in self.task_check_vars.items() if var.get()]
        self.parent.settings["ai_target_tasks"] = selected
        self.parent.save_data()
        self.parent._schedule_tasks_independently(force_reset=False)

    def trigger_test_roast(self):
        play_button_sound()
        self.parent.trigger_ai_notification(is_test=True)

    def trigger_test_error(self):
        play_button_sound()
        self.parent.trigger_ai_notification(is_test=True, force_snooze_count=1)


# ============================================================
#  ANA UYGULAMA
# ============================================================
class HabitTrackerApp(ctk.CTk):
    CURRENT_INSTANCE = None

    def __init__(self):
        super().__init__()
        HabitTrackerApp.CURRENT_INSTANCE = self

        self.title("Görev & Alışkanlık Takip Programı")

        try:
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            default_w = min(1480, max(1200, int(screen_w * 0.94)))
            default_h = min(920, max(750, int(screen_h * 0.88)))
            px = max(0, (screen_w - default_w) // 2)
            py = max(0, (screen_h - default_h) // 2)
            self.geometry(f"{default_w}x{default_h}+{px}+{py}")
        except Exception:
            self.geometry("1440x880")

        self.minsize(1050, 700)

        # Uygulama Simgesi (ToDo.ico)
        self.apply_app_icon()
        self.after(200, self.apply_app_icon)

        # Tarih bilgileri
        self.today = datetime.date.today()

        # Haftalık hesap (grafik 1 için)
        self.current_monday = self.today - datetime.timedelta(days=self.today.weekday())
        self.selected_monday = self.current_monday
        self.week_dates = [self.current_monday + datetime.timedelta(days=i) for i in range(7)]

        # Grafik ve Tablo ay navigasyonu
        self.chart_year = self.today.year
        self.chart_month = self.today.month
        self.table_year = self.today.year
        self.table_month = self.today.month

        # Veriler (İlk kurulum varsayılanları)
        self.tasks = ["Sabah Yürüyüşü / Spor", "Kitap Oku (20 Sayfa)", "Kodlama & Proje Çalış", "Günde 2L Su İç"]
        self.task_targets = {"Günde 2L Su İç": 8, "Kitap Oku (20 Sayfa)": 20}
        self.records = {}
        self.moral_records = {}
        self.efektiflik_records = {}
        self.task_snooze_counts = {}
        self.today_dismissed_tasks = set()
        self.task_scheduled_times = {}
        self.active_popups = {}
        self.settings = {
            "mode": "light",
            "light_theme": "Latte & Şeftali",
            "dark_theme": "Karanlık Karbon",
            "task_sound": "Mekanik & Pop İkilisi",
            "button_sound": "Krem Switch (Lofi)",
            "notification_sound": "Tatlı Kabarcık (Bubble Pop)",
            "rating_sound": "Minimalist UI Tık",
            "bonus_xp": 0,
            "streak_freezes": 1,
            "last_freeze_week": self.today.isocalendar()[1],
            "last_celebrated_date": "",
            "ai_notifications_enabled": True,
            "ai_model": DEFAULT_AI_MODEL,
            "ai_personality": "Sert & Direkt",
            "ai_custom_prompt": "",
            "ai_interval": "45 Dk",
            "ai_target_tasks": ["Sabah Yürüyüşü / Spor", "Kitap Oku (20 Sayfa)", "Kodlama & Proje Çalış", "Günde 2L Su İç"],
            "last_ai_notification_time": 0
        }

        self.load_data()
        self.check_streak_freeze()

        # Geriye dönük uyumluluk
        if self.settings.get("light_theme") not in THEMES["light"]:
            self.settings["light_theme"] = "Latte & Şeftali"
        if self.settings.get("dark_theme") not in THEMES["dark"]:
            self.settings["dark_theme"] = "Karanlık Karbon"
        if self.settings.get("task_sound") not in SOUND_OPTIONS:
            self.settings["task_sound"] = "Mekanik & Pop İkilisi"
        if self.settings.get("button_sound") not in SOUND_OPTIONS:
            self.settings["button_sound"] = "Krem Switch (Lofi)"
        if self.settings.get("notification_sound") not in SOUND_OPTIONS:
            self.settings["notification_sound"] = "Tatlı Kabarcık (Bubble Pop)"
        if self.settings.get("rating_sound") not in SOUND_OPTIONS:
            self.settings["rating_sound"] = "Minimalist UI Tık"

        self.settings.setdefault("bonus_xp", 0)
        self.settings.setdefault("streak_freezes", 1)
        self.settings.setdefault("last_freeze_week", self.today.isocalendar()[1])
        self.settings.setdefault("last_celebrated_date", "")
        self.settings.setdefault("ai_notifications_enabled", True)
        self.settings.setdefault("ai_model", DEFAULT_AI_MODEL)
        if self.settings.get("ai_model") == "Dahili Motor (Yerel/Hızlı)":
            self.settings["ai_model"] = DEFAULT_AI_MODEL
        self.settings.setdefault("ai_personality", "Sert & Direkt")
        self.settings.setdefault("ai_custom_prompt", "")
        self.settings.setdefault("ai_interval", "45 Dk")
        self.settings.setdefault("ai_target_tasks", list(self.tasks))
        self.settings.setdefault("last_ai_notification_time", 0)
        self.settings.setdefault("gemini_api_key", "")
        self.settings.setdefault("sticky_x", max(0, self.winfo_screenwidth() - 270))
        self.settings.setdefault("sticky_y", 80)

        # Kayan Mini Widget & Global Hotkey (Ctrl+Shift+T)
        self.sticky_widget = None
        self.hotkey_mgr = GlobalHotkeyManager(self.toggle_from_hotkey)

        # Tema modu
        mode = self.settings.get("mode", "light")
        ctk.set_appearance_mode("Light" if mode == "light" else "Dark")

        self.setup_ui()
        self.setup_charts()
        self.apply_theme(mode_changed=False)
        self.update_clock()
        self.update_charts()
        self.update_progress()

        # Sistem Tepsisi & Arka Plan AI Darlama Döngüsü
        self.protocol("WM_DELETE_WINDOW", self.hide_to_tray)
        self.tray_icon = None
        self.setup_tray_icon()
        self.check_ai_notifications()

    # ---------- VERİ YÖNETİMİ ----------
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", self.tasks)
                    self.task_targets = data.get("task_targets", getattr(self, "task_targets", {}))
                    self.records = data.get("records", {})
                    self.moral_records = data.get("moral_records", {})
                    self.efektiflik_records = data.get("efektiflik_records", {})
                    self.settings = data.get("settings", self.settings)
                    return
            except Exception as e:
                print(f"Veri yükleme hatası: {e}")

        # Yedekten kurtarma (varsa)
        bak_file = DATA_FILE + ".bak"
        if os.path.exists(bak_file):
            try:
                with open(bak_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", self.tasks)
                    self.task_targets = data.get("task_targets", getattr(self, "task_targets", {}))
                    self.records = data.get("records", {})
                    self.moral_records = data.get("moral_records", {})
                    self.efektiflik_records = data.get("efektiflik_records", {})
                    self.settings = data.get("settings", self.settings)
            except Exception:
                pass

    def save_data(self):
        data = {
            "tasks": self.tasks,
            "task_targets": getattr(self, "task_targets", {}),
            "records": self.records,
            "moral_records": self.moral_records,
            "efektiflik_records": self.efektiflik_records,
            "settings": self.settings,
        }
        try:
            tmp_file = DATA_FILE + ".tmp"
            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            if os.path.exists(DATA_FILE):
                try:
                    import shutil
                    shutil.copy2(DATA_FILE, DATA_FILE + ".bak")
                except Exception:
                    pass
            os.replace(tmp_file, DATA_FILE)
        except Exception as e:
            print(f"Veri kaydetme hatası: {e}")
            try:
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            except Exception:
                pass

    def get_task_target(self, task_name):
        return max(1, int(getattr(self, "task_targets", {}).get(task_name, 1)))

    def get_task_val(self, date_obj, task_name):
        return self.records.get(date_obj.strftime("%Y-%m-%d"), {}).get(task_name, False)

    def get_task_state(self, date_obj, task_name):
        """Görevin o gün tamamlanıp tamamlanmadığını döndürür (True/False)."""
        target = self.get_task_target(task_name)
        val = self.get_task_val(date_obj, task_name)
        if target <= 1:
            return bool(val)
        if isinstance(val, (int, float)):
            return val >= target
        return bool(val)

    def get_task_count(self, date_obj, task_name):
        """Sayaçlı görevler için o günkü mevcut sayıyı döndürür."""
        target = self.get_task_target(task_name)
        val = self.get_task_val(date_obj, task_name)
        if target <= 1:
            return 1 if val else 0
        if isinstance(val, (int, float)):
            return min(target, max(0, int(val)))
        return target if val else 0

    def increment_task(self, date_obj, task_name):
        """Görevin durumunu günceller: normal görevde True/False, sayaçlı görevde +1 (dolunca 0)."""
        target = self.get_task_target(task_name)
        ds = date_obj.strftime("%Y-%m-%d")
        self.records.setdefault(ds, {})
        curr_val = self.records[ds].get(task_name, 0 if target > 1 else False)

        if target <= 1:
            new_val = not bool(curr_val)
            self.records[ds][task_name] = new_val
            is_completed = new_val
            is_just_completed = new_val
        else:
            curr_count = curr_val if isinstance(curr_val, (int, float)) else (target if curr_val is True else 0)
            if curr_count >= target:
                new_val = 0
                is_completed = False
                is_just_completed = False
            else:
                new_val = curr_count + 1
                is_completed = (new_val >= target)
                is_just_completed = (new_val == target)
            self.records[ds][task_name] = new_val

        self.save_data()
        return new_val, is_completed, is_just_completed

    def decrement_task(self, date_obj, task_name):
        """Sağ tıklandığında: sayaçlı görevde sayıyı 1 azaltır (-1), normal görevde ise işareti kaldırır (False)."""
        target = self.get_task_target(task_name)
        ds = date_obj.strftime("%Y-%m-%d")
        self.records.setdefault(ds, {})
        curr_val = self.records[ds].get(task_name, 0 if target > 1 else False)

        if target <= 1:
            new_val = False
            is_completed = False
        else:
            curr_count = curr_val if isinstance(curr_val, (int, float)) else (target if curr_val is True else 0)
            new_val = max(0, curr_count - 1)
            is_completed = (new_val >= target)

        self.records[ds][task_name] = new_val
        self.save_data()
        return new_val, is_completed

    def set_task_state(self, date_obj, task_name, value):
        ds = date_obj.strftime("%Y-%m-%d")
        self.records.setdefault(ds, {})[task_name] = value
        self.save_data()

    def set_score(self, date_obj, score_type, value):
        ds = date_obj.strftime("%Y-%m-%d")
        if score_type == "moral":
            self.moral_records[ds] = value
        else:
            self.efektiflik_records[ds] = value
        self.save_data()

    # ---------- OYUNLAŞTIRMA (XP, SEVİYE & KALKAN) ----------
    def calculate_total_xp(self):
        """Tüm tamamlanan görevler ve bonuslarla toplam XP'yi hesaplar."""
        total_xp = int(self.settings.get("bonus_xp", 0))
        for ds, day_rec in self.records.items():
            if not isinstance(day_rec, dict):
                continue
            day_done = 0
            day_total = len(self.tasks)
            for t in self.tasks:
                target = self.get_task_target(t)
                val = day_rec.get(t, False)
                if target <= 1:
                    if val:
                        total_xp += 15
                        day_done += 1
                else:
                    cnt = int(val) if isinstance(val, (int, float)) else (target if val is True else 0)
                    total_xp += (cnt * 2)
                    if cnt >= target:
                        total_xp += 10
                        day_done += 1
            if day_total > 0 and day_done == day_total:
                total_xp += 50
        return max(0, total_xp)

    def calculate_streak(self):
        """Bugünden veya dünden geriye doğru kesintisiz görev yapılan ardışık gün serisini hesaplar (Kalkan korumalı)."""
        streak = 0
        cur_d = self.today
        today_done = sum(1 for t in self.tasks if self.get_task_state(cur_d, t)) if self.tasks else 0
        if today_done == 0:
            cur_d = self.today - datetime.timedelta(days=1)

        freezes = self.settings.get("streak_freezes", 1)

        while True:
            has_done = any(self.get_task_state(cur_d, t) for t in self.tasks) if self.tasks else False
            if has_done:
                streak += 1
                cur_d -= datetime.timedelta(days=1)
            elif freezes > 0 and streak > 0:
                # Kalkan bu 1 günlük kaçırmayı seriyi bozmadan korur
                freezes -= 1
                cur_d -= datetime.timedelta(days=1)
            else:
                break
        return streak

    def get_level_data(self):
        xp = self.calculate_total_xp()
        return get_level_info(xp)

    def check_streak_freeze(self):
        """Haftalık 1 kalkan hakkını kontrol eder."""
        try:
            curr_week = self.today.isocalendar()[1]
            if self.settings.get("last_freeze_week") != curr_week:
                self.settings["streak_freezes"] = 1
                self.settings["last_freeze_week"] = curr_week
                self.save_data()
        except Exception:
            pass

    def check_daily_completion(self):
        """Bugünün tüm görevleri bittiğinde (%100) zafer kutlaması tetikler."""
        done, total = self.get_today_progress()
        if total > 0 and done == total:
            today_str = self.today.strftime("%Y-%m-%d")
            if self.settings.get("last_celebrated_date") != today_str:
                self.settings["last_celebrated_date"] = today_str
                self.save_data()
                self.trigger_celebration_popup()

    def trigger_celebration_popup(self):
        """%100 Gün Tamamlama Zafer Penceresi."""
        theme = self.get_theme()
        play_notification_sound()

        popup = ctk.CTkToplevel(self)
        popup.title("🎉 Günün Zaferi!")
        popup.geometry("380x210")
        popup.resizable(False, False)
        popup.transient(self)
        popup.attributes("-topmost", True)
        popup.configure(fg_color=theme["bg"])

        try:
            px = self.winfo_x() + (self.winfo_width() - 380) // 2
            py = self.winfo_y() + (self.winfo_height() - 210) // 2
            popup.geometry(f"380x210+{max(0, px)}+{max(0, py)}")
        except Exception:
            pass

        card = ctk.CTkFrame(popup, fg_color=theme["card"], corner_radius=14, border_width=2, border_color=theme["done"])
        card.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(card, text="🎉  TEBRİKLER!", font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=theme["done"]).pack(pady=(16, 4))
        ctk.CTkLabel(card, text="Bugünkü tüm görevlerini (%100) başarıyla tamamladın!",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=theme["text"]).pack(pady=(0, 6))

        xp_badge = ctk.CTkFrame(card, fg_color=theme["card_alt"], corner_radius=8)
        xp_badge.pack(pady=4)
        ctk.CTkLabel(xp_badge, text="⭐ +50 Bonus XP Kazanıldı!", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=theme.get("moral_color", "#D98A48")).pack(padx=14, pady=4)

        ctk.CTkButton(card, text="Harika!", width=110, height=30, corner_radius=10,
                      fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"],
                      text_color=theme["text"], font=ctk.CTkFont(size=11, weight="bold"),
                      command=popup.destroy).pack(pady=(12, 10))

        popup.after(6000, lambda: popup.destroy() if popup.winfo_exists() else None)

    # ---------- TEMA ----------
    def get_theme(self):
        mode = self.settings.get("mode", "light")
        if mode == "light":
            name = self.settings.get("light_theme", "Matcha & Adaçayı")
            if name not in THEMES["light"]:
                name = list(THEMES["light"].keys())[0]
            return THEMES["light"][name]
        else:
            name = self.settings.get("dark_theme", "Gece Yarısı")
            if name not in THEMES["dark"]:
                name = list(THEMES["dark"].keys())[0]
            return THEMES["dark"][name]

    def apply_theme(self, mode_changed=False):
        theme = self.get_theme()
        mode = self.settings.get("mode", "light")

        if mode_changed:
            ctk.set_appearance_mode("Light" if mode == "light" else "Dark")

        self.configure(fg_color=theme["bg"])

        # Header
        self.title_label.configure(text_color=theme["text"])
        self.clock_label.configure(text_color=theme["accent"])

        # Level & Gamification
        if hasattr(self, "level_badge_lbl"):
            self.level_badge_lbl.configure(text_color=theme.get("accent", "#FB7185"))
            self.xp_bar.configure(fg_color=theme["progress_bg"], progress_color=theme.get("moral_color", "#D98A48"))
            self.xp_label.configure(text_color=theme["text_secondary"])

            if hasattr(self, "streak_badge"):
                self.streak_badge.configure(fg_color=theme["card_alt"])
                self.streak_lbl.configure(text_color=theme.get("accent", "#FB7185"))

                self.shield_badge.configure(fg_color=theme["card_alt"])
                self.shield_lbl.configure(text_color=theme.get("efektiflik_color", "#957DC7"))

        # Mode switch
        self.mode_switch.configure(
            fg_color=theme["switch_off"], progress_color=theme["switch_on"],
            button_color=theme["switch_btn"], button_hover_color=theme["switch_btn_hover"])
        self.mode_icon_label.configure(text_color=theme["text_secondary"])

        # Buttons
        self.settings_btn.configure(fg_color=theme["btn_settings"], hover_color=theme["btn_settings_hover"],
                                    text_color=theme["text"])
        if hasattr(self, "sticky_btn"):
            self.sticky_btn.configure(fg_color=theme["card_alt"], hover_color=theme["btn_primary_hover"], text_color=theme["text"])
        if hasattr(self, "sticky_widget") and self.sticky_widget and self.sticky_widget.winfo_exists():
            self.sticky_widget.apply_theme()

        # Top Frame / Chart Containers
        self.top_frame.configure(fg_color=theme["card"])
        for cf in (self.chart1_frame, self.chart2_frame, self.chart3_frame):
            cf.configure(fg_color=theme["chart_bg"])

        # Chart Nav Controls
        self.chart1_title_lbl.configure(text_color=theme["text"])
        self.chart1_prev_btn.configure(fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"], text_color=theme["text"])
        self.chart1_next_btn.configure(fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"], text_color=theme["text"])

        self.chart2_title_lbl.configure(text_color=theme["text"])
        self.chart2_prev_btn.configure(fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"], text_color=theme["text"])
        self.chart2_next_btn.configure(fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"], text_color=theme["text"])

        self.chart3_title_lbl.configure(text_color=theme["text"])

        # Stat cards
        if hasattr(self, "stat_card1"):
            for sc in (self.stat_card1, self.stat_card2, self.stat_card3):
                sc.configure(fg_color=theme["card_alt"])
            self.stat_c1_title.configure(text_color=theme["text_secondary"])
            self.stat_c2_title.configure(text_color=theme["text_secondary"])
            self.stat_c3_title.configure(text_color=theme["text_secondary"])
            self.stat_c1_val.configure(text_color=theme.get("accent", "#FB7185"))
            self.stat_c2_val.configure(text_color=theme.get("done", "#789262"))
            self.stat_c3_val.configure(text_color=theme.get("efektiflik_color", "#957DC7"))

        # Bottom Frame & Nav Capsule
        self.bottom_frame.configure(fg_color=theme["card"])
        if hasattr(self, "table_nav_center"):
            self.table_nav_center.configure(fg_color=theme["card_alt"])
            self.table_prev_btn.configure(text_color=theme["text"], hover_color=theme["btn_primary_hover"])
            self.table_next_btn.configure(text_color=theme["text"], hover_color=theme["btn_primary_hover"])
            self.table_month_lbl.configure(text_color=theme["text"])

        # Render Table & Charts (ultra-fast)
        self.render_table()
        self.update_charts()
        self.update_progress()

    def toggle_mode(self):
        play_button_sound()
        mode = self.settings.get("mode", "light")
        new_mode = "dark" if mode == "light" else "light"
        self.settings["mode"] = new_mode
        self.save_data()

        icon = "🌙" if new_mode == "dark" else "☀️"
        self.mode_icon_label.configure(text=icon)
        self.apply_theme(mode_changed=True)

    # ---------- ARAYÜZ ----------
    def setup_ui(self):
        theme = self.get_theme()

        # ─── BAŞLIK (SOL BAŞLIK, ORTA SEVİYE & ROZETLER, SAĞ KONTROLLER) ───
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(side="top", fill="x", padx=16, pady=(10, 4))
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=2)
        self.header_frame.grid_columnconfigure(2, weight=1)

        # SOL: Başlık
        self.left_header = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.left_header.grid(row=0, column=0, sticky="w")

        self.title_label = ctk.CTkLabel(
            self.left_header, text="📋 Görev & Alışkanlık Takibi",
            font=ctk.CTkFont(size=19, weight="bold"), text_color=theme["text"])
        self.title_label.pack(side="left")

        # ORTA: Seviye Barı & Rozetler (Tam Ortalanmış)
        self.center_header = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.center_header.grid(row=0, column=1)

        self.level_badge_lbl = ctk.CTkLabel(
            self.center_header, text="⭐ Lvl 1: Çaylak",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=theme.get("accent", "#FB7185")
        )
        self.level_badge_lbl.pack(side="left", padx=(0, 8))

        self.xp_bar = ctk.CTkProgressBar(
            self.center_header, width=200, height=12,
            corner_radius=6,
            fg_color=theme["progress_bg"],
            progress_color=theme.get("moral_color", "#D98A48")
        )
        self.xp_bar.pack(side="left", padx=(0, 8))
        self.xp_bar.set(0)

        self.xp_label = ctk.CTkLabel(
            self.center_header, text="0/120 XP",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=theme["text_secondary"]
        )
        self.xp_label.pack(side="left", padx=(0, 10))

        # 1. Seri (Streak)
        self.streak_badge = ctk.CTkFrame(self.center_header, fg_color=theme["card_alt"], corner_radius=8)
        self.streak_badge.pack(side="left", padx=(0, 6))
        self.streak_lbl = ctk.CTkLabel(
            self.streak_badge, text="🔥 0 Gün",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=theme.get("accent", "#FB7185")
        )
        self.streak_lbl.pack(padx=7, pady=2)

        # 2. Kalkan (Shield)
        self.shield_badge = ctk.CTkFrame(self.center_header, fg_color=theme["card_alt"], corner_radius=8)
        self.shield_badge.pack(side="left")
        self.shield_lbl = ctk.CTkLabel(
            self.shield_badge, text="🛡️ 1 Kalkan",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=theme.get("efektiflik_color", "#957DC7")
        )
        self.shield_lbl.pack(padx=7, pady=2)

        # SAĞ: Saat, Switch, Ayarlar
        self.right_header = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.right_header.grid(row=0, column=2, sticky="e")

        self.clock_label = ctk.CTkLabel(self.right_header, text="",
                                        font=ctk.CTkFont(size=11, weight="bold"),
                                        text_color=theme["accent"])
        self.clock_label.pack(side="left", padx=(0, 10))

        # Dark / Light switch
        mode = self.settings.get("mode", "light")
        self.mode_icon_label = ctk.CTkLabel(self.right_header,
                                            text="🌙" if mode == "dark" else "☀️",
                                            font=ctk.CTkFont(size=15),
                                            text_color=theme["text_secondary"])
        self.mode_icon_label.pack(side="left", padx=(0, 4))

        self.mode_switch = ctk.CTkSwitch(
            self.right_header, text="", width=40,
            fg_color=theme["switch_off"], progress_color=theme["switch_on"],
            button_color=theme["switch_btn"], button_hover_color=theme["switch_btn_hover"],
            command=self.toggle_mode)
        if mode == "dark":
            self.mode_switch.select()
        self.mode_switch.pack(side="left", padx=(0, 10))

        # Kayan Mini Widget Butonu
        self.sticky_btn = ctk.CTkButton(
            self.right_header, text="📌 Mini", width=68, height=30,
            fg_color=theme["card_alt"], hover_color=theme["btn_primary_hover"],
            text_color=theme["text"], corner_radius=12, font=ctk.CTkFont(size=11, weight="bold"),
            command=self.toggle_sticky_mode)
        self.sticky_btn.pack(side="left", padx=(0, 6))

        # Ayarlar butonu (Yumuşak hap şeklinde)
        self.settings_btn = ctk.CTkButton(
            self.right_header, text="⚙ Ayarlar", width=95, height=30,
            fg_color=theme["btn_settings"], hover_color=theme["btn_settings_hover"],
            text_color=theme["text"], corner_radius=12, font=ctk.CTkFont(size=11, weight="bold"),
            command=self.open_settings)
        self.settings_btn.pack(side="left")

        # ─── ÜST PANEL (GRAFİKLER) ───
        self.top_frame = ctk.CTkFrame(self, corner_radius=16, fg_color=theme["card"])
        self.top_frame.pack(side="top", fill="x", padx=15, pady=(8, 4))
        self.top_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # 1. Grafik Kartı (Haftalık Günler)
        self.chart1_frame = ctk.CTkFrame(self.top_frame, fg_color=theme["chart_bg"], corner_radius=12)
        self.chart1_frame.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")

        chart1_header = ctk.CTkFrame(self.chart1_frame, fg_color="transparent")
        chart1_header.pack(fill="x", padx=8, pady=(6, 2))

        self.chart1_prev_btn = ctk.CTkButton(
            chart1_header, text="◄", width=28, height=22,
            fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"],
            text_color=theme["text"], corner_radius=11, font=ctk.CTkFont(family="Arial", size=10, weight="bold"),
            command=lambda: self.navigate_week(-1))
        self.chart1_prev_btn.pack(side="left")

        self.chart1_title_lbl = ctk.CTkLabel(
            chart1_header, text="Bu Hafta",
            font=ctk.CTkFont(size=11, weight="bold"), text_color=theme["text"])
        self.chart1_title_lbl.pack(side="left", expand=True)

        self.chart1_next_btn = ctk.CTkButton(
            chart1_header, text="►", width=28, height=22,
            fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"],
            text_color=theme["text"], corner_radius=11, font=ctk.CTkFont(family="Arial", size=10, weight="bold"),
            command=lambda: self.navigate_week(1))
        self.chart1_next_btn.pack(side="right")

        # 2. Grafik Kartı (Aylık Tamamlanma - Donut Grafik)
        self.chart2_frame = ctk.CTkFrame(self.top_frame, fg_color=theme["chart_bg"], corner_radius=12)
        self.chart2_frame.grid(row=0, column=1, padx=6, pady=6, sticky="nsew")

        chart2_header = ctk.CTkFrame(self.chart2_frame, fg_color="transparent")
        chart2_header.pack(fill="x", padx=8, pady=(6, 2))

        self.chart2_prev_btn = ctk.CTkButton(
            chart2_header, text="◄", width=28, height=22,
            fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"],
            text_color=theme["text"], corner_radius=11, font=ctk.CTkFont(family="Arial", size=10, weight="bold"),
            command=lambda: self.navigate_month(-1))
        self.chart2_prev_btn.pack(side="left")

        self.chart2_title_lbl = ctk.CTkLabel(
            chart2_header, text=f"Aylık Odak ({TURKISH_MONTHS[self.chart_month]})",
            font=ctk.CTkFont(size=11, weight="bold"), text_color=theme["text"])
        self.chart2_title_lbl.pack(side="left", expand=True)

        self.chart2_next_btn = ctk.CTkButton(
            chart2_header, text="►", width=28, height=22,
            fg_color=theme["btn_primary"], hover_color=theme["btn_primary_hover"],
            text_color=theme["text"], corner_radius=11, font=ctk.CTkFont(family="Arial", size=10, weight="bold"),
            command=lambda: self.navigate_month(1))
        self.chart2_next_btn.pack(side="right")

        # 3. Kart (🏆 Alışkanlık & Başarı Özeti)
        self.chart3_frame = ctk.CTkFrame(self.top_frame, fg_color=theme["chart_bg"], corner_radius=12)
        self.chart3_frame.grid(row=0, column=2, padx=6, pady=6, sticky="nsew")

        chart3_header = ctk.CTkFrame(self.chart3_frame, fg_color="transparent")
        chart3_header.pack(fill="x", padx=8, pady=(6, 2))

        self.chart3_title_lbl = ctk.CTkLabel(
            chart3_header, text="🏆 Alışkanlık Özeti",
            font=ctk.CTkFont(size=11, weight="bold"), text_color=theme["text"])
        self.chart3_title_lbl.pack(fill="x", expand=True, pady=1)

        self.stats_cards_container = ctk.CTkFrame(self.chart3_frame, fg_color="transparent")
        self.stats_cards_container.pack(fill="both", expand=True, padx=8, pady=(4, 6))
        self.stats_cards_container.grid_rowconfigure((0, 1, 2), weight=1)
        self.stats_cards_container.grid_columnconfigure(0, weight=1)

        # 1. Mini Kart: En Uzun Seri
        self.stat_card1 = ctk.CTkFrame(self.stats_cards_container, fg_color=theme["card_alt"], corner_radius=8)
        self.stat_card1.grid(row=0, column=0, sticky="nsew", pady=2)
        self.stat_c1_title = ctk.CTkLabel(self.stat_card1, text="👑 En Uzun Seri", font=ctk.CTkFont(size=10), text_color=theme["text_secondary"])
        self.stat_c1_title.pack(side="left", padx=10)
        self.stat_c1_val = ctk.CTkLabel(self.stat_card1, text="🔥 0 Gün", font=ctk.CTkFont(size=11, weight="bold"), text_color=theme.get("accent", "#FB7185"))
        self.stat_c1_val.pack(side="right", padx=10)

        # 2. Mini Kart: Bu Ay Tamamlanan
        self.stat_card2 = ctk.CTkFrame(self.stats_cards_container, fg_color=theme["card_alt"], corner_radius=8)
        self.stat_card2.grid(row=1, column=0, sticky="nsew", pady=2)
        self.stat_c2_title = ctk.CTkLabel(self.stat_card2, text="⚡ Bu Ay Başarı", font=ctk.CTkFont(size=10), text_color=theme["text_secondary"])
        self.stat_c2_title.pack(side="left", padx=10)
        self.stat_c2_val = ctk.CTkLabel(self.stat_card2, text="0 Görev (%0)", font=ctk.CTkFont(size=11, weight="bold"), text_color=theme.get("done", "#789262"))
        self.stat_c2_val.pack(side="right", padx=10)

        # 3. Mini Kart: En İstikrarlı Alışkanlık
        self.stat_card3 = ctk.CTkFrame(self.stats_cards_container, fg_color=theme["card_alt"], corner_radius=8)
        self.stat_card3.grid(row=2, column=0, sticky="nsew", pady=2)
        self.stat_c3_title = ctk.CTkLabel(self.stat_card3, text="🎯 En İstikrarlı", font=ctk.CTkFont(size=10), text_color=theme["text_secondary"])
        self.stat_c3_title.pack(side="left", padx=10)
        self.stat_c3_val = ctk.CTkLabel(self.stat_card3, text="-", font=ctk.CTkFont(size=10, weight="bold"), text_color=theme.get("efektiflik_color", "#957DC7"))
        self.stat_c3_val.pack(side="right", padx=10)

        # ─── ALT PANEL (ULTRA-HIZLI CANVAS TABLO) ───
        self.bottom_frame = ctk.CTkFrame(self, corner_radius=16, fg_color=theme["card"])
        self.bottom_frame.pack(side="bottom", fill="both", expand=True, padx=15, pady=(4, 12))

        self.table_canvas = tk.Canvas(
            self.bottom_frame,
            bg=theme["card"],
            highlightthickness=0,
            bd=0
        )
        self.table_canvas.pack(side="top", fill="both", expand=True, padx=12, pady=(10, 2))

        # Alt Ay Gezinme Kapsülü (Ultra-Minimalist Lofi Kapsül)
        self.table_nav_frame = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.table_nav_frame.pack(side="bottom", fill="x", pady=(0, 6))

        self.table_nav_center = ctk.CTkFrame(self.table_nav_frame, fg_color=theme["card_alt"], corner_radius=12)
        self.table_nav_center.pack(anchor="center")

        self.table_prev_btn = ctk.CTkButton(
            self.table_nav_center, text="◄", width=24, height=20,
            fg_color="transparent", hover_color=theme["btn_primary_hover"],
            text_color=theme["text"], corner_radius=10, font=ctk.CTkFont(family="Arial", size=9, weight="bold"),
            command=lambda: self.navigate_table_month(-1))
        self.table_prev_btn.pack(side="left", padx=(3, 1), pady=2)

        self.table_month_lbl = ctk.CTkLabel(
            self.table_nav_center, text=f"{TURKISH_MONTHS[self.table_month]} {self.table_year}",
            font=ctk.CTkFont(size=10, weight="bold"), text_color=theme["text"],
            cursor="hand2"
        )
        self.table_month_lbl.pack(side="left", padx=8, pady=2)
        self.table_month_lbl.bind("<Button-1>", lambda e: self.reset_to_current_month())

        self.table_next_btn = ctk.CTkButton(
            self.table_nav_center, text="►", width=24, height=20,
            fg_color="transparent", hover_color=theme["btn_primary_hover"],
            text_color=theme["text"], corner_radius=10, font=ctk.CTkFont(family="Arial", size=9, weight="bold"),
            command=lambda: self.navigate_table_month(1))
        self.table_next_btn.pack(side="left", padx=(1, 3), pady=2)

        self.table_canvas.bind("<Configure>", lambda e: self.render_table())
        self.table_canvas.bind("<Button-1>", self.on_table_click)
        self.table_canvas.bind("<Button-3>", self.on_table_right_click)
        self.table_canvas.bind("<Motion>", self.on_table_motion)

    def open_settings(self):
        play_button_sound()
        SettingsWindow(self)

    # ---------- SAAT (OPTİMİZE EDİLMİŞ) ----------
    def update_clock(self):
        if hasattr(self, "_clock_job") and self._clock_job:
            try:
                self.after_cancel(self._clock_job)
            except Exception:
                pass
            self._clock_job = None

        now = datetime.datetime.now()
        new_today = now.date()
        if new_today != self.today:
            self.today = new_today
            self.task_snooze_counts.clear()
            self.today_dismissed_tasks.clear()
            self.current_monday = self.today - datetime.timedelta(days=self.today.weekday())
            self.selected_monday = self.current_monday
            self.week_dates = [self.current_monday + datetime.timedelta(days=i) for i in range(7)]
            self.render_table()
            self.update_charts()

        month_name = TURKISH_MONTHS.get(now.month, "")
        self.clock_label.configure(text=f"{now.day} {month_name} {now.year}  |  {now.strftime('%H:%M:%S')}")

        if self.winfo_viewable():
            self._clock_job = self.after(1000, self.update_clock)
        else:
            self._clock_job = self.after(60000, self.update_clock)

    # ---------- PROGRESS ----------
    def get_today_progress(self):
        if not self.tasks:
            return 0, 0
        done = sum(1 for t in self.tasks if self.get_task_state(self.today, t))
        return done, len(self.tasks)

    def update_progress(self):
        # Update Level & XP Bar
        if hasattr(self, "xp_bar"):
            lvl_info = self.get_level_data()
            self.level_badge_lbl.configure(text=f"{lvl_info['icon']} Lvl {lvl_info['level']}: {lvl_info['title']}")
            self.xp_bar.set(lvl_info["ratio"])
            self.xp_label.configure(text=f"{lvl_info['current_xp']}/{lvl_info['next_xp']} XP")

            if hasattr(self, "streak_lbl"):
                streak_days = self.calculate_streak()
                self.streak_lbl.configure(text=f"🔥 {streak_days} Gün Seri" if streak_days > 0 else "🔥 0 Gün")

            if hasattr(self, "shield_lbl"):
                freezes = self.settings.get("streak_freezes", 1)
                self.shield_lbl.configure(text=f"🛡️ {freezes} Kalkan" if freezes > 0 else "🛡️ Kalkan Yok")

        if hasattr(self, "sticky_widget") and self.sticky_widget and self.sticky_widget.winfo_exists():
            self.sticky_widget.render_tasks()

    # ---------- ULTRA-HIZLI VE YUMUŞAK PASTEL AYLIK TABLO ----------
    def render_table(self):
        theme = self.get_theme()
        canvas = self.table_canvas
        canvas.delete("all")
        canvas.configure(bg=theme["card"])

        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 100:
            w = 1200
        if h < 100:
            h = 240

        year = getattr(self, "table_year", self.today.year)
        month = getattr(self, "table_month", self.today.month)
        num_days = calendar.monthrange(year, month)[1]

        task_col_w = 160
        avail_w = w - task_col_w - 20
        col_w = max(26, avail_w / num_days)

        header_h = 46
        row_h = 28
        sep_h = 10
        total_task_rows = len(self.tasks)

        # Geometri bilgisi (Tıklama hesaplaması için)
        self._table_geo = {
            "task_col_w": task_col_w,
            "col_w": col_w,
            "header_h": header_h,
            "row_h": row_h,
            "num_days": num_days,
            "year": year,
            "month": month,
            "moral_y": header_h + total_task_rows * row_h + sep_h,
            "efektiflik_y": header_h + total_task_rows * row_h + sep_h + row_h,
        }

        # 1. Başlık: Ay İsmi
        canvas.create_text(
            12, 16, text=f"📅  {TURKISH_MONTHS[month]} {year}",
            anchor="w", font=("Segoe UI", 12, "bold"), fill=theme["header_text"]
        )

        # 2. Görevler Kolon Başlığı
        canvas.create_text(
            12, 35, text="Görevler",
            anchor="w", font=("Segoe UI", 9, "bold"), fill=theme["text_secondary"]
        )

        # 3. Gün Sütunları ve Vurguları
        total_table_h = header_h + (total_task_rows + 2) * row_h + sep_h + 8

        for day in range(1, num_days + 1):
            d_obj = datetime.date(year, month, day)
            wd = d_obj.weekday()
            is_today = (d_obj == self.today)
            is_weekend = (wd >= 5)

            x1 = task_col_w + (day - 1) * col_w
            x2 = x1 + col_w
            cx = (x1 + x2) / 2

            # Bugün Vurgu Kolonu
            if is_today:
                draw_round_rect(
                    canvas, x1 + 2, 2, x2 - 2, total_table_h, r=6,
                    fill=theme["today_col"], outline=""
                )
                draw_round_rect(
                    canvas, x1 + 4, 1, x2 - 4, 4, r=2,
                    fill=theme["today_header"], outline=""
                )
            elif is_weekend:
                draw_round_rect(
                    canvas, x1 + 2, 2, x2 - 2, total_table_h, r=6,
                    fill=theme["weekend_col"], outline=""
                )

            # Gün Numarası & Gün Kısaltması
            header_color = theme["today_header"] if is_today else (theme["accent"] if is_weekend else theme["text_secondary"])
            font_weight = "bold" if is_today else "normal"

            canvas.create_text(
                cx, 22, text=str(day),
                font=("Segoe UI", 9, "bold" if is_today else "normal"),
                fill=header_color
            )
            canvas.create_text(
                cx, 35, text=SHORT_DAYS[wd],
                font=("Segoe UI", 8, font_weight),
                fill=header_color
            )

        # 4. Görev Satırları ve Kutucuklar / Sayaç Rozetleri
        for r_idx, task_name in enumerate(self.tasks):
            y_top = header_h + r_idx * row_h
            y_bot = y_top + row_h
            cy = (y_top + y_bot) / 2

            # Alternatif Satır Arka Planı
            if r_idx % 2 == 0:
                draw_round_rect(
                    canvas, 4, y_top + 1, w - 4, y_bot - 1, r=6,
                    fill=theme["card_alt"], outline=""
                )

            target = self.get_task_target(task_name)

            # Görev Adı Metni
            canvas.create_text(
                12, cy, text=task_name,
                anchor="w", font=("Segoe UI", 9, "normal"), fill=theme["text"]
            )

            # Her Gün İçin Kutu veya Sayaç Rozeti
            for day in range(1, num_days + 1):
                d_obj = datetime.date(year, month, day)
                is_today = (d_obj == self.today)

                x1 = task_col_w + (day - 1) * col_w
                x2 = x1 + col_w
                cx = (x1 + x2) / 2

                if target <= 1:
                    is_checked = self.get_task_state(d_obj, task_name)
                    box_size = 18
                    bx1 = cx - box_size / 2
                    by1 = cy - box_size / 2
                    bx2 = cx + box_size / 2
                    by2 = cy + box_size / 2

                    if is_checked:
                        draw_round_rect(
                            canvas, bx1, by1, bx2, by2, r=4,
                            fill=theme["done"], outline=theme["done"]
                        )
                        check_fg = "#FFFFFF" if self.settings.get("mode", "light") == "dark" else "#1A251C"
                        canvas.create_text(
                            cx, cy, text="✔",
                            font=("Segoe UI", 9, "bold"),
                            fill=check_fg
                        )
                    else:
                        border_c = theme["today_header"] if is_today else theme["checkbox_border"]
                        draw_round_rect(
                            canvas, bx1, by1, bx2, by2, r=4,
                            fill=theme["checkbox_bg"], outline=border_c, width=1.5 if is_today else 1
                        )
                else:
                    # Sayaçlı Görev Rozeti (örn: 3/8)
                    cnt = self.get_task_count(d_obj, task_name)
                    pw = max(22, min(col_w - 4, 30))
                    ph = 18
                    px1 = cx - pw / 2
                    py1 = cy - ph / 2
                    px2 = cx + pw / 2
                    py2 = cy + ph / 2

                    if cnt >= target:
                        draw_round_rect(
                            canvas, px1, py1, px2, py2, r=5,
                            fill=theme["done"], outline=theme["done"]
                        )
                        txt_fg = "#FFFFFF" if self.settings.get("mode", "light") == "dark" else "#1A251C"
                        canvas.create_text(
                            cx, cy, text=f"✓{cnt}",
                            font=("Segoe UI", 8, "bold"), fill=txt_fg
                        )
                    elif cnt > 0:
                        draw_round_rect(
                            canvas, px1, py1, px2, py2, r=5,
                            fill=theme.get("today_col", theme["card_alt"]),
                            outline=theme.get("accent", "#FB7185"), width=1.5
                        )
                        canvas.create_text(
                            cx, cy, text=f"{cnt}/{target}",
                            font=("Segoe UI", 7, "bold"), fill=theme["text"]
                        )
                    else:
                        border_c = theme["today_header"] if is_today else theme["checkbox_border"]
                        draw_round_rect(
                            canvas, px1, py1, px2, py2, r=5,
                            fill=theme["checkbox_bg"], outline=border_c, width=1.5 if is_today else 1
                        )
                        canvas.create_text(
                            cx, cy, text=f"0/{target}",
                            font=("Segoe UI", 7, "normal"),
                            fill=theme["today_header"] if is_today else theme["text_secondary"]
                        )

        # 5. Ayırıcı Çizgi
        sep_y = header_h + total_task_rows * row_h + (sep_h / 2)
        canvas.create_line(
            8, sep_y, w - 8, sep_y,
            fill=theme["separator"], width=1
        )

        # 6. Moral Satırı
        moral_y = self._table_geo["moral_y"]
        canvas.create_text(
            12, moral_y + row_h / 2, text="😊 Moral",
            anchor="w", font=("Segoe UI", 9, "bold"), fill=theme["moral_color"]
        )

        for day in range(1, num_days + 1):
            d_obj = datetime.date(year, month, day)
            val = str(self.moral_records.get(d_obj.strftime("%Y-%m-%d"), "-"))
            is_today = (d_obj == self.today)

            x1 = task_col_w + (day - 1) * col_w
            x2 = x1 + col_w
            cx = (x1 + x2) / 2
            cy = moral_y + row_h / 2

            if val != "-":
                draw_round_rect(
                    canvas, cx - 10, cy - 9, cx + 10, cy + 9, r=6,
                    fill=theme["moral_color"], outline=""
                )
                canvas.create_text(
                    cx, cy, text=val,
                    font=("Segoe UI", 8, "bold"), fill="#FFFFFF"
                )
            else:
                canvas.create_text(
                    cx, cy, text="-",
                    font=("Segoe UI", 8, "normal"),
                    fill=theme["moral_color"] if is_today else theme["text_secondary"]
                )

        # 7. Efektiflik Satırı
        efekt_y = self._table_geo["efektiflik_y"]
        canvas.create_text(
            12, efekt_y + row_h / 2, text="⚡ Efektiflik",
            anchor="w", font=("Segoe UI", 9, "bold"), fill=theme["efektiflik_color"]
        )

        for day in range(1, num_days + 1):
            d_obj = datetime.date(year, month, day)
            val = str(self.efektiflik_records.get(d_obj.strftime("%Y-%m-%d"), "-"))
            is_today = (d_obj == self.today)

            x1 = task_col_w + (day - 1) * col_w
            x2 = x1 + col_w
            cx = (x1 + x2) / 2
            cy = efekt_y + row_h / 2

            if val != "-":
                draw_round_rect(
                    canvas, cx - 10, cy - 9, cx + 10, cy + 9, r=6,
                    fill=theme["efektiflik_color"], outline=""
                )
                canvas.create_text(
                    cx, cy, text=val,
                    font=("Segoe UI", 8, "bold"), fill="#FFFFFF"
                )
            else:
                canvas.create_text(
                    cx, cy, text="-",
                    font=("Segoe UI", 8, "normal"),
                    fill=theme["efektiflik_color"] if is_today else theme["text_secondary"]
                )

    # ---------- TABLO TIKLAMA İŞLEMLERİ (SADECE BUGÜN TIKLANABİLİR) ----------
    def on_table_click(self, event):
        if not hasattr(self, "_table_geo"):
            return

        geo = self._table_geo
        x, y = event.x, event.y

        if x < geo["task_col_w"]:
            return

        day_idx = int((x - geo["task_col_w"]) / geo["col_w"])
        day = day_idx + 1

        if not (1 <= day <= geo["num_days"]):
            return

        d_obj = datetime.date(geo["year"], geo["month"], day)

        # KURAL: Sadece BUGÜNÜN günü tıklanabilir ve işaretlenebilir
        if d_obj != self.today:
            return

        # 1. Görev Satırlarına Tıklama (Bugün)
        if geo["header_h"] <= y < geo["header_h"] + len(self.tasks) * geo["row_h"]:
            task_idx = int((y - geo["header_h"]) / geo["row_h"])
            if 0 <= task_idx < len(self.tasks):
                task_name = self.tasks[task_idx]
                new_val, is_completed, is_just_completed = self.increment_task(d_obj, task_name)
                play_task_sound(is_checking=is_completed)

                if is_completed:
                    if hasattr(self, "task_snooze_counts") and task_name in self.task_snooze_counts:
                        self.task_snooze_counts[task_name] = 0
                    if hasattr(self, "active_popups") and task_name in self.active_popups:
                        try:
                            self.active_popups[task_name].destroy()
                        except Exception:
                            pass

                self.render_table()
                self.update_charts()
                self.update_progress()
                self.check_daily_completion()
                return

        # 2. Moral Satırına Tıklama (Bugün)
        if geo["moral_y"] <= y < geo["moral_y"] + geo["row_h"]:
            play_rating_sound()
            values = ["-", "1", "2", "3", "4", "5"]
            ds = d_obj.strftime("%Y-%m-%d")
            curr_val = str(self.moral_records.get(ds, "-"))
            next_idx = (values.index(curr_val) + 1) % len(values) if curr_val in values else 0
            self.set_score(d_obj, "moral", values[next_idx])
            self.render_table()
            self.update_charts()
            return

        # 3. Efektiflik Satırına Tıklama (Bugün)
        if geo["efektiflik_y"] <= y < geo["efektiflik_y"] + geo["row_h"]:
            play_rating_sound()
            values = ["-", "1", "2", "3", "4", "5"]
            ds = d_obj.strftime("%Y-%m-%d")
            curr_val = str(self.efektiflik_records.get(ds, "-"))
            next_idx = (values.index(curr_val) + 1) % len(values) if curr_val in values else 0
            self.set_score(d_obj, "efektiflik", values[next_idx])
            self.render_table()
            self.update_charts()
            return

    # ---------- TABLO SAĞ TIKLAMA (SAYACI AZALT / İŞARETİ KALDIR) ----------
    def on_table_right_click(self, event):
        if not hasattr(self, "_table_geo"):
            return

        geo = self._table_geo
        x, y = event.x, event.y

        if x < geo["task_col_w"]:
            return

        day_idx = int((x - geo["task_col_w"]) / geo["col_w"])
        day = day_idx + 1

        if not (1 <= day <= geo["num_days"]):
            return

        d_obj = datetime.date(geo["year"], geo["month"], day)

        if d_obj != self.today:
            return

        # 1. Görev Satırlarına Sağ Tıklama (Sayaç -1 veya İşareti Kaldır)
        if geo["header_h"] <= y < geo["header_h"] + len(self.tasks) * geo["row_h"]:
            task_idx = int((y - geo["header_h"]) / geo["row_h"])
            if 0 <= task_idx < len(self.tasks):
                task_name = self.tasks[task_idx]
                new_val, is_completed = self.decrement_task(d_obj, task_name)
                play_task_sound(is_checking=False)

                self.render_table()
                self.update_charts()
                self.update_progress()
                return

        # 2. Moral Satırına Sağ Tıklama (Geri Say)
        if geo["moral_y"] <= y < geo["moral_y"] + geo["row_h"]:
            play_rating_sound()
            values = ["-", "1", "2", "3", "4", "5"]
            ds = d_obj.strftime("%Y-%m-%d")
            curr_val = str(self.moral_records.get(ds, "-"))
            next_idx = (values.index(curr_val) - 1) % len(values) if curr_val in values else 0
            self.set_score(d_obj, "moral", values[next_idx])
            self.render_table()
            self.update_charts()
            return

        # 3. Efektiflik Satırına Sağ Tıklama (Geri Say)
        if geo["efektiflik_y"] <= y < geo["efektiflik_y"] + geo["row_h"]:
            play_rating_sound()
            values = ["-", "1", "2", "3", "4", "5"]
            ds = d_obj.strftime("%Y-%m-%d")
            curr_val = str(self.efektiflik_records.get(ds, "-"))
            next_idx = (values.index(curr_val) - 1) % len(values) if curr_val in values else 0
            self.set_score(d_obj, "efektiflik", values[next_idx])
            self.render_table()
            self.update_charts()
            return

    def on_table_motion(self, event):
        if not hasattr(self, "_table_geo"):
            return
        geo = self._table_geo
        x, y = event.x, event.y

        desired_cursor = ""
        if x >= geo["task_col_w"]:
            day_idx = int((x - geo["task_col_w"]) / geo["col_w"])
            day = day_idx + 1
            if (1 <= day <= geo["num_days"] and
                    day == self.today.day and
                    geo["month"] == self.today.month and
                    geo["header_h"] <= y <= geo["efektiflik_y"] + geo["row_h"]):
                desired_cursor = "hand2"

        if getattr(self, "_current_table_cursor", None) != desired_cursor:
            self._current_table_cursor = desired_cursor
            self.table_canvas.configure(cursor=desired_cursor)

    # ---------- GRAFİKLER & DASHBOARD (MODERN VE DOLGUN) ----------
    def setup_charts(self):
        # 1. Grafik: Haftalık Trend (Bar)
        self.fig1, self.ax1 = plt.subplots(figsize=(3.4, 1.8), dpi=80)
        self.fig1.subplots_adjust(left=0.12, right=0.96, top=0.86, bottom=0.20)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.chart1_frame)
        self.canvas1.get_tk_widget().pack(fill="both", expand=True, padx=2, pady=2)

        # 2. Grafik: Aylık Tamamlanma (Donut)
        self.fig2, self.ax2 = plt.subplots(figsize=(3.4, 1.8), dpi=80)
        self.fig2.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.08)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.chart2_frame)
        self.canvas2.get_tk_widget().pack(fill="both", expand=True, padx=2, pady=2)

    def get_max_streak(self):
        """Kullanıcının geçmişten bugüne kaydettiği en uzun ardışık gün serisini hesaplar."""
        active_dates = []
        for ds_str in self.records:
            try:
                d_obj = datetime.date.fromisoformat(ds_str)
                if any(self.get_task_state(d_obj, t) for t in self.tasks):
                    active_dates.append(d_obj)
            except Exception:
                pass
        if not active_dates:
            return 0
        active_dates = sorted(set(active_dates))
        max_s = 1
        curr_s = 1
        for i in range(1, len(active_dates)):
            if active_dates[i] - active_dates[i - 1] == datetime.timedelta(days=1):
                curr_s += 1
                if curr_s > max_s:
                    max_s = curr_s
            else:
                curr_s = 1
        return max_s

    def update_charts(self):
        theme = self.get_theme()

        # ─── GRAFİK 1: Seçili Haftanın Günleri (Modern Bar Grafik) ───
        week_dates = [self.selected_monday + datetime.timedelta(days=i) for i in range(7)]
        daily_counts = []
        for d_obj in week_dates:
            daily_counts.append(sum(1 for t in self.tasks if self.get_task_state(d_obj, t)))

        self.ax1.clear()
        self.fig1.patch.set_facecolor(theme["chart_bg"])
        self.ax1.set_facecolor(theme["chart_bg"])

        max_val = max(len(self.tasks), 1)
        bars = self.ax1.bar(SHORT_DAYS, daily_counts, color=theme["chart_bar1"],
                            width=0.52, edgecolor=theme["chart_bg"], linewidth=0.5)

        for i, d_obj in enumerate(week_dates):
            cnt = daily_counts[i]
            if d_obj == self.today:
                bars[i].set_color(theme["done"])
                bars[i].set_edgecolor(theme.get("accent", "#FB7185"))
                bars[i].set_linewidth(1.5)
            if cnt > 0:
                self.ax1.text(i, cnt + (max_val * 0.04), str(cnt),
                              ha="center", va="bottom", fontsize=7.5, fontweight="bold",
                              color=theme["text"])

        self.ax1.set_ylim(0, max_val + max(1, int(max_val * 0.22)))
        self.ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=min(max_val + 1, 4)))
        self.ax1.tick_params(axis="both", colors=theme["chart_text"], labelsize=7.5)
        self.ax1.spines["top"].set_visible(False)
        self.ax1.spines["right"].set_visible(False)
        self.ax1.spines["left"].set_color(theme["chart_grid"])
        self.ax1.spines["bottom"].set_color(theme["chart_grid"])
        self.canvas1.draw_idle()

        # ─── GRAFİK 2: Seçili Ayın Donut Grafiği (Modern Halka) ───
        cy, cm = self.chart_year, self.chart_month
        nd = calendar.monthrange(cy, cm)[1]
        total_possible = len(self.tasks) * nd
        total_done = 0
        task_counts = {t: 0 for t in self.tasks}

        for d in range(1, nd + 1):
            d_obj = datetime.date(cy, cm, d)
            for t in self.tasks:
                if self.get_task_state(d_obj, t):
                    total_done += 1
                    task_counts[t] += 1

        total_remain = max(0, total_possible - total_done)
        pct = int(total_done / total_possible * 100) if total_possible > 0 else 0

        self.ax2.clear()
        self.fig2.patch.set_facecolor(theme["chart_bg"])
        self.ax2.set_facecolor(theme["chart_bg"])

        if total_done == 0 and total_remain == 0:
            sizes = [0, 1]
        else:
            sizes = [total_done, total_remain]

        wedge_colors = [theme["chart_pie_done"], theme["chart_pie_remain"]]
        self.ax2.pie(sizes, colors=wedge_colors,
                     startangle=90, counterclock=False,
                     wedgeprops=dict(width=0.36, edgecolor=theme["chart_bg"], linewidth=1.5))

        # Ortadaki Yüzde & Bilgi Metni
        self.ax2.text(0, 0.08, f"%{pct}", ha="center", va="center",
                      fontsize=12, fontweight="bold", color=theme["text"])
        self.ax2.text(0, -0.22, f"{total_done}/{total_possible}", ha="center", va="center",
                      fontsize=7, fontweight="bold", color=theme["text_secondary"])

        self.canvas2.draw_idle()

        # ─── 3. KART: Alışkanlık & Başarı İstatistikleri ───
        if hasattr(self, "stat_c1_val"):
            max_s = self.get_max_streak()
            self.stat_c1_val.configure(text=f"🔥 {max_s} Gün" if max_s > 0 else "0 Gün")
            self.stat_c2_val.configure(text=f"{total_done} Görev (%{pct})")

            # En çok yapılan görev
            if task_counts and total_done > 0:
                top_task, top_cnt = max(task_counts.items(), key=lambda x: x[1])
                t_display = top_task if len(top_task) <= 15 else (top_task[:14] + "..")
                self.stat_c3_val.configure(text=f"{t_display} ({top_cnt}x)" if top_cnt > 0 else "-")
            else:
                self.stat_c3_val.configure(text="-")

    def navigate_week(self, delta):
        play_button_sound()
        self.selected_monday += datetime.timedelta(days=7 * delta)
        self.update_chart1_title()
        self.update_charts()

    def update_chart1_title(self):
        if self.selected_monday == self.current_monday:
            title = "Bu Hafta"
        else:
            sun = self.selected_monday + datetime.timedelta(days=6)
            m1 = TURKISH_MONTHS[self.selected_monday.month][:3]
            m2 = TURKISH_MONTHS[sun.month][:3]
            if self.selected_monday.month == sun.month:
                title = f"{self.selected_monday.day}-{sun.day} {m1}"
            else:
                title = f"{self.selected_monday.day} {m1} - {sun.day} {m2}"
        self.chart1_title_lbl.configure(text=title)

    def navigate_month(self, delta):
        play_button_sound()
        m = self.chart_month + delta
        y = self.chart_year
        if m > 12:
            m = 1
            y += 1
        elif m < 1:
            m = 12
            y -= 1
        self.chart_month = m
        self.chart_year = y
        self.table_month = m
        self.table_year = y
        self.chart2_title_lbl.configure(text=f"Aylık Odak ({TURKISH_MONTHS[m]} {y})")
        if hasattr(self, "table_month_lbl"):
            self.table_month_lbl.configure(text=f"{TURKISH_MONTHS[m]} {y}")
        self.render_table()
        self.update_charts()

    def navigate_table_month(self, delta):
        play_button_sound()
        m = getattr(self, "table_month", self.today.month) + delta
        y = getattr(self, "table_year", self.today.year)
        if m > 12:
            m = 1
            y += 1
        elif m < 1:
            m = 12
            y -= 1
        self.table_month = m
        self.table_year = y
        self.chart_month = m
        self.chart_year = y
        self.chart2_title_lbl.configure(text=f"Aylık Odak ({TURKISH_MONTHS[m]} {y})")
        if hasattr(self, "table_month_lbl"):
            self.table_month_lbl.configure(text=f"{TURKISH_MONTHS[m]} {y}")
        self.render_table()
        self.update_charts()

    def reset_to_current_month(self):
        play_button_sound()
        self.table_month = self.today.month
        self.table_year = self.today.year
        self.chart_month = self.today.month
        self.chart_year = self.today.year
        self.chart2_title_lbl.configure(text=f"Aylık Odak ({TURKISH_MONTHS[self.today.month]} {self.today.year})")
        if hasattr(self, "table_month_lbl"):
            self.table_month_lbl.configure(text=f"{TURKISH_MONTHS[self.today.month]} {self.today.year}")
        self.render_table()
        self.update_charts()

    # ---------- SİSTEM TEPSİSİ, KAYAN WİDGET & ARKA PLAN MODU ----------
    def setup_tray_icon(self):
        """Pencere kapatıldığında arka planda %0 CPU ile çalışacak sistem tepsisi ikonu."""
        try:
            icon_img = create_tray_icon_image()
            menu = pystray.Menu(
                pystray.MenuItem("📂 Uygulamayı Aç", lambda icon, item: self.restore_from_tray(), default=True),
                pystray.MenuItem("📌 Kayan Mini Modu Aç/Kapat", lambda icon, item: self.after(0, self.toggle_sticky_mode)),
                pystray.MenuItem("⚡ Şimdi Darlama Bildirimi Gönder", lambda icon, item: self.after(0, lambda: self.trigger_ai_notification(is_test=True))),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("❌ Tamamen Kapat", lambda icon, item: self.after(0, self.quit_app))
            )
            self.tray_icon = pystray.Icon("HabitTracker", icon_img, "📋 Görev Takip (AI Darlama Aktif)", menu)
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
        except Exception as e:
            print(f"Sistem tepsisi başlatma hatası: {e}")

    def toggle_sticky_mode(self):
        """Kayan Mini Widget modunu açar veya kapatır."""
        play_button_sound()
        if not hasattr(self, "sticky_widget") or self.sticky_widget is None or not self.sticky_widget.winfo_exists():
            self.sticky_widget = StickyWidget(self)

        if self.sticky_widget.winfo_viewable():
            self.sticky_widget.hide_widget()
        else:
            self.sticky_widget.show_widget()

    def open_sticky_widget(self):
        play_button_sound()
        if not hasattr(self, "sticky_widget") or self.sticky_widget is None or not self.sticky_widget.winfo_exists():
            self.sticky_widget = StickyWidget(self)
        self.sticky_widget.show_widget()

    def hide_sticky_widget(self):
        play_button_sound()
        if hasattr(self, "sticky_widget") and self.sticky_widget and self.sticky_widget.winfo_exists():
            self.sticky_widget.hide_widget()

    def toggle_from_hotkey(self):
        """Global kısayola (Ctrl+Shift+T) basıldığında arka plandan tetiklenir."""
        self.after(0, self._on_hotkey_pressed)

    def _on_hotkey_pressed(self):
        if hasattr(self, "sticky_widget") and self.sticky_widget and self.sticky_widget.winfo_exists() and self.sticky_widget.winfo_viewable():
            self.sticky_widget.hide_widget()
        elif self.state() == "withdrawn" or self.state() == "iconic":
            self.restore_from_tray()
        else:
            self.open_sticky_widget()

    def hide_to_tray(self):
        """Pencereyi gizler, sistem tepsisinde arka planda hafifçe çalışmaya devam eder."""
        self.withdraw()

    def restore_from_tray(self):
        """Pencereyi sistem tepsisinden geri açar ve öne getirir."""
        self.after(0, self._do_restore)

    def apply_app_icon(self):
        """Uygulamanın başlık çubuğu ve görev çubuğu simgesini ToDo.ico yapar."""
        if os.path.exists(ICON_FILE):
            try:
                self.iconbitmap(ICON_FILE)
            except Exception:
                pass
            try:
                self.wm_iconbitmap(ICON_FILE)
            except Exception:
                pass

    def _do_restore(self):
        self.deiconify()
        self.state('normal')
        self.lift()
        self.focus_force()
        self.apply_app_icon()
        self.update_clock()
        self.attributes("-topmost", True)
        self.after(250, lambda: self.attributes("-topmost", False))

    def quit_app(self):
        """Uygulamayı ve tüm arka plan süreçlerini anında ve tamamen sonlandırır."""
        if hasattr(self, "hotkey_mgr") and self.hotkey_mgr:
            try:
                self.hotkey_mgr.stop()
            except Exception:
                pass
        if hasattr(self, "lock_socket") and self.lock_socket:
            try:
                self.lock_socket.close()
            except Exception:
                pass
        if self.tray_icon:
            try:
                self.tray_icon.stop()
            except Exception:
                pass
        try:
            self.destroy()
        except Exception:
            pass
        os._exit(0)

    # ---------- AI DARLAMA BİLDİRİM SİSTEMİ ----------
    def get_task_missed_days(self, task_name):
        """Görevin geriye dönük kaç gündür aksatıldığını hesaplar (yalnızca var olduğu geçmiş kayıtlar taranır)."""
        days = 0
        check_date = self.today - datetime.timedelta(days=1)
        for _ in range(30):
            ds = check_date.strftime("%Y-%m-%d")
            if ds not in self.records:
                # Veri tabanında bu gün için hiçbir kayıt yoksa geriye gitmeyi durdur
                break
            rec = self.records[ds]
            if task_name not in rec:
                # Bu görev o tarihte henüz eklenmemişse geçmişi saymayı durdur
                break
            if self.get_task_state(check_date, task_name):
                # Görev o gün yapılmış/tamamlanmış, aksatma serisi sonlandı
                break
            days += 1
            check_date -= datetime.timedelta(days=1)
        return days

    def _schedule_tasks_independently(self, force_reset=False):
        """Tüm hedef görevler için seçilen süre (örn: 45 dk) sonrasına yayılan bağımsız rastgele zamanlar belirler."""
        interval_str = self.settings.get("ai_interval", "45 Dk")
        base_minutes = {
            "15 Dk": 15, "30 Dk": 30, "45 Dk": 45,
            "1 Saat": 60, "2 Saat": 120
        }.get(interval_str, 45)

        target_tasks = self.settings.get("ai_target_tasks", self.tasks)
        if not target_tasks:
            target_tasks = self.tasks

        now_time = time.time()
        base_sec = base_minutes * 60

        shuffled = list(target_tasks)
        random.shuffle(shuffled)

        cumulative_gap = 0
        for task_name in shuffled:
            # Görev için henüz zaman atanmamışsa veya zorunlu sıfırlama istendiyse
            if force_reset or task_name not in self.task_scheduled_times or self.task_scheduled_times[task_name] < (now_time - 86400):
                gap = random.randint(1, 4) * 60 if cumulative_gap == 0 else random.randint(2, 6) * 60
                cumulative_gap += gap
                self.task_scheduled_times[task_name] = now_time + base_sec + cumulative_gap

    def trigger_single_ai_notification(self, task_name, is_test=False, force_snooze_count=None):
        """Tek bir görev için arka planda AI roast üretip popup açar."""
        if not is_test and task_name not in self.tasks:
            return
        dismissed = getattr(self, "today_dismissed_tasks", set())
        if not is_test and task_name in dismissed:
            return
        if not is_test and self.get_task_state(self.today, task_name):
            return

        days_missed = self.get_task_missed_days(task_name)
        pers = self.settings.get("ai_personality", "Sert & Direkt")
        model = self.settings.get("ai_model", "Dahili Baskıcı AI Motoru (Yerel/Hızlı)")
        c_prompt = self.settings.get("ai_custom_prompt", "")

        def _worker():
            roast_msg = generate_ai_roast(
                task_name=task_name,
                days_missed=days_missed,
                personality=pers,
                model_choice=model,
                custom_prompt=c_prompt
            )
            self.after(0, lambda: self._show_ai_popup(task_name, roast_msg, force_snooze_count=force_snooze_count))

        threading.Thread(target=_worker, daemon=True).start()

    def trigger_ai_notification(self, specific_task=None, is_test=False, force_snooze_count=None):
        """Test amaçlı veya tek bir görevi ekrana getirir."""
        if specific_task:
            self.trigger_single_ai_notification(specific_task, is_test=is_test, force_snooze_count=force_snooze_count)
            return

        target_tasks = self.settings.get("ai_target_tasks", self.tasks)
        if not target_tasks:
            target_tasks = self.tasks

        chosen = random.choice(list(target_tasks)) if target_tasks else "Örnek Görev"
        self.trigger_single_ai_notification(chosen, is_test=is_test, force_snooze_count=force_snooze_count)

    def _show_ai_popup(self, task_name, message, force_snooze_count=None):
        theme = self.get_theme()
        pers = self.settings.get("ai_personality", "Sert & Direkt")
        snooze_cnt = force_snooze_count if force_snooze_count is not None else getattr(self, "task_snooze_counts", {}).get(task_name, 0)

        # Eğer bu görev için açık bir popup varsa önce onu kapat
        if hasattr(self, "active_popups") and task_name in self.active_popups:
            try:
                self.active_popups[task_name].destroy()
            except Exception:
                pass

        popup = NotificationPopup(self, task_name, message, theme, is_ai=True, personality=pers, snooze_count=snooze_cnt)
        if hasattr(self, "active_popups"):
            self.active_popups[task_name] = popup

        self.settings["last_ai_notification_time"] = time.time()
        self.save_data()

    def check_ai_notifications(self):
        """Her görevin kendi bağımsız zamanı geldiğinde aralıklı ve rastgele bildirim atmasını denetler."""
        try:
            if self.settings.get("ai_notifications_enabled", True):
                now_time = time.time()
                self._schedule_tasks_independently(force_reset=False)

                target_tasks = self.settings.get("ai_target_tasks", self.tasks)
                dismissed = getattr(self, "today_dismissed_tasks", set())

                interval_str = self.settings.get("ai_interval", "45 Dk")
                base_min = {
                    "15 Dk": 15, "30 Dk": 30, "45 Dk": 45,
                    "1 Saat": 60, "2 Saat": 120
                }.get(interval_str, 45)

                for task_name in list(target_tasks):
                    sched_time = self.task_scheduled_times.get(task_name, 0)
                    if sched_time > 0 and now_time >= sched_time:
                        # Bu görevin sonraki hatırlatma zamanını planla (temel süre + rastgele +/- sapma)
                        jitter_sec = random.randint(-int(base_min * 0.15) * 60, int(base_min * 0.25) * 60)
                        self.task_scheduled_times[task_name] = now_time + (base_min * 60) + jitter_sec

                        # Eğer görev hala yapılmadıysa ve bugün kapatılmadıysa bildirimi tek başına aç
                        if not self.get_task_state(self.today, task_name) and task_name not in dismissed:
                            self.trigger_single_ai_notification(task_name)
        except Exception as e:
            print(f"AI bildirim kontrol hatası: {e}")

        self.after(20000, self.check_ai_notifications)


# ============================================================
#  TEKİL ÇALIŞMA (SINGLE INSTANCE IPC)
# ============================================================
SINGLE_INSTANCE_PORT = 52849


def ensure_single_instance(app_instance):
    """Uygulamanın birden fazla açılmasını engeller; kısayoldan tekrar açıldığında arka plandakini öne getirir."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", SINGLE_INSTANCE_PORT))
        s.listen(5)

        def _listen():
            while True:
                try:
                    conn, _ = s.accept()
                    data = conn.recv(1024)
                    if b"RESTORE" in data:
                        app_instance.after(0, app_instance._do_restore)
                    conn.close()
                except Exception:
                    break

        threading.Thread(target=_listen, daemon=True).start()
        return s
    except OSError:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("127.0.0.1", SINGLE_INSTANCE_PORT))
            client.sendall(b"RESTORE")
            client.close()
        except Exception:
            pass
        sys.exit(0)


# ============================================================
#  BAŞLAT
# ============================================================
if __name__ == "__main__":
    # 1. Hızlı Soket Kontrolü (Uygulama zaten açıksa 1 ms'de öne getirip GUI yüklemeden anında sonlan)
    try:
        quick_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        quick_sock.connect(("127.0.0.1", SINGLE_INSTANCE_PORT))
        quick_sock.sendall(b"RESTORE")
        quick_sock.close()
        sys.exit(0)
    except OSError:
        pass

    app = HabitTrackerApp()
    app.lock_socket = ensure_single_instance(app)
    app.mainloop()