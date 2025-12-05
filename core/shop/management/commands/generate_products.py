from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.conf import settings
from faker import Faker
from shop.models import Product, Category, ProductStatus, ProductImage
from django.contrib.auth import get_user_model
import os
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate sample products using Faker'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of products to generate (default: 10)'
        )

    def handle(self, *args, **options):
        faker = Faker('fa_IR')  # استفاده از locale فارسی
        count = options['count']
        
        # بررسی وجود کاربران
        users = list(User.objects.all())
        if not users:
            self.stdout.write(
                self.style.ERROR('❌ No user found! Create a user first.')
            )
            return
        
        # بررسی وجود دسته‌بندی
        categories = list(Category.objects.all())
        if not categories:
            self.stdout.write(
                self.style.ERROR('❌ No categories found! Run: python manage.py generate_categories')
            )
            return
        
        # دریافت لیست عکس‌های موجود
        img_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'product_img')
        available_images = []
        
        if os.path.exists(img_dir):
            available_images = [
                f for f in os.listdir(img_dir)
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))
            ]
            self.stdout.write(
                self.style.SUCCESS(f'✓ Found {len(available_images)} images in {img_dir}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠️  Image directory not found: {img_dir}')
            )
        
        created_count = 0
        for i in range(count):
            try:
                # تولید نام محصول
                product_name = faker.word().capitalize()
                
                # بررسی تکراری نبودن
                counter = 1
                original_name = product_name
                while Product.objects.filter(name=product_name).exists():
                    product_name = f"{original_name} {counter}"
                    counter += 1
                
                # تولید slug
                slug = slugify(product_name, allow_unicode=True)
                counter = 1
                original_slug = slug
                while Product.objects.filter(slug=slug).exists():
                    slug = f"{original_slug}-{counter}"
                    counter += 1
                
                # تولید توضیح
                description = faker.paragraph(nb_sentences=3)
                
                # تولید قیمت (10000 تا 1000000)
                price = faker.random_int(min=10000, max=1000000)
                
                # تولید قیمت تخفیف (20% کمتر از قیمت اصلی)
                discount_price = int(price * 0.8)
                
                # تولید موجودی (0 تا 100)
                stock = faker.random_int(min=0, max=100)
                
                # انتخاب وضعیت تصادفی
                status = random.choice([
                    ProductStatus.ACTIVE,
                    ProductStatus.INACTIVE,
                    ProductStatus.OUT_OF_STOCK
                ])
                
                # انتخاب کاربر تصادفی
                user = random.choice(users)
                
                # ایجاد محصول
                product = Product.objects.create(
                    user=user,
                    name=product_name,
                    description=description,
                    price=price,
                    discount_price=discount_price,
                    stock=stock,
                    slug=slug,
                    status=status
                )
                
                # اضافه کردن دسته‌بندی‌های تصادفی (1 تا 3 دسته)
                product_categories = random.sample(
                    categories,
                    k=random.randint(1, min(3, len(categories)))
                )
                product.category.set(product_categories)
                
                # اضافه کردن عکس‌های تصادفی (اگر موجود باشند)
                num_images = 0
                if available_images:
                    num_images = random.randint(1, min(3, len(available_images)))
                    selected_images = random.sample(available_images, num_images)
                    
                    for img_file in selected_images:
                        ProductImage.objects.create(
                            product=product,
                            image=f'product_img/{img_file}',
                            alt_text=f'{product_name} - Image'
                        )
                
                created_count += 1
                categories_str = ', '.join([cat.name for cat in product_categories])
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ {product_name} | Price: {price:,} | Images: {num_images} | Categories: {categories_str}'
                    )
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error creating product: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Successfully created {created_count} products!'
            )
        )
