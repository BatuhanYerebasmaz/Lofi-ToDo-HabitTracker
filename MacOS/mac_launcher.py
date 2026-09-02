#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macOS Başlatıcı (Launcher)
==========================

Bu dosya, ana proje kaynak kodunu (ToDoList.py) TEK BİR SATIRINI BİLE
DEĞİŞTİRMEDEN macOS üzerinde çalıştırmak için tasarlanmıştır.

ToDoList.py Windows'a özgü yazıldığı için doğrudan macOS'ta çalışmaz:
en tepede korumasız bir `import winsound` vardır ve `winsound` yalnızca
Windows'ta bulunur. Bu launcher, ToDoList.py import edilmeden ÖNCE
sys.modules içine sahte (stub) bir `winsound` modülü enjekte eder,
ardından orijinal dosyayı byte-byte olduğu gibi yükler.

Windows'a özel diğer çağrılar (ctypes.windll ile köşe yuvarlatma, global
Ctrl+Shift+T kısayolu, taskbar API'leri, .ico ikon) zaten orijinal kodda
try/except ile korunmuş durumda; macOS'ta sessizce devre dışı kalırlar,
uygulama çökmez.

Ek olarak macOS'a özgü üç runtime yaması uygulanır (hepsi yalnızca
bellekte; ToDoList.py dosyasına dokunulmaz):
  * SES      -> Windows winmm (MCI) yerine `afplay`
  * GÖRSEL   -> os.startfile yerine `open`
  * TEPSİ    -> pystray macOS'ta ana iş parçacığı dışında çalışamaz,
                bu yüzden tepsi kapatılır ve pencere kapatma "Dock'a
                küçült" davranışına çevrilir.
  * VERİ     -> LOFI_DATA_DIR ortam değişkeni verilmişse (.app paketi
                bunu ayarlar) günlük/görev verisi paket içine değil
                ~/Library/Application Support altına yazılır.
"""

import os
import sys
import types
import subprocess
import importlib.util

# ------------------------------------------------------------------
# 1) Ana proje kökünü bul (bu launcher MacOS/ alt klasöründe durur;
#    kaynaklar bir üst dizindedir: ToDoList.py, images/, sounds/, data/)
#    .app paketi içinde ise ToDoList.py bu launcher ile aynı klasörde
#    (Resources) bulunur; her iki durumu da destekle.
# ------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_CANDIDATES = [
    os.path.join(_HERE, "ToDoList.py"),                   # .app Resources düzeni
    os.path.join(os.path.dirname(_HERE), "ToDoList.py"),  # repo düzeni (MacOS/..)
]
TODO_MAIN = next((p for p in _CANDIDATES if os.path.exists(p)), None)
if TODO_MAIN is None:
    sys.stderr.write("HATA: ToDoList.py bulunamadi.\n")
    sys.exit(1)

PROJECT_ROOT = os.path.dirname(TODO_MAIN)
SOUNDS_DIR = os.path.join(PROJECT_ROOT, "sounds")


# ------------------------------------------------------------------
# 2) Sahte 'winsound' modülü — yalnızca ToDoList.py'nin kullandığı
#    isimleri sağlar (MessageBeep ve MB_* sabitleri).
# ------------------------------------------------------------------
def _install_winsound_stub():
    if "winsound" in sys.modules:
        return
    stub = types.ModuleType("winsound")
    stub.MB_ICONHAND = 0x00000010
    stub.MB_ICONQUESTION = 0x00000020
    stub.MB_ICONEXCLAMATION = 0x00000030
    stub.MB_ICONASTERISK = 0x00000040
    stub.MB_OK = 0x00000000
    stub.SND_FILENAME = 0x00020000
    stub.SND_ASYNC = 0x0001

    def MessageBeep(_type=0):
        _afplay("/System/Library/Sounds/Funk.aiff")

    def PlaySound(sound, flags=0):
        if sound and isinstance(sound, str):
            _afplay(sound)

    def Beep(freq=1000, dur=200):
        MessageBeep()

    stub.MessageBeep = MessageBeep
    stub.PlaySound = PlaySound
    stub.Beep = Beep
    sys.modules["winsound"] = stub


def _afplay(path):
    """Sesi bloklamadan çal; hata olursa sessizce yut."""
    try:
        if path and os.path.exists(path):
            subprocess.Popen(
                ["afplay", path],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
    except Exception:
        pass


# ------------------------------------------------------------------
# 3) macOS ses yaması: orijinaldeki SoundEngine sınıfı Windows winmm
#    (ctypes.windll) kullanır ve macOS'ta tamamen sessiz kalır.
#    Sınıf metotlarını çalışma zamanında afplay ile değiştiriyoruz.
# ------------------------------------------------------------------
def _patch_sound_engine(mod):
    SoundEngine = getattr(mod, "SoundEngine", None)
    if SoundEngine is None:
        return

    def _play(cls, file_name):
        if not file_name:
            return
        _afplay(os.path.join(SOUNDS_DIR, file_name))

    def _noop(cls, *a, **k):
        return

    SoundEngine.play = classmethod(_play)
    SoundEngine.init_engine = classmethod(_noop)
    SoundEngine.close_all = classmethod(_noop)


# ------------------------------------------------------------------
# 4) os.startfile yaması: macOS'ta bu fonksiyon yoktur; orijinal kod
#    hata alınca görseli tarayıcıda açmaya çalışır. Bunun yerine
#    macOS'un kendi 'open' komutuna yönlendiriyoruz (Önizleme açılır).
# ------------------------------------------------------------------
def _patch_startfile():
    if hasattr(os, "startfile"):
        return

    def startfile(path, *a, **k):
        subprocess.Popen(["open", path],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.startfile = startfile


# ------------------------------------------------------------------
# 5) Sistem tepsisi yaması: pystray'in macOS arka ucu yalnızca ana
#    iş parçacığında çalışabilir, ToDoList.py ise onu daemon thread'de
#    başlatıyor. Bu macOS'ta tepsiyi çalıştırmaz (ve çökebilir), o
#    yüzden tepsiyi devre dışı bırakıp pencere kapatmayı Dock'a
#    küçültmeye çeviriyoruz — böylece uygulama kaybolmuyor.
# ------------------------------------------------------------------
def _patch_tray(mod):
    App = getattr(mod, "HabitTrackerApp", None)
    if App is None:
        return

    def setup_tray_icon(self):
        self.tray_icon = None

    def hide_to_tray(self):
        try:
            self.iconify()
        except Exception:
            self.withdraw()

    App.setup_tray_icon = setup_tray_icon
    App.hide_to_tray = hide_to_tray


# ------------------------------------------------------------------
# 6) Veri dizini yaması: .app paketinden çalışırken paketin içi salt
#    okunur kabul edilir; görev/günlük verisi ve fotoğraflar kullanıcı
#    ev dizinine yazılır. Yol, paketin başlatıcısı tarafından
#    LOFI_DATA_DIR ortam değişkeni ile bildirilir. Değişken yoksa
#    (depodan çalıştırma) orijinal davranış korunur: proje/data.
# ------------------------------------------------------------------
def _patch_data_dirs(mod):
    data_dir = os.environ.get("LOFI_DATA_DIR")
    if not data_dir:
        return
    media_dir = os.path.join(data_dir, "notes_media")
    os.makedirs(media_dir, exist_ok=True)
    mod.DATA_DIR = data_dir
    mod.DATA_FILE = os.path.join(data_dir, "data.json")
    mod.NOTES_MEDIA_DIR = media_dir


def _exec_tolerant(spec, module):
    """ToDoList.py modül gövdesinde koşulsuz os.makedirs(DATA_DIR) çağrısı
    var; salt okunur bir .app paketinde bu hata verirdi. Yalnızca yükleme
    süresince makedirs'i toleranslı yapıyoruz, hemen sonra geri alıyoruz."""
    real_makedirs = os.makedirs

    def tolerant(path, *a, **k):
        try:
            return real_makedirs(path, *a, **k)
        except OSError:
            return None

    os.makedirs = tolerant
    try:
        spec.loader.exec_module(module)
    finally:
        os.makedirs = real_makedirs


