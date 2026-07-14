# SpaceWarx - Android APK Nasil Derlenir?

## ONERILEN: APK_KOLAY_YONTEM.md dosyasina bak!
Bilgisayarina hicbir sey kurmadan, GitHub'in ucretsiz sunuculariyla otomatik
APK derletebilirsin. Asagidaki WSL yontemi ise manuel/ileri seviye alternatiftir.

---



Buildozer sadece Linux'ta calisir. Windows kullaniyorsan **WSL (Windows Subsystem for Linux)** kurman gerekir.

## WSL kurulumu (Windows'ta, sadece bir kere)
1. PowerShell'i yonetici olarak ac, sunu yaz: `wsl --install`
2. Bilgisayari yeniden baslat
3. Acilan Ubuntu penceresinde kullanici adi/sifre olustur

## APK derleme adimlari (WSL/Ubuntu terminalinde)

```bash
# 1) Gerekli sistem paketlerini kur
sudo apt update
sudo apt install -y python3-pip python3-venv git zip unzip openjdk-17-jdk \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev cmake

# 2) Buildozer kur
pip install --user buildozer cython numpy

# 3) Proje klasorune gir (bu klasoru WSL'e kopyala)
cd skygame

# 4) Sprite'lari ve muzikleri olustur
python3 gen_assets.py
python3 gen_assets_phase1.py
python3 gen_assets_phase2.py
python3 gen_assets_phase3.py
python3 gen_music.py
python3 gen_sfx.py

# 5) APK derle (ilk seferde Android SDK/NDK indirir, 20-40 dakika surebilir)
~/.local/bin/buildozer -v android debug
```

Derleme bitince APK dosyan burada olacak:
`bin/spacewarx-0.1-arm64-v8a_armeabi-v7a-debug.apk`

Bu dosyayi telefonuna atip yukleyebilir, ya da Play Store'a atmadan once
`buildozer android release` komutuyla imzali surum olusturabilirsin.

## Play Store icin onemli not
Google Play artik **.aab** (Android App Bundle) formatini istiyor, sade .apk degil.
`buildozer.spec` icinde release ayarlarini yapip:
```bash
buildozer android release
```
komutunu calistirinca hem apk hem gerekli dosyalar `bin/` klasorunde olusur.
imzalama (keystore) icin Google'in resmi dokumantasyonunu takip et:
https://developer.android.com/studio/publish/app-signing
