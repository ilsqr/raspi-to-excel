# Raspberry Pi OCR to Excel

Raspberry Pi üzerinde çalışan, kamera görüntüsündeki sayıları OCR (Optical Character Recognition) ile tanıyıp Excel dosyasına kaydeden Python uygulaması.

## 🌟 Özellikler

- 📷 **Çoklu Kamera Desteği**: Raspberry Pi Camera Module ve USB webcam desteği
- 🔍 **Gelişmiş OCR**: Tesseract OCR ile yüksek doğrulukta sayı tanıma
- 📊 **Excel Entegrasyonu**: Otomatik Excel (.xlsx) dosyası oluşturma ve güncelleme
- ⏰ **Zaman Damgası**: Her kayıt için tarih ve saat bilgisi
- 🎨 **Görüntü Ön İşleme**: OCR doğruluğunu artırmak için otomatik görüntü işleme
- 📝 **Loglama**: Detaylı log kayıtları ve hata yönetimi
- ⚙️ **Yapılandırılabilir**: Kolay özelleştirme için config dosyası
- 🔄 **Sürekli Mod**: Belirli aralıklarla otomatik görüntü yakalama
- 💾 **Görüntü Kaydetme**: İşlenen ve orijinal görüntüleri saklama

## 📋 Gereksinimler

### Donanım
- Raspberry Pi (3/4/5 veya Zero W)
- Raspberry Pi Camera Module veya USB webcam
- 8GB+ SD kart
- İnternet bağlantısı (kurulum için)

### Yazılım
- Raspberry Pi OS (Debian tabanlı)
- Python 3.7 veya üzeri

## 🚀 Kurulum

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/ilsqr/raspi-to-excel.git
cd raspi-to-excel
```

### 2. Kurulum Scriptini Çalıştırın

```bash
sudo ./setup.sh
```

Bu script:
- Sistem güncellemesi yapar
- Tesseract OCR ve bağımlılıklarını kurar
- OpenCV ve görüntü işleme kütüphanelerini kurar
- Python paketlerini yükler
- İsteğe bağlı olarak Python sanal ortamı oluşturur

### 3. Manuel Kurulum (Alternatif)

Eğer `setup.sh` scriptini kullanmak istemiyorsanız:

```bash
# Sistem paketleri
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-tur
sudo apt-get install -y python3 python3-pip python3-venv

# Python sanal ortamı (önerilen)
python3 -m venv venv
source venv/bin/activate

# Python paketleri
pip install --upgrade pip
pip install -r requirements.txt
```

## 💻 Kullanım

### Temel Kullanım

Tek bir görüntü yakalama ve işleme:

```bash
python3 capture_numbers.py
```

### Sürekli Çalışma Modu

Belirli aralıklarla otomatik görüntü yakalama:

```bash
python3 capture_numbers.py --continuous
```

### Özel Yapılandırma

```bash
python3 capture_numbers.py --config my_config.py
```

### Sanal Ortam Kullanımı

Eğer kurulum sırasında sanal ortam oluşturduysanız:

```bash
source venv/bin/activate
python3 capture_numbers.py
deactivate  # Çıkış için
```

## ⚙️ Yapılandırma

`config.py` dosyasını düzenleyerek programı özelleştirebilirsiniz:

### Kamera Ayarları

```python
CAMERA_TYPE = "auto"  # "picamera", "usb", "auto"
CAMERA_INDEX = 0      # USB kamera indeksi
CAMERA_RESOLUTION = (1280, 720)
```

### OCR Ayarları

```python
TESSERACT_LANG = 'eng'  # OCR dili
MIN_CONFIDENCE = 60     # Minimum güven skoru (%)
```

### Görüntü İşleme

```python
IMAGE_PREPROCESSING = True  # Ön işlemeyi etkinleştir
GRAYSCALE = True           # Gri tonlama
THRESHOLD = True           # Eşikleme
DENOISE = True             # Gürültü azaltma
RESIZE_FACTOR = 2.0        # Büyütme faktörü
```

### Excel Ayarları

```python
EXCEL_FILE = "ocr_results.xlsx"
EXCEL_SHEET = "Sayılar"
APPEND_MODE = True  # Mevcut dosyaya ekle
```

### Sürekli Mod Ayarları

```python
CONTINUOUS_MODE = False
CAPTURE_INTERVAL = 5    # Saniye
MAX_CAPTURES = 100      # 0 = sınırsız
```

## 📂 Çıktı Dosyaları

### Excel Dosyası

Program aşağıdaki sütunları içeren bir Excel dosyası oluşturur:

| Tarih | Saat | Sayı | Güven (%) |
|-------|------|------|-----------|
| 2026-01-01 | 15:30:45 | 12345 | 95.5 |
| 2026-01-01 | 15:31:00 | 67890 | 92.3 |

### Log Dosyası

`ocr_log.txt` dosyasında detaylı işlem logları saklanır:

```
2026-01-01 15:30:45 - INFO - Raspberry Pi OCR to Excel başlatılıyor...
2026-01-01 15:30:47 - INFO - USB kamera başarıyla başlatıldı
2026-01-01 15:30:50 - INFO - OCR sonucu: '12345' (Güven: 95.5%)
```

### Görüntü Dosyaları

`captured_images/` klasöründe:
- `original_YYYYMMDD_HHMMSS.jpg` - Orijinal görüntüler
- `processed_YYYYMMDD_HHMMSS.jpg` - İşlenmiş görüntüler

## 🔧 Sorun Giderme

### Kamera Algılanmıyor

**Raspberry Pi Camera Module:**
```bash
# Kamera interface'ini etkinleştirin
sudo raspi-config
# 3. Interface Options > Camera > Enable

