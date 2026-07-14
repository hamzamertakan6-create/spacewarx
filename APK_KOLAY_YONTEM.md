# EN KOLAY YOL: GitHub Uzerinden Otomatik APK Derleme (bilgisayarina hicbir sey kurmadan)

Bu yontemde APK'yi SENIN bilgisayarin degil, GitHub'in ucretsiz sunuculari derler.
Senin yapman gereken tek sey dosyalari GitHub'a yuklemek. ~10-15 dakika surer.

## Adim 1: GitHub hesabi ac (yoksa)
https://github.com/signup adresinden ucretsiz hesap ac (kredi karti istemez).

## Adim 2: Yeni bir repo (proje) olustur
1. Sag ustteki **+** isaretine tikla -> **New repository**
2. Repository name: `spacewarx` yaz
3. **Public** secili kalsin (ucretsiz Actions dakikasi icin gerekli)
4. **Create repository** butonuna tikla

## Adim 3: Bu klasordeki TUM dosyalari yukle
1. Az once acilan sayfada **"uploading an existing file"** linkine tikla
   (veya "Add file" -> "Upload files")
2. Bu zip'i actiktan sonra icindeki TUM dosya ve klasorleri
   (main.py, assets/, fonts/, gen_*.py, .github/ klasoru dahil HEPSI)
   surukle-birak ile yukleme alanina at
   - ONEMLI: `.github` klasorunun de yuklendiginden emin ol (bazen gizli klasorler
     gorunmeyebilir; dosya secme penceresinden "Gizli dosyalari goster" secenegini ac)
3. Altta "Commit changes" butonuna tikla

## Adim 4: Otomatik derlemeyi izle
1. Repo sayfasinda ust menuden **Actions** sekmesine tikla
2. "Build APK" adinda bir islem baslamis olacak (sari nokta = calisiyor,
   yesil tik = bitti, kirmizi X = hata)
3. Ilk derleme Android SDK/NDK indirdigi icin **20-35 dakika** surebilir,
   sabirli ol

## Adim 5: APK'yi indir
1. Islem yesil tik ile bitince, o islemin sayfasina tikla
2. En altta **Artifacts** bolumunde **SpaceWarx-apk** dosyasini goreceksin
3. Ona tikla, bilgisayarina zip olarak iner, icinde .apk dosyan var
4. O .apk dosyasini telefonuna aktar (WhatsApp, Google Drive, USB kablo -
   hangisi kolayina geliyorsa) ve telefonda dosyaya tiklayip kur
   (Ayarlar -> Guvenlik -> "Bilinmeyen kaynaklardan yukleme" izni istenebilir)

## Bir seyler ters giderse
Actions sekmesinde kirmizi X gorursen, o islemin uzerine tikla, kirmizi
satirlarda hata mesaji yazar - o mesaji bana gonder, birlikte cozeriz.

## Play Store'a atmak icin
Bu debug APK'dir, sadece test/kurulum icindir. Play Store'a atmadan once
imzali (release) surum ve .aab formati gerekir - ANDROID_BUILD_TALIMATI.md
dosyasindaki "Play Store icin onemli not" bolumune bak.