# ------------------------------------------------------------------
# 7) Uygulama kimliği: python.org derlemesi Tk pencerelerini kendi
#    "Python.app" paketiyle açar; bu yüzden menü çubuğunda ve Dock'ta
#    "Python" yazar ve jenerik roket ikonu görünür. NSBundle bilgi
#    sözlüğünü ve Dock ikonunu çalışma zamanında düzeltiyoruz.
#    (pyobjc, pystray bağımlılığı olarak zaten kurulu.)
# ------------------------------------------------------------------
APP_NAME = os.environ.get("LOFI_APP_NAME", "Lofi-ToDo-HabitTracker")
APP_ICON = os.environ.get("LOFI_APP_ICON") or os.path.join(_HERE, "AppIcon.icns")


def _patch_bundle_name():
    """Menü çubuğundaki uygulama adını düzeltir. Tk başlamadan ÖNCE çağrılmalı."""
    try:
        from Foundation import NSBundle
        bundle = NSBundle.mainBundle()
        info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
        if info is not None:
            info["CFBundleName"] = APP_NAME
            info["CFBundleDisplayName"] = APP_NAME
    except Exception:
        pass


def _set_dock_icon():
    """Dock ikonunu uygulamanın kendi ikonuyla değiştirir (Tk açıldıktan sonra)."""
    try:
        if not os.path.exists(APP_ICON):
            return
        from AppKit import NSApplication, NSImage
        img = NSImage.alloc().initWithContentsOfFile_(APP_ICON)
        if img is not None:
            NSApplication.sharedApplication().setApplicationIconImage_(img)
    except Exception:
        pass


def main():
    _install_winsound_stub()
    _patch_startfile()

    # ToDoList.py tüm yollarını __file__'e göre kurar, yine de çalışma
    # dizinini proje köküne sabitlemek güvenli.
    os.chdir(PROJECT_ROOT)
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

    # Orijinal dosyayı 'todolist_app' adıyla yüklüyoruz. Böylece
    # `if __name__ == "__main__"` bloğu ÇALIŞMAZ; sınıflar tanımlanır,
    # biz macOS yamalarını uygularız ve uygulamayı elle başlatırız.
    spec = importlib.util.spec_from_file_location("todolist_app", TODO_MAIN)
    module = importlib.util.module_from_spec(spec)
    sys.modules["todolist_app"] = module
    _exec_tolerant(spec, module)

    _patch_data_dirs(module)
    _patch_sound_engine(module)
    _patch_tray(module)

    # Menü çubuğu adı Tk pencereden ÖNCE ayarlanmalı.
    _patch_bundle_name()

    # Orijinal __main__ bloğuyla birebir aynı başlatma sırası.
    lock_sock = module.acquire_single_instance_lock()
    app = module.HabitTrackerApp()
    app.lock_socket = lock_sock
    module.start_single_instance_listener(lock_sock, app)
    app.after(150, _set_dock_icon)
    app.mainloop()


if __name__ == "__main__":
    main()
