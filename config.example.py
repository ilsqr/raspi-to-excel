"""
Örnek Yapılandırma Dosyası
Bu dosyayı kopyalayıp düzenleyerek özel ayarlar oluşturabilirsiniz.

Kullanım:
    cp config.example.py my_config.py
    # my_config.py dosyasını düzenleyin
    python3 capture_numbers.py --config my_config.py
"""

# ============================================
# SENARYO 1: Enerji Sayacı Okuma
# ============================================
# CAMERA_TYPE = "usb"
# CAMERA_INDEX = 0
# CAMERA_RESOLUTION = (1920, 1080)
# 
# TESSERACT_LANG = 'eng'
# MIN_CONFIDENCE = 70
# 
# CONTINUOUS_MODE = True
# CAPTURE_INTERVAL = 60  # Her dakika bir okuma
# MAX_CAPTURES = 1440    # 24 saat (60 dakika x 24)
# 
# EXCEL_FILE = "enerji_sayaci_okumalari.xlsx"
# EXCEL_SHEET = "Günlük Okumalar"
# 
# SAVE_IMAGES = True
# IMAGE_OUTPUT_DIR = "sayac_goruntuleri"

# ============================================
# SENARYO 2: Yüksek Hızlı Sayma
# ============================================
# CAMERA_TYPE = "picamera"
# CAMERA_RESOLUTION = (640, 480)  # Düşük çözünürlük = hızlı işleme
# 
# IMAGE_PREPROCESSING = True
# RESIZE_FACTOR = 1.5  # Daha az büyütme
# 
# CONTINUOUS_MODE = True
# CAPTURE_INTERVAL = 1  # Her saniye
# MAX_CAPTURES = 0      # Sınırsız
# 
# EXCEL_FILE = "hizli_sayim.xlsx"
# SAVE_IMAGES = False   # Hız için görüntü kaydetme

# ============================================
# SENARYO 3: Yüksek Doğruluk OCR
# ============================================
# CAMERA_TYPE = "usb"
# CAMERA_RESOLUTION = (2560, 1440)  # Yüksek çözünürlük
# 
# IMAGE_PREPROCESSING = True
# GRAYSCALE = True
# THRESHOLD = True
# THRESHOLD_METHOD = 'otsu'
# DENOISE = True
# RESIZE_FACTOR = 3.0  # Maksimum büyütme
# 
# MIN_CONFIDENCE = 90  # Yüksek güven eşiği
# 
# SAVE_IMAGES = True
# SAVE_PROCESSED_IMAGES = True
# 
# LOG_LEVEL = "DEBUG"  # Detaylı loglama

# ============================================
# SENARYO 4: Test Modu
# ============================================
# CAMERA_TYPE = "usb"
# CAMERA_INDEX = 0
# CAMERA_RESOLUTION = (1280, 720)
# 
# CONTINUOUS_MODE = False  # Tek çekim
# 
# SAVE_IMAGES = True
# SAVE_PROCESSED_IMAGES = True
# 
# LOG_LEVEL = "DEBUG"
# LOG_TO_CONSOLE = True
# 
# EXCEL_FILE = "test_results.xlsx"

# ============================================
# VARSAYILAN AYARLAR (config.py ile aynı)
# ============================================

# Kamera Ayarları
CAMERA_TYPE = "auto"
CAMERA_INDEX = 0
CAMERA_RESOLUTION = (1280, 720)
CAMERA_WARMUP_TIME = 2

# OCR Ayarları
TESSERACT_CONFIG = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.'
TESSERACT_LANG = 'eng'
MIN_CONFIDENCE = 60

# Görüntü Ön İşleme Ayarları
IMAGE_PREPROCESSING = True
GRAYSCALE = True
THRESHOLD = True
THRESHOLD_METHOD = 'adaptive'
DENOISE = True
RESIZE_FACTOR = 2.0

# Excel Ayarları
EXCEL_FILE = "ocr_results.xlsx"
EXCEL_SHEET = "Sayılar"
APPEND_MODE = True

# Loglama Ayarları
LOG_FILE = "ocr_log.txt"
LOG_LEVEL = "INFO"
LOG_TO_CONSOLE = True

# Çalışma Modu
CONTINUOUS_MODE = False
CAPTURE_INTERVAL = 5
MAX_CAPTURES = 100

# Görüntü Kaydetme
SAVE_IMAGES = True
IMAGE_OUTPUT_DIR = "captured_images"
SAVE_PROCESSED_IMAGES = True

# Hata Yönetimi
MAX_RETRIES = 3
RETRY_DELAY = 1
