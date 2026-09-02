#!/bin/bash
# ============================================================
#  Lofi ToDo & Habit Tracker — macOS Başlatıcı
#  Finder'da ÇİFT TIKLAYIN. İlk açılışta sanal ortam kurulur
#  ve gerekli kütüphaneler indirilir (1-2 dakika), sonraki
#  açılışlar anındadır.
# ============================================================
set -e
cd "$(dirname "$0")"

# Python.org derlemesi universal2 oldugu icin, Rosetta altindaki bir
# terminalden calistirilirsa paketler (numpy/matplotlib) yuklenemez.
# Her seyi donanimin kendi mimarisinde calistiriyoruz.
if [ "$(sysctl -n hw.optional.arm64 2>/dev/null)" = "1" ]; then
    NATIVE=(/usr/bin/arch -arch arm64)
else
    NATIVE=(/usr/bin/arch -arch x86_64)
fi

PROJECT_ROOT="$(cd .. && pwd)"
VENV="$(pwd)/.venv"
PYBIN="$VENV/bin/python"

# --- 1) Tkinter'i olan bir Python 3 bul --------------------
find_python() {
    for c in /Library/Frameworks/Python.framework/Versions/3.14/bin/python3 \
             /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
             /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 \
             /usr/local/bin/python3 /opt/homebrew/bin/python3 /usr/bin/python3; do
        if [ -x "$c" ] && "${NATIVE[@]}" "$c" -c "import tkinter" >/dev/null 2>&1; then
            echo "$c"; return 0
        fi
    done
    return 1
}

# --- 2) Sanal ortam yoksa kur ------------------------------
if [ ! -x "$PYBIN" ]; then
    BASE_PY="$(find_python)" || {
        echo ""
        echo "HATA: Tkinter destekli bir Python 3 bulunamadi."
        echo "Lutfen python.org adresinden Python 3 kurun:"
        echo "   https://www.python.org/downloads/macos/"
        echo ""
        read -n 1 -s -r -p "Kapatmak icin bir tusa basin..."
        exit 1
    }
    echo "Ilk kurulum yapiliyor (Python: $BASE_PY)..."
    "${NATIVE[@]}" "$BASE_PY" -m venv "$VENV"
    "${NATIVE[@]}" "$PYBIN" -m pip install --upgrade pip >/dev/null
    "${NATIVE[@]}" "$PYBIN" -m pip install -r "$PROJECT_ROOT/requirements.txt"
    echo "Kurulum tamamlandi."
fi

# --- 3) Uygulamayi baslat ----------------------------------
echo "Uygulama baslatiliyor..."
exec "${NATIVE[@]}" "$PYBIN" "$(pwd)/mac_launcher.py"
