#!/bin/bash
# ============================================================
#  Lofi-ToDo-HabitTracker — macOS release derleyicisi
#  Ciktilar:
#    dist/Lofi-ToDo-HabitTracker.app   (cift tikla calisan uygulama)
#    dist/Lofi-ToDo-HabitTracker.dmg   (dagitim imaji)
#  Kullanim: bu dosyaya cift tiklayin ya da  bash MacOS/build_release.command
# ============================================================
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$(pwd)"

APP_NAME="Lofi-ToDo-HabitTracker"
BUNDLE_ID="com.yasinkaratoprak.lofi-todo-habittracker"
VERSION="1.0"

DIST="$ROOT/dist"
APP="$DIST/$APP_NAME.app"
DMG="$DIST/$APP_NAME.dmg"
RES="$APP/Contents/Resources"
PAYLOAD="$RES/app"

echo "==> Temizlik"
rm -rf "$APP" "$DMG"
mkdir -p "$APP/Contents/MacOS" "$PAYLOAD"

# --- Ikon ---------------------------------------------------
if [ ! -f "$ROOT/MacOS/AppIcon.icns" ]; then
    echo "==> Ikon uretiliyor"
    PY="$ROOT/MacOS/.venv/bin/python"
    [ -x "$PY" ] || PY="$(command -v python3)"
    "$PY" "$ROOT/MacOS/make_app_icon.py"
fi
cp "$ROOT/MacOS/AppIcon.icns" "$RES/AppIcon.icns"

# --- Uygulama yuku (salt okunur kaynaklar) ------------------
echo "==> Kaynaklar kopyalaniyor"
cp "$ROOT/ToDoList.py" "$ROOT/requirements.txt" "$PAYLOAD/"
cp "$ROOT/MacOS/mac_launcher.py" "$PAYLOAD/"
cp -R "$ROOT/sounds" "$ROOT/images" "$ROOT/assets" "$PAYLOAD/"
find "$PAYLOAD" -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
find "$PAYLOAD" -name '.DS_Store' -delete 2>/dev/null || true

# --- Info.plist ---------------------------------------------
echo "==> Info.plist yaziliyor"
cat > "$APP/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>              <string>$APP_NAME</string>
    <key>CFBundleDisplayName</key>       <string>$APP_NAME</string>
    <key>CFBundleIdentifier</key>        <string>$BUNDLE_ID</string>
    <key>CFBundleExecutable</key>        <string>$APP_NAME</string>
    <key>CFBundleIconFile</key>          <string>AppIcon</string>
    <key>CFBundlePackageType</key>       <string>APPL</string>
    <key>CFBundleShortVersionString</key><string>$VERSION</string>
    <key>CFBundleVersion</key>           <string>$VERSION</string>
    <key>CFBundleInfoDictionaryVersion</key><string>6.0</string>
    <key>LSMinimumSystemVersion</key>    <string>11.0</string>
    <key>LSApplicationCategoryType</key> <string>public.app-category.productivity</string>
    <key>NSHighResolutionCapable</key>   <true/>
    <key>LSArchitecturePriority</key>
    <array>
        <string>arm64</string>
        <string>x86_64</string>
    </array>
    <key>NSHumanReadableCopyright</key>  <string>Lofi ToDo &amp; Habit Tracker</string>
</dict>
</plist>
PLIST

# --- Baslatici betigi ---------------------------------------
echo "==> Baslatici yaziliyor"
cat > "$APP/Contents/MacOS/$APP_NAME" <<'LAUNCHER'
#!/bin/bash
# Lofi-ToDo-HabitTracker — .app baslatici
# Paketin ici SALT OKUNUR kabul edilir: sanal ortam ve kullanici verisi
# ~/Library/Application Support/Lofi-ToDo-HabitTracker altinda tutulur.

SUPPORT="$HOME/Library/Application Support/Lofi-ToDo-HabitTracker"
VENV="$SUPPORT/venv"
PYBIN="$VENV/bin/python"
LOG="$SUPPORT/launch.log"
mkdir -p "$SUPPORT"

dialog() {
    /usr/bin/osascript -e "display dialog \"$1\" buttons {\"Tamam\"} default button 1 with title \"Lofi-ToDo-HabitTracker\" with icon caution" >/dev/null 2>&1
}

# Universal2 Python + tek mimarili paketler: Rosetta ile baslatilirsa
# numpy/matplotlib yuklenmez. Donanimin kendi mimarisini zorluyoruz.
if [ "$(sysctl -n hw.optional.arm64 2>/dev/null)" = "1" ]; then
    NATIVE=(/usr/bin/arch -arch arm64)
