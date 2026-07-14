@echo off
REM ============================================
REM SpaceWarx - Windows .exe olusturma scripti
REM Kullanim: Bu dosyayi cift tikla (Windows'ta)
REM Gereksinim: Python 3.10-3.12 kurulu olmali (python.org)
REM ============================================

echo [1/4] Python kontrol ediliyor...
python --version
if errorlevel 1 (
    echo HATA: Python bulunamadi. Once https://python.org adresinden Python kurun.
    echo Kurulumda "Add Python to PATH" kutusunu isaretlemeyi unutmayin.
    pause
    exit /b 1
)

echo [2/4] Gerekli kutuphaneler kuruluyor...
pip install kivy pyinstaller numpy --quiet

echo [3/4] Sprite'lar ve muzikler olusturuluyor...
python gen_assets.py
python gen_assets_phase1.py
python gen_assets_phase2.py
python gen_assets_phase3.py
python gen_music.py
python gen_sfx.py

echo [4/4] EXE derleniyor (birkac dakika surebilir)...
pyinstaller --onefile --windowed --name SpaceWarx ^
    --add-data "assets;assets" ^
    --add-data "fonts;fonts" ^
    main.py

echo.
echo ============================================
echo TAMAMLANDI! EXE dosyaniz: dist\SpaceWarx.exe
echo ============================================
pause
