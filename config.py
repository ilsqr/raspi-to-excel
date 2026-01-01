"""
Yapılandırma Ayarları
Bu dosyayı düzenleyerek programın davranışını özelleştirebilirsiniz.
"""

# Kamera Ayarları
CAMERA_TYPE = "auto"  # "picamera", "usb", "auto" (otomatik algıla)
CAMERA_INDEX = 0  # USB kamera için cihaz indeksi
CAMERA_RESOLUTION = (1280, 720)  # Görüntü çözünürlüğü (genişlik, yükseklik)
CAMERA_WARMUP_TIME = 2  # Kamera ısınma süresi (saniye)

# OCR Ayarları
TESSERACT_CONFIG = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.'  # Sadece sayılar ve nokta
TESSERACT_LANG = 'eng'  # OCR dili ('eng' veya 'tur')
MIN_CONFIDENCE = 60  # Minimum güven skoru (0-100)

# Görüntü Ön İşleme Ayarları
IMAGE_PREPROCESSING = True  # Görüntü ön işlemeyi etkinleştir
GRAYSCALE = True  # Gri tonlamaya çevir
THRESHOLD = True  # Eşikleme uygula
THRESHOLD_METHOD = 'adaptive'  # 'adaptive' veya 'otsu'
DENOISE = True  # Gürültü azaltma
RESIZE_FACTOR = 2.0  # Görüntüyü büyütme faktörü (OCR doğruluğu için)

# Excel Ayarları
EXCEL_FILE = "ocr_results.xlsx"  # Çıktı Excel dosyası
EXCEL_SHEET = "Sayılar"  # Excel sheet ismi
APPEND_MODE = True  # Mevcut dosyaya ekle (False ise üzerine yaz)

# Loglama Ayarları
LOG_FILE = "ocr_log.txt"  # Log dosyası
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_TO_CONSOLE = True  # Konsola da log yazdır

# Çalışma Modu
CONTINUOUS_MODE = False  # Sürekli çalışma modu (True) veya tek çekim (False)
CAPTURE_INTERVAL = 5  # Sürekli modda çekimler arası bekleme (saniye)
MAX_CAPTURES = 100  # Sürekli modda maksimum çekim sayısı (0 = sınırsız)

# Görüntü Kaydetme
SAVE_IMAGES = True  # Yakalanan görüntüleri kaydet
IMAGE_OUTPUT_DIR = "captured_images"  # Görüntülerin kaydedileceği klasör
SAVE_PROCESSED_IMAGES = True  # İşlenmiş görüntüleri de kaydet

# Hata Yönetimi
MAX_RETRIES = 3  # Başarısız OCR denemelerinde maksimum tekrar sayısı
RETRY_DELAY = 1  # Tekrar denemeleri arasındaki bekleme (saniye)
