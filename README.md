# SpaceWarx - 2D Pixel Art Uzay Ucus Oyunu

## Durum: Faz 1 + Faz 2 tamamlandi (temel akis calisiyor)

### Tamamlanan
- [x] Splash ekrani (siyah kare fade-out animasyonu)
- [x] Yukleme bari + 7 dilli bayrak secimi (TR/EN/FR/PT/RU/JP/CN)
- [x] Pixelli ogretici (yukari/sag/sol surukleme, SUCCESS animasyonu)
- [x] Ana menu: kullanici adi sorma, altin/elmas bari, uzay temali
      hareketli arkaplan, sandik/oynat/harita butonlari, yukseltme butonu
- [x] JSON tabanli kayit sistemi (kullanici adi, altin, elmas kalici)
- [x] Tum pixel art sprite'lar kod ile uretildi (assets/ klasoru)

### Sirada (Faz 3-6)
- [ ] Cekirdek oynanis: surukle kontrol, 5'li kirmizi dusman filosu, ates/carpisma
- [ ] Can bari, kalkan/heal/lazer yetenekleri (sol alt daireler)
- [ ] Sonsuz bolum sistemi + her 20 bolumde boss
- [ ] Altin/elmas drop animasyonlari
- [ ] Sandik/magaza ekrani (gunluk teklifler)
- [ ] Uzay haritasi (kampanya ekrani)
- [ ] Karakter/ucak yukseltme + 5 yardimci ucak sistemi

## Nasil calistirilir (test icin, bilgisayarinda)
```bash
pip install -r requirements.txt
python gen_assets.py
python gen_assets_phase1.py
python gen_assets_phase2.py
python gen_assets_phase3.py
python gen_music.py
python gen_sfx.py
python main.py
```

## .exe olusturmak icin (Windows'ta)
`build_windows_exe.bat` dosyasina cift tikla.

## .apk olusturmak icin (Android)
`ANDROID_BUILD_TALIMATI.md` dosyasindaki adimlari izle (WSL/Linux gerekir).
