#!/usr/bin/env python3
"""
Test scripti - Capture Numbers uygulaması için
Bu script, kamera olmadan OCR fonksiyonlarını test etmek için kullanılabilir.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Test için sahte bir görüntü oluştur
try:
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    
    def create_test_image():
        """Test için sayı içeren bir görüntü oluştur"""
        # Beyaz arka plan
        img = Image.new('RGB', (400, 100), color='white')
        draw = ImageDraw.Draw(img)
        
        # Büyük sayı yaz
        try:
            # Sistem fontu kullan
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        except:
            # Varsayılan font
            font = ImageFont.load_default()
        
        draw.text((50, 20), "12345", fill='black', font=font)
        
        # Kaydet
        output_dir = Path("test_images")
        output_dir.mkdir(exist_ok=True)
        
        filename = output_dir / "test_number.png"
        img.save(filename)
        
        print(f"✓ Test görüntüsü oluşturuldu: {filename}")
        return str(filename)
    
    def test_ocr_without_camera():
        """Kamera olmadan OCR testi"""
        print("\n" + "="*50)
        print("OCR TEST (Kamera Olmadan)")
        print("="*50 + "\n")
        
        # Test görüntüsü oluştur
        test_image_path = create_test_image()
        
        # OCR modüllerini test et
        try:
            import pytesseract
            from PIL import Image
            
            print("✓ pytesseract modülü yüklendi")
            
            # Görüntüyü yükle
            img = Image.open(test_image_path)
            print(f"✓ Test görüntüsü yüklendi: {test_image_path}")
            
            # OCR uygula
            text = pytesseract.image_to_string(img, config='--psm 6')
            print(f"✓ OCR sonucu: '{text.strip()}'")
            
            if '12345' in text:
                print("✓ OCR testi BAŞARILI - Sayı doğru tanındı!")
            else:
                print("⚠ OCR testi UYARI - Sayı tam olarak tanınmadı")
            
        except ImportError as e:
            print(f"✗ Gerekli modüller bulunamadı: {e}")
            print("  Lütfen 'pip install pytesseract Pillow' komutunu çalıştırın")
        except Exception as e:
            print(f"✗ OCR testi başarısız: {e}")
    
    def test_excel_writing():
        """Excel yazma testi"""
        print("\n" + "="*50)
        print("EXCEL YAZMA TESTİ")
        print("="*50 + "\n")
        
        try:
            import pandas as pd
            from openpyxl import Workbook
            
            print("✓ Excel modülleri yüklendi")
            
            # Test verisi
            data = {
                'Tarih': [datetime.now().strftime('%Y-%m-%d')],
                'Saat': [datetime.now().strftime('%H:%M:%S')],
                'Sayı': ['12345'],
                'Güven (%)': [95.5]
            }
            
            df = pd.DataFrame(data)
            
            # Test dosyası
            test_file = "test_output.xlsx"
            df.to_excel(test_file, sheet_name="Test", index=False, engine='openpyxl')
            
            print(f"✓ Test Excel dosyası oluşturuldu: {test_file}")
            
            # Dosyayı oku ve kontrol et
            df_read = pd.read_excel(test_file, sheet_name="Test")
            print(f"✓ Excel dosyası başarıyla okundu")
            print(f"  Satır sayısı: {len(df_read)}")
            print(f"  Sütunlar: {', '.join(df_read.columns)}")
            
            # Temizle
            os.remove(test_file)
            print(f"✓ Test dosyası temizlendi")
            
            print("✓ Excel testi BAŞARILI!")
            
        except ImportError as e:
            print(f"✗ Gerekli modüller bulunamadı: {e}")
            print("  Lütfen 'pip install pandas openpyxl' komutunu çalıştırın")
        except Exception as e:
            print(f"✗ Excel testi başarısız: {e}")
    
    def test_image_processing():
        """Görüntü işleme testi"""
        print("\n" + "="*50)
        print("GÖRÜNTÜ İŞLEME TESTİ")
        print("="*50 + "\n")
        
        try:
            import cv2
            import numpy as np
            
            print("✓ OpenCV modülü yüklendi")
            
            # Test görüntüsü oluştur
            test_img = np.ones((100, 400, 3), dtype=np.uint8) * 255
            
            # Gri tonlama
            gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
            print("✓ Gri tonlama testi başarılı")
            
            # Eşikleme
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            print("✓ Eşikleme testi başarılı")
            
            # Yeniden boyutlandırma
            resized = cv2.resize(gray, (800, 200))
            print("✓ Yeniden boyutlandırma testi başarılı")
            
            print("✓ Görüntü işleme testi BAŞARILI!")
            
        except ImportError as e:
            print(f"✗ OpenCV modülü bulunamadı: {e}")
            print("  Lütfen 'pip install opencv-python' komutunu çalıştırın")
        except Exception as e:
            print(f"✗ Görüntü işleme testi başarısız: {e}")
    
    def main():
        """Ana test fonksiyonu"""
        print("\n" + "="*60)
        print("RASPBERRY PI OCR TO EXCEL - TEST PROGRAMI")
        print("="*60)
        
        # Tüm testleri çalıştır
        test_image_processing()
        test_excel_writing()
        test_ocr_without_camera()
        
        print("\n" + "="*60)
        print("TEST TAMAMLANDI")
        print("="*60 + "\n")
        
        print("Not: Gerçek kullanım için capture_numbers.py scriptini çalıştırın")
        print("     python3 capture_numbers.py\n")
    
    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"✗ Temel modüller eksik: {e}")
    print("\nLütfen önce gerekli paketleri yükleyin:")
    print("  pip install numpy Pillow")
    print("\nVeya kurulum scriptini çalıştırın:")
    print("  sudo ./setup.sh")
    sys.exit(1)
