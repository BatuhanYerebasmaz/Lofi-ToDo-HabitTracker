#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linux Başlatıcı (Launcher)
==========================

Bu dosya, ana proje kaynak kodunu (ToDoList.py) TEK BİR SATIRINI BİLE
DEĞİŞTİRMEDEN Linux üzerinde çalıştırmak için tasarlanmıştır. Aynı yöntem
macOS launcher'ında (MacOS/mac_launcher.py) kullanılan yöntemdir: ToDoList.py
import edilmeden ÖNCE sys.modules içine sahte (stub) bir `winsound` modülü
enjekte edilir, ardından orijinal dosya byte-byte olduğu gibi yüklenir.

Windows'a özel diğer çağrılar (ctypes.windll ile köşe yuvarlatma, global
Ctrl+Shift+T kısayolu, taskbar API'leri) zaten orijinal kodda try/except ile
korunmuş durumda; Linux'ta `ctypes.windll` erişimi AttributeError fırlatır ve
sessizce yutulur, uygulama çökmez. `pystray` Linux'ta gerçek bir arka uca
sahiptir (AppIndicator/GTK ya da Xorg), bu yüzden macOS'takinin aksine sistem
tepsisi burada devre dışı BIRAKILMAZ.

Uygulanan runtime yamaları (hepsi yalnızca bellekte; ToDoList.py dosyasına
dokunulmaz):
  * SES      -> Windows winmm (MCI) yerine paplay/aplay/ffplay (bulunan ilki)
  * GÖRSEL   -> os.startfile yerine xdg-open
"""

import os
import sys
import types
import shutil
import subprocess
import importlib.util

_HERE = os.path.dirname(os.path.abspath(__file__))
_CANDIDATES = [
    os.path.join(_HERE, "ToDoList.py"),
    os.path.join(os.path.dirname(_HERE), "ToDoList.py"),
]
TODO_MAIN = next((p for p in _CANDIDATES if os.path.exists(p)), None)
if TODO_MAIN is None:
    sys.stderr.write("HATA: ToDoList.py bulunamadi.\n")
    sys.exit(1)

PROJECT_ROOT = os.path.dirname(TODO_MAIN)
SOUNDS_DIR = os.path.join(PROJECT_ROOT, "sounds")


# ------------------------------------------------------------------
# 1) Ses çalma: paplay (PulseAudio/PipeWire) -> aplay (ALSA) -> ffplay.
#    İlk bulunan komut sabitlenir, her çağrıda yeniden aranmaz.
# ------------------------------------------------------------------
def _find_player():
    for cmd, args in (
        ("paplay", []),
        ("aplay", ["-q"]),
        ("ffplay", ["-nodisp", "-autoexit", "-loglevel", "quiet"]),
    ):
        path = shutil.which(cmd)
        if path:
            return [path] + args
    return None


_PLAYER = _find_player()


def _play_sound(path):
    """Sesi bloklamadan çal; hata olursa ya da oynatıcı yoksa sessizce yut."""
    if not _PLAYER or not path or not os.path.exists(path):
        return
    try:
        subprocess.Popen(
            _PLAYER + [path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


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
        # Sistemin varsayılan uyarı sesi Linux dağıtımları arasında tutarlı
        # bir yol üzerinden gelmez; sessizce görmezden gel (kritik değil).
        pass

    def PlaySound(sound, flags=0):
        if sound and isinstance(sound, str):
            _play_sound(sound)

    def Beep(freq=1000, dur=200):
        pass

    stub.MessageBeep = MessageBeep
    stub.PlaySound = PlaySound
    stub.Beep = Beep
    sys.modules["winsound"] = stub


# ------------------------------------------------------------------
# 3) Linux ses yaması: orijinaldeki SoundEngine sınıfı Windows winmm
#    (ctypes.windll) kullanır ve Linux'ta tamamen sessiz kalır.
#    Sınıf metotlarını çalışma zamanında paplay/aplay/ffplay ile
#    değiştiriyoruz.
# ------------------------------------------------------------------
def _patch_sound_engine(mod):
    SoundEngine = getattr(mod, "SoundEngine", None)
    if SoundEngine is None:
        return

    def _play(cls, file_name):
        if not file_name:
            return
        _play_sound(os.path.join(SOUNDS_DIR, file_name))

    def _noop(cls, *a, **k):
        return

    SoundEngine.play = classmethod(_play)
    SoundEngine.init_engine = classmethod(_noop)
    SoundEngine.close_all = classmethod(_noop)


# ------------------------------------------------------------------
# 4) CTkToplevel.grab_set yaması: SettingsWindow (ToDoList.py:3410),
#    pencere daha görünür/eşlenmiş olmadan grab_set() çağırıyor. Windows
#    bu sıralamayı tolere eder; X11'de bu ya "grab failed: window not
#    viewable" hatasına ya da içeriği hiç çizilmemiş beyaz/boş bir
#    pencereye yol açar (pencere yöneticisi henüz haritalamadan input
#    kilitleniyor). Pencere gerçekten görünür olana kadar bekleyip
#    ardından asıl grab_set'i çağırıyoruz — tüm CTkToplevel örneklerini
#    kapsar, yalnızca ToDoList.py'nin davranışını çalışma zamanında
#    düzeltir.
# ------------------------------------------------------------------
def _patch_toplevel_grab():
    try:
        import customtkinter as ctk
    except ImportError:
        return
    orig_grab_set = ctk.CTkToplevel.grab_set

    def safe_grab_set(self, *a, **k):
        try:
            self.wait_visibility()
        except Exception:
            pass
        try:
            return orig_grab_set(self, *a, **k)
        except Exception:
            pass

    ctk.CTkToplevel.grab_set = safe_grab_set


# ------------------------------------------------------------------
# 5) os.startfile yaması: Linux'ta bu fonksiyon yoktur; orijinal kod
#    hata alınca görseli tarayıcıda açmaya çalışır. Bunun yerine
#    masaüstü ortamının kendi 'xdg-open' komutuna yönlendiriyoruz.
# ------------------------------------------------------------------
def _patch_startfile():
    if hasattr(os, "startfile"):
        return

    def startfile(path, *a, **k):
        opener = shutil.which("xdg-open")
        if opener:
            subprocess.Popen([opener, path],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.startfile = startfile


def _exec_tolerant(spec, module):
    """ToDoList.py modül gövdesinde koşulsuz os.makedirs(DATA_DIR) çağrısı
    var; salt okunur bir dizinde çalıştırılırsa hata verirdi. Yalnızca
    yükleme süresince makedirs'i toleranslı yapıyoruz."""
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


def main():
    _install_winsound_stub()
    _patch_startfile()

    os.chdir(PROJECT_ROOT)
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

    spec = importlib.util.spec_from_file_location("todolist_app", TODO_MAIN)
    module = importlib.util.module_from_spec(spec)
    sys.modules["todolist_app"] = module
    _exec_tolerant(spec, module)

    _patch_sound_engine(module)
    _patch_toplevel_grab()

    lock_sock = module.acquire_single_instance_lock()
    app = module.HabitTrackerApp()
    app.lock_socket = lock_sock
    module.start_single_instance_listener(lock_sock, app)
    app.mainloop()


if __name__ == "__main__":
    main()
