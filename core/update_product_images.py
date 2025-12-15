#!/usr/bin/env python
"""
اسکریپت برای آپدیت عکس‌های محصولات
"""
import os
import django
from django.core.files import File
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from shop.models import Product

# مسیر پوشه عکس‌های اصلی
IMAGE_DIR = Path('/app/media/product_img')

# مسیر پوشه عکس‌های پشتیبان (static)
BACKUP_IMAGE_DIR = Path('/app/static/img')

# دریافت لیست عکس‌های اصلی
image_files = list(IMAGE_DIR.glob('*.jpg')) + list(IMAGE_DIR.glob('*.png')) + list(IMAGE_DIR.glob('*.jpeg'))
image_files = sorted([f for f in image_files if f.is_file()])

# دریافت لیست عکس‌های پشتیبان (تمام پوشه‌های زیرمجموعه)
backup_images = list(BACKUP_IMAGE_DIR.rglob('*.jpg')) + list(BACKUP_IMAGE_DIR.rglob('*.png')) + list(BACKUP_IMAGE_DIR.rglob('*.jpeg'))
backup_images = sorted([f for f in backup_images if f.is_file()])

print(f"تعداد عکس‌های اصلی یافت شده: {len(image_files)}")
print(f"تعداد عکس‌های پشتیبان یافت شده: {len(backup_images)}")

# آپدیت محصولات
products = Product.objects.all().order_by('-id')
print(f"\nتعداد محصولات: {len(products)}")

for i, product in enumerate(products):
    # انتخاب عکس
    if i < len(image_files):
        image_path = image_files[i]
        source = "اصلی"
    elif (i - len(image_files)) < len(backup_images):
        image_path = backup_images[i - len(image_files)]
        source = "پشتیبان"
    else:
        print(f"محصول {product.id} بدون عکس باقی ماند")
        continue
    
    print(f"\nآپدیت محصول {product.id} ({product.name}):")
    print(f"  عکس ({source}): {image_path.name}")
    
    try:
        with open(image_path, 'rb') as f:
            product.image.save(
                image_path.name,
                File(f),
                save=True
            )
        print(f"  ✓ موفق!")
    except Exception as e:
        print(f"  ✗ خطا: {e}")

print("\n✓ پروسه تکمیل شد!")

