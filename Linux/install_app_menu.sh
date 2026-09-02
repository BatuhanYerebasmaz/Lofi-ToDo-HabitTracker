#!/usr/bin/env bash
# ============================================================
#  Lofi ToDo & Habit Tracker — Uygulama Menüsüne Ekle
#  Herhangi bir Linux masaüstü ortamında (GNOME, KDE, XFCE,
#  Hyprland+wofi/rofi, vb.) çalışır: freedesktop.org .desktop
#  standardını kullanır, dağıtıma özel bir şey yapmaz.
#
#  Kullanim:  ./install_app_menu.sh
#  Kaldirmak icin: rm ~/.local/share/applications/lofi-todo-habit-tracker.desktop
# ============================================================
set -e
cd "$(dirname "$0")"
LINUX_DIR="$(pwd)"
PROJECT_ROOT="$(cd .. && pwd)"

APPS_DIR="$HOME/.local/share/applications"
ICONS_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
mkdir -p "$APPS_DIR" "$ICONS_DIR"

ICON_SRC="$PROJECT_ROOT/images/ToDo.ico"
ICON_DST="$ICONS_DIR/lofi-todo-habit-tracker.png"
ICON_FOR_DESKTOP="$ICON_SRC"

# --- .ico -> .png dönüşümü ----------------------------------
# Çoğu masaüstü ortamı .ico simgesini menüde düzgün göstermez;
# elimizde Pillow varsa (proje bağımlılığı) PNG'ye çeviriyoruz.
# Yoksa sessizce orijinal .ico yoluna geri düşüyoruz.
PYBIN=""
if [ -x "$LINUX_DIR/.venv/bin/python" ]; then
    PYBIN="$LINUX_DIR/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    PYBIN="$(command -v python3)"
fi

if [ -n "$PYBIN" ] && [ -f "$ICON_SRC" ]; then
    if "$PYBIN" - "$ICON_SRC" "$ICON_DST" <<'EOF' 2>/dev/null
import sys
try:
    from PIL import Image
except ImportError:
    sys.exit(1)
src, dst = sys.argv[1], sys.argv[2]
Image.open(src).save(dst, format="PNG")
EOF
    then
        ICON_FOR_DESKTOP="$ICON_DST"
    fi
fi

# --- .desktop dosyasi ----------------------------------------
DESKTOP_FILE="$APPS_DIR/lofi-todo-habit-tracker.desktop"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=Lofi ToDo & Habit Tracker
Comment=Lofi tarzi gorev ve aliskanlik takip uygulamasi
Exec=$LINUX_DIR/baslat.sh
Icon=$ICON_FOR_DESKTOP
Terminal=false
Categories=Office;
EOF
chmod +x "$DESKTOP_FILE"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APPS_DIR" >/dev/null 2>&1 || true
fi

echo "Uygulama menuye eklendi: $DESKTOP_FILE"
echo "Menude gorunmezse oturumu kapatip tekrar acmayi deneyin (bazi DE'ler .desktop dosyalarini oturum baslangicinda tarar)."