# Test edin
libcamera-hello
```

**USB Webcam:**
```bash
# Kamerayı listeleyin
ls -l /dev/video*

# Test edin
v4l2-ctl --list-devices
```

### OCR Düşük Doğruluk

1. `config.py` dosyasında `RESIZE_FACTOR` değerini artırın (örn. 3.0)
2. Aydınlatmayı iyileştirin
3. Kamera odağını ayarlayın
4. `THRESHOLD_METHOD` ayarını değiştirin ('adaptive' veya 'otsu')

### Tesseract Dil Paketi Eksik

```bash
# Türkçe dil paketi
sudo apt-get install tesseract-ocr-tur

# Diğer diller için
sudo apt-get install tesseract-ocr-[dil_kodu]
```

### İzin Hataları

```bash
# Kullanıcıyı video grubuna ekleyin
sudo usermod -a -G video $USER

# Yeniden giriş yapın veya reboot edin
```

### OpenCV Kurulum Hataları

Raspberry Pi'da OpenCV kurulumu uzun sürebilir. Önceden derlenmiş wheel kullanın:

```bash
pip install opencv-python-headless
```

## 📖 API Dokümantasyonu

### CameraCapture

```python
camera = CameraCapture(
    camera_type="auto",    # "picamera", "usb", "auto"
    camera_index=0,        # USB kamera indeksi
    resolution=(1280, 720) # Çözünürlük
)
image = camera.capture_image()
camera.release()
```

### ImageProcessor

```python
# Görüntü ön işleme
processed = ImageProcessor.preprocess_image(image)

# OCR ile sayı çıkarma
result = ImageProcessor.extract_numbers(image)
# result = {
#     'text': '12345',
#     'confidence': 95.5,
#     'processed_image': numpy_array
# }
```

### ExcelWriter

```python
writer = ExcelWriter("output.xlsx", "Sheet1")
writer.write_data(
    number_text="12345",
    confidence=95.5,
    timestamp=datetime.now()
)
```

## 🧪 Test

### Manuel Test

1. Test görüntüsü hazırlayın (sayılar içeren)
2. Programı çalıştırın
3. Excel dosyasını kontrol edin

### Kamera Testi

```python
import cv2

# USB kamera testi
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if ret:
    cv2.imwrite("test.jpg", frame)
    print("✓ Kamera çalışıyor")
cap.release()
```

### OCR Testi

```python
import pytesseract
from PIL import Image

img = Image.open("test_image.jpg")
text = pytesseract.image_to_string(img)
print(f"OCR sonucu: {text}")
```

## 🎯 Kullanım Senaryoları

### Senaryo 1: Enerji Sayacı Okuma

```python
# config.py
CAMERA_TYPE = "usb"
CONTINUOUS_MODE = True
CAPTURE_INTERVAL = 60  # Her dakika
EXCEL_FILE = "enerji_sayaci.xlsx"
```

### Senaryo 2: Araç Plaka Tanıma

```python
# config.py
TESSERACT_CONFIG = '--oem 3 --psm 7'
MIN_CONFIDENCE = 70
SAVE_IMAGES = True
```

### Senaryo 3: Üretim Hattı Sayma

```python
# config.py
CONTINUOUS_MODE = True
CAPTURE_INTERVAL = 5
MAX_CAPTURES = 1000
```

## 🔒 Güvenlik

- Hassas verileri `config.py` yerine `config_local.py` dosyasında saklayın
- `.gitignore` dosyası bu dosyayı otomatik olarak hariç tutar
- Excel dosyalarını düzenli olarak yedekleyin

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🙏 Teşekkürler

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [OpenCV](https://opencv.org/)
- [Raspberry Pi Foundation](https://www.raspberrypi.org/)

## 📞 İletişim

Sorularınız için issue açabilirsiniz.

## 🔄 Değişiklik Geçmişi

### v1.0.0 (2026-01-01)
- İlk sürüm
- Temel OCR ve Excel entegrasyonu
- Çoklu kamera desteği
- Görüntü ön işleme
- Sürekli çalışma modu

---

**Not**: Bu proje Raspberry Pi üzerinde test edilmiştir ancak genel Linux sistemlerinde de çalışabilir.