else
    NATIVE=(/usr/bin/arch -arch x86_64)
fi

RES="$(cd "$(dirname "$0")/../Resources/app" && pwd)"
LAUNCHER_PY="$RES/mac_launcher.py"

if [ ! -f "$LAUNCHER_PY" ]; then
    dialog "Uygulama paketi bozuk gorunuyor (mac_launcher.py yok)."
    exit 1
fi

# --- Ilk acilis: sanal ortam ---------------------------------
if [ ! -x "$PYBIN" ]; then
    BASE_PY=""
    for c in /Library/Frameworks/Python.framework/Versions/3.14/bin/python3 \
             /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
             /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 \
             /usr/local/bin/python3 /opt/homebrew/bin/python3 /usr/bin/python3; do
        if [ -x "$c" ] && "${NATIVE[@]}" "$c" -c "import tkinter" >/dev/null 2>&1; then BASE_PY="$c"; break; fi
    done
    if [ -z "$BASE_PY" ]; then
        dialog "Tkinter destekli Python 3 bulunamadi.\n\npython.org uzerinden Python 3 kurup tekrar deneyin:\nhttps://www.python.org/downloads/macos/"
        exit 1
    fi
    /usr/bin/osascript -e 'display notification "Gerekli kutuphaneler indiriliyor, birkac dakika surebilir..." with title "Lofi-ToDo-HabitTracker" subtitle "Ilk kurulum"' >/dev/null 2>&1
    if ! { "${NATIVE[@]}" "$BASE_PY" -m venv "$VENV" &&
           "${NATIVE[@]}" "$PYBIN" -m pip install --upgrade pip &&
           "${NATIVE[@]}" "$PYBIN" -m pip install -r "$RES/requirements.txt"; } >"$LOG" 2>&1; then
        rm -rf "$VENV"
        dialog "Kurulum basarisiz oldu. Ayrintilar: $LOG"
        exit 1
    fi
    /usr/bin/osascript -e 'display notification "Kurulum tamamlandi, uygulama aciliyor." with title "Lofi-ToDo-HabitTracker"' >/dev/null 2>&1
fi

# --- Calistir -------------------------------------------------
# LOFI_DATA_DIR: mac_launcher.py veriyi paket yerine buraya yazar.
export LOFI_DATA_DIR="$SUPPORT/data"
export LOFI_APP_NAME="Lofi-ToDo-HabitTracker"
export LOFI_APP_ICON="$(cd "$(dirname "$0")/../Resources" && pwd)/AppIcon.icns"
mkdir -p "$LOFI_DATA_DIR"
cd "$RES"
exec "${NATIVE[@]}" "$PYBIN" "$LAUNCHER_PY" >>"$LOG" 2>&1
LAUNCHER
chmod +x "$APP/Contents/MacOS/$APP_NAME"

plutil -lint "$APP/Contents/Info.plist" >/dev/null
touch "$APP"

# --- DMG -----------------------------------------------------
echo "==> DMG olusturuluyor"
STAGE="$(mktemp -d)"
cp -R "$APP" "$STAGE/"
ln -s /Applications "$STAGE/Applications"
cat > "$STAGE/OKU-BENI.txt" <<TXT
Lofi-ToDo-HabitTracker — macOS Kurulumu
=======================================

1) Soldaki uygulamayi sag taraftaki "Applications" klasorune surukleyin.
2) Ilk acilista macOS "gelistirici dogrulanamadi" diyebilir:
   uygulamaya SAG TIKLAYIP "Ac" (Open) secin, ardindan "Ac" deyin.
   (Alternatif: Sistem Ayarlari > Gizlilik ve Guvenlik > "Yine de Ac")
3) Ilk acilis bilgisayarinizda kurulu Python 3 ile kendi sanal ortamini
   kurar (birkac dakika). Tkinter destekli Python 3 gerekir:
   https://www.python.org/downloads/macos/

Verileriniz nerede?
  ~/Library/Application Support/Lofi-ToDo-HabitTracker/data
  (Gorevler, gunluk ve fotograflar burada; uygulamayi silmek veriyi silmez.)
TXT

hdiutil create -volname "$APP_NAME" -srcfolder "$STAGE" -ov -format UDZO -quiet "$DMG"
rm -rf "$STAGE"

echo ""
echo "TAMAM:"
echo "  $APP"
echo "  $DMG  ($(du -h "$DMG" | cut -f1))"
