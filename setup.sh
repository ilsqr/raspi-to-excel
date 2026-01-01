#!/bin/bash

# Raspberry Pi OCR to Excel - Kurulum Scripti
# Bu script gerekli sistem bağımlılıklarını ve Python paketlerini kurar

echo "====================================="
echo "Raspberry Pi OCR to Excel Kurulumu"
echo "====================================="
echo ""

# Root kontrolü
if [ "$EUID" -ne 0 ]; then 
    echo "Bu scripti root olarak çalıştırın: sudo ./setup.sh"
    exit 1
fi

# Sistem güncellemesi
echo "Sistem güncelleniyor..."
apt-get update

# Tesseract OCR kurulumu
echo ""
echo "Tesseract OCR kuruluyor..."
apt-get install -y tesseract-ocr tesseract-ocr-tur tesseract-ocr-eng

# OpenCV bağımlılıkları
echo ""
echo "OpenCV bağımlılıkları kuruluyor..."
apt-get install -y libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test

# Görüntü işleme kütüphaneleri
echo ""
echo "Görüntü işleme kütüphaneleri kuruluyor..."
apt-get install -y libjpeg-dev libtiff-dev libpng-dev
apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
apt-get install -y libxvidcore-dev libx264-dev

# Python ve pip kontrolü
echo ""
echo "Python ve pip kontrol ediliyor..."
apt-get install -y python3 python3-pip python3-dev

# Raspberry Pi kamera modülü desteği
echo ""
read -p "Raspberry Pi Camera Module kullanıyor musunuz? (e/h): " camera_choice
if [ "$camera_choice" = "e" ] || [ "$camera_choice" = "E" ]; then
    echo "Raspberry Pi Camera desteği etkinleştiriliyor..."
    apt-get install -y python3-picamera2
fi

# Python sanal ortam (opsiyonel ama önerilen)
echo ""
read -p "Python sanal ortamı (virtual environment) oluşturulsun mu? (e/h): " venv_choice
if [ "$venv_choice" = "e" ] || [ "$venv_choice" = "E" ]; then
    apt-get install -y python3-venv
    echo "Sanal ortam oluşturuluyor..."
    sudo -u $SUDO_USER python3 -m venv venv
    echo "Sanal ortam oluşturuldu. Aktif etmek için: source venv/bin/activate"
    
    # Sanal ortamda paketleri kur
    echo "Python paketleri sanal ortama kuruluyor..."
    sudo -u $SUDO_USER venv/bin/pip install --upgrade pip
    sudo -u $SUDO_USER venv/bin/pip install -r requirements.txt
else
    # Sistem geneline kur
    echo "Python paketleri sistem geneline kuruluyor..."
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
fi

echo ""
echo "====================================="
echo "Kurulum tamamlandı!"
echo "====================================="
echo ""
echo "Kullanım:"
if [ "$venv_choice" = "e" ] || [ "$venv_choice" = "E" ]; then
    echo "1. Sanal ortamı aktif edin: source venv/bin/activate"
    echo "2. Scripti çalıştırın: python capture_numbers.py"
else
    echo "python3 capture_numbers.py"
fi
echo ""
echo "Yapılandırma için config.py dosyasını düzenleyin."
echo ""
