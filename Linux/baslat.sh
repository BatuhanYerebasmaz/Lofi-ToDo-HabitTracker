#!/usr/bin/env bash
# ============================================================
#  Lofi ToDo & Habit Tracker — Linux Başlatıcı
#  Terminalden çalıştırın: ./baslat.sh
#  İlk açılışta sanal ortam kurulur ve gerekli kütüphaneler
#  indirilir (1-2 dakika), sonraki açılışlar anındadır.
# ============================================================
set -e
cd "$(dirname "$0")"

PROJECT_ROOT="$(cd .. && pwd)"
VENV="$(pwd)/.venv"
PYBIN="$VENV/bin/python"

find_python() {
    for c in python3.13 python3.12 python3.11 python3; do
        if command -v "$c" >/dev/null 2>&1 && "$c" -c "import tkinter" >/dev/null 2>&1; then
            command -v "$c"; return 0
        fi
    done
    return 1
}

if [ ! -x "$PYBIN" ]; then
    BASE_PY="$(find_python)" || {
        echo ""
        echo "HATA: Tkinter destekli bir Python 3 bulunamadi."
        echo "Debian/Ubuntu:  sudo apt install python3 python3-venv python3-tk"
        echo "Fedora:         sudo dnf install python3 python3-tkinter"
        echo "Arch:           sudo pacman -S python tk"
        echo ""
        exit 1
    }
    echo "Ilk kurulum yapiliyor (Python: $BASE_PY)..."
    "$BASE_PY" -m venv "$VENV"
    "$PYBIN" -m pip install --upgrade pip >/dev/null
    "$PYBIN" -m pip install -r "$PROJECT_ROOT/requirements.txt"
    echo "Kurulum tamamlandi."
fi

echo "Uygulama baslatiliyor..."
exec "$PYBIN" "$(pwd)/linux_launcher.py"
