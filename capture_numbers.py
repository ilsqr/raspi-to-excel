#!/usr/bin/env python3
"""
Raspberry Pi OCR to Excel
Kamera görüntüsündeki sayıları OCR ile tanıyıp Excel'e kaydeden script

Kullanım:
    python3 capture_numbers.py
    python3 capture_numbers.py --continuous
    python3 capture_numbers.py --config custom_config.py
"""

import os
import sys
import time
import logging
import argparse
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import pytesseract
from PIL import Image
import pandas as pd
from openpyxl import load_workbook, Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# Yapılandırma dosyasını içe aktar
import config


class CameraCapture:
    """Kamera görüntüsü yakalama sınıfı"""
    
    def __init__(self, camera_type="auto", camera_index=0, resolution=(1280, 720)):
        self.camera_type = camera_type
        self.camera_index = camera_index
        self.resolution = resolution
        self.camera = None
        self.use_picamera = False
        
        self._initialize_camera()
    
    def _initialize_camera(self):
        """Kamera başlatma"""
        if self.camera_type == "picamera":
            self.use_picamera = self._try_picamera()
        elif self.camera_type == "usb":
            self.use_picamera = False
            self._init_usb_camera()
        else:  # auto
            # Önce PiCamera dene, olmazsa USB kamera
            self.use_picamera = self._try_picamera()
            if not self.use_picamera:
                self._init_usb_camera()
    
    def _try_picamera(self):
        """PiCamera2 başlatmayı dene"""
        try:
            from picamera2 import Picamera2
            logging.info("PiCamera2 başlatılıyor...")
            self.camera = Picamera2()
            camera_config = self.camera.create_still_configuration(
                main={"size": self.resolution}
            )
            self.camera.configure(camera_config)
            self.camera.start()
            time.sleep(config.CAMERA_WARMUP_TIME)
            logging.info("PiCamera2 başarıyla başlatıldı")
            return True
        except ImportError:
            logging.warning("picamera2 modülü bulunamadı, USB kamera kullanılacak")
            return False
        except Exception as e:
            logging.warning(f"PiCamera başlatılamadı: {e}, USB kamera deneniyor...")
            return False
    
    def _init_usb_camera(self):
        """USB kamera başlat"""
        try:
            logging.info(f"USB kamera (index: {self.camera_index}) başlatılıyor...")
            self.camera = cv2.VideoCapture(self.camera_index)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            
            if not self.camera.isOpened():
                raise Exception("USB kamera açılamadı")
            
            # Kamerayı ısıt
            time.sleep(config.CAMERA_WARMUP_TIME)
            # İlk birkaç frame'i at (kamera stabilizasyonu için)
            for _ in range(5):
                self.camera.read()
            
            logging.info("USB kamera başarıyla başlatıldı")
        except Exception as e:
            logging.error(f"USB kamera başlatılamadı: {e}")
            raise
    
    def capture_image(self):
        """Görüntü yakala"""
        try:
            if self.use_picamera:
                # PiCamera2 ile yakala
                image_array = self.camera.capture_array()
                # RGB'den BGR'ye çevir (OpenCV için)
                image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            else:
                # USB kamera ile yakala
                ret, image = self.camera.read()
                if not ret:
                    raise Exception("Görüntü yakalanamadı")
            
            logging.info("Görüntü başarıyla yakalandı")
            return image
        except Exception as e:
            logging.error(f"Görüntü yakalama hatası: {e}")
            raise
    
    def release(self):
        """Kamera kaynaklarını serbest bırak"""
        try:
            if self.use_picamera and self.camera:
                self.camera.stop()
                self.camera.close()
            elif not self.use_picamera and self.camera:
                self.camera.release()
            logging.info("Kamera kaynakları serbest bırakıldı")
        except Exception as e:
            logging.error(f"Kamera kapatma hatası: {e}")


