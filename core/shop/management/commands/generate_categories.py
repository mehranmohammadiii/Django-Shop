from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from shop.models import Category


class Command(BaseCommand):
    help = 'Generate sample categories using Faker'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of categories to generate (default: 10)'
        )

    def handle(self, *args, **options):
        faker = Faker()
        count = options['count']
        
        created_count = 0
        for _ in range(count):
            try:
                # تولید نام دسته‌بندی
                name = faker.word().capitalize()
                
                # بررسی تکراری نبودن
                if Category.objects.filter(name=name).exists():
                    continue
                
                # تولید slug
                slug = slugify(name, allow_unicode=True)
                
                # بررسی تکراری نبودن slug
                if Category.objects.filter(slug=slug).exists():
                    slug = f"{slug}-{faker.random_int(1000, 9999)}"
                
                # تولید توضیح
                description = faker.sentence(nb_words=10)
                
                # ایجاد دسته‌بندی
                Category.objects.create(
                    name=name,
                    slug=slug,
                    description=description
                )
                
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created category: {name}')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error creating category: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Successfully created {created_count} categories!'
            )
        )