class ImageProcessor:
    """Görüntü işleme ve OCR sınıfı"""
    
    @staticmethod
    def preprocess_image(image):
        """Görüntüyü OCR için ön işle"""
        processed = image.copy()
        
        # Gri tonlamaya çevir
        if config.GRAYSCALE:
            processed = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
        
        # Görüntüyü büyüt (daha iyi OCR için)
        if config.RESIZE_FACTOR != 1.0:
            new_width = int(processed.shape[1] * config.RESIZE_FACTOR)
            new_height = int(processed.shape[0] * config.RESIZE_FACTOR)
            processed = cv2.resize(processed, (new_width, new_height), 
                                   interpolation=cv2.INTER_CUBIC)
        
        # Gürültü azaltma
        if config.DENOISE:
            processed = cv2.fastNlMeansDenoising(processed)
        
        # Eşikleme (thresholding)
        if config.THRESHOLD:
            if config.THRESHOLD_METHOD == 'adaptive':
                processed = cv2.adaptiveThreshold(
                    processed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY, 11, 2
                )
            else:  # otsu
                _, processed = cv2.threshold(
                    processed, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )
        
        return processed
    
    @staticmethod
    def extract_numbers(image):
        """OCR ile görüntüden sayıları çıkar"""
        try:
            # Görüntüyü ön işle
            if config.IMAGE_PREPROCESSING:
                processed_image = ImageProcessor.preprocess_image(image)
            else:
                processed_image = image
            
            # PIL formatına çevir
            pil_image = Image.fromarray(processed_image)
            
            # OCR uygula
            text = pytesseract.image_to_string(
                pil_image,
                lang=config.TESSERACT_LANG,
                config=config.TESSERACT_CONFIG
            )
            
            # OCR detaylarını al (güven skorları için)
            data = pytesseract.image_to_data(
                pil_image,
                lang=config.TESSERACT_LANG,
                config=config.TESSERACT_CONFIG,
                output_type=pytesseract.Output.DICT
            )
            
            # Güven skoru hesapla
            confidences = [int(conf) for conf in data['conf'] if conf != '-1']
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # Metni temizle
            text = text.strip()
            
            logging.info(f"OCR sonucu: '{text}' (Güven: {avg_confidence:.1f}%)")
            
            return {
                'text': text,
                'confidence': avg_confidence,
                'processed_image': processed_image
            }
        
        except Exception as e:
            logging.error(f"OCR hatası: {e}")
            raise


class ExcelWriter:
    """Excel dosyası yazma sınıfı"""
    
    def __init__(self, filename, sheet_name="Sayılar"):
        self.filename = filename
        self.sheet_name = sheet_name
    
    def write_data(self, number_text, confidence, timestamp=None):
        """Veriyi Excel dosyasına yaz"""
        try:
            if timestamp is None:
                timestamp = datetime.now()
            
            # Veri satırı oluştur
            data = {
                'Tarih': [timestamp.strftime('%Y-%m-%d')],
                'Saat': [timestamp.strftime('%H:%M:%S')],
                'Sayı': [number_text],
                'Güven (%)': [round(confidence, 2)]
            }
            
            df = pd.DataFrame(data)
            
            # Dosya varsa ve ekleme modu aktifse
            if os.path.exists(self.filename) and config.APPEND_MODE:
                # Mevcut dosyayı oku
                with pd.ExcelFile(self.filename) as xls:
                    if self.sheet_name in xls.sheet_names:
                        existing_df = pd.read_excel(xls, sheet_name=self.sheet_name)
                        df = pd.concat([existing_df, df], ignore_index=True)
                
                # Dosyaya yaz
                with pd.ExcelWriter(self.filename, engine='openpyxl', mode='a', 
                                    if_sheet_exists='replace') as writer:
                    df.to_excel(writer, sheet_name=self.sheet_name, index=False)
            else:
                # Yeni dosya oluştur
                with pd.ExcelWriter(self.filename, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name=self.sheet_name, index=False)
            
            logging.info(f"Veri Excel'e yazıldı: {self.filename}")
            return True
        
        except Exception as e:
            logging.error(f"Excel yazma hatası: {e}")
            raise


def setup_logging():
    """Loglama yapılandırması"""
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    
    handlers = []
    
    # Dosya handler
    if config.LOG_FILE:
        file_handler = logging.FileHandler(config.LOG_FILE, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(file_handler)
    
    # Konsol handler
    if config.LOG_TO_CONSOLE:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(console_handler)
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=handlers
    )


def save_image(image, prefix="capture"):
    """Görüntüyü diske kaydet"""
    if not config.SAVE_IMAGES:
        return None
    
    try:
        # Çıktı klasörünü oluştur
        output_dir = Path(config.IMAGE_OUTPUT_DIR)
        output_dir.mkdir(exist_ok=True)
        
        # Dosya adı oluştur
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = output_dir / f"{prefix}_{timestamp}.jpg"
        
        # Görüntüyü kaydet
        cv2.imwrite(str(filename), image)
        logging.info(f"Görüntü kaydedildi: {filename}")
        
        return str(filename)
    
    except Exception as e:
        logging.error(f"Görüntü kaydetme hatası: {e}")
        return None


def process_single_capture(camera, excel_writer):
    """Tek bir görüntü yakalama ve işleme"""
    try:
        # Görüntü yakala
        image = camera.capture_image()
        
        # Orijinal görüntüyü kaydet
        if config.SAVE_IMAGES:
            save_image(image, "original")
        
        # OCR işlemi
        result = ImageProcessor.extract_numbers(image)
        
        # İşlenmiş görüntüyü kaydet
        if config.SAVE_PROCESSED_IMAGES and config.SAVE_IMAGES:
            save_image(result['processed_image'], "processed")
        
        # Güven skoru kontrolü
        if result['confidence'] < config.MIN_CONFIDENCE:
            logging.warning(
                f"Düşük güven skoru: {result['confidence']:.1f}% "
                f"(Minimum: {config.MIN_CONFIDENCE}%)"
            )
            print(f"⚠ Uyarı: Düşük güven skoru. OCR sonucu güvenilir olmayabilir.")
        
        # Excel'e yaz
        if result['text']:
            excel_writer.write_data(result['text'], result['confidence'])
            print(f"✓ Tanınan sayı: {result['text']} (Güven: {result['confidence']:.1f}%)")
            return True
        else:
            logging.warning("OCR sonucu boş")
            print("⚠ Görüntüde sayı algılanamadı")
            return False
    
    except Exception as e:
        logging.error(f"İşlem hatası: {e}")
        print(f"✗ Hata: {e}")
        return False


def main():
    """Ana fonksiyon"""
    # Komut satırı argümanları
    parser = argparse.ArgumentParser(
        description='Raspberry Pi OCR to Excel - Kameradan sayı tanıma'
    )
    parser.add_argument(
        '--continuous', '-c',
        action='store_true',
        help='Sürekli çalışma modu'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Özel yapılandırma dosyası'
    )
    args = parser.parse_args()
    
    # Yapılandırmayı yükle
    if args.config:
        # Özel config dosyasını yükle
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", args.config)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)
        globals()['config'] = config_module
    
    # Loglama başlat
    setup_logging()
    logging.info("=" * 50)
    logging.info("Raspberry Pi OCR to Excel başlatılıyor...")
    logging.info("=" * 50)
    
    # Sürekli mod kontrolü
    continuous = args.continuous or config.CONTINUOUS_MODE
    
    camera = None
    try:
        # Kamerayı başlat
        print("Kamera başlatılıyor...")
        camera = CameraCapture(
            camera_type=config.CAMERA_TYPE,
            camera_index=config.CAMERA_INDEX,
            resolution=config.CAMERA_RESOLUTION
        )
        print("✓ Kamera hazır")
        
        # Excel writer oluştur
        excel_writer = ExcelWriter(config.EXCEL_FILE, config.EXCEL_SHEET)
        print(f"✓ Excel dosyası: {config.EXCEL_FILE}")
        
        if continuous:
            # Sürekli çalışma modu
            print(f"\n📸 Sürekli çalışma modu aktif")
            print(f"   Çekim aralığı: {config.CAPTURE_INTERVAL} saniye")
            if config.MAX_CAPTURES > 0:
                print(f"   Maksimum çekim: {config.MAX_CAPTURES}")
            print("   Durdurmak için Ctrl+C basın\n")
            
            capture_count = 0
            while True:
                if config.MAX_CAPTURES > 0 and capture_count >= config.MAX_CAPTURES:
                    print(f"\n✓ Maksimum çekim sayısına ulaşıldı: {config.MAX_CAPTURES}")
                    break
                
                print(f"\n--- Çekim #{capture_count + 1} ---")
                process_single_capture(camera, excel_writer)
                capture_count += 1
                
                if config.MAX_CAPTURES == 0 or capture_count < config.MAX_CAPTURES:
                    print(f"⏳ {config.CAPTURE_INTERVAL} saniye bekleniyor...")
                    time.sleep(config.CAPTURE_INTERVAL)
        else:
            # Tek çekim modu
            print("\n📸 Görüntü yakalanıyor...\n")
            process_single_capture(camera, excel_writer)
        
        print("\n✓ İşlem tamamlandı!")
        logging.info("İşlem başarıyla tamamlandı")
    
    except KeyboardInterrupt:
        print("\n\n⚠ Program kullanıcı tarafından durduruldu")
        logging.info("Program kullanıcı tarafından durduruldu")
    
    except Exception as e:
        print(f"\n✗ Hata: {e}")
        logging.error(f"Kritik hata: {e}", exc_info=True)
        sys.exit(1)
    
    finally:
        # Temizlik
        if camera:
            print("Kamera kapatılıyor...")
            camera.release()
        print("Program sonlandırıldı.")
        logging.info("Program sonlandırıldı")


if __name__ == "__main__":
    main()
