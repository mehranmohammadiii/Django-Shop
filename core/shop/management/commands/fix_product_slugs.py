from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Product, Category


class Command(BaseCommand):
    help = 'Fix empty slugs for products and categories'

    def handle(self, *args, **options):
        # Fix Product slugs
        products_with_empty_slug = Product.objects.filter(slug='')
        self.stdout.write(
            self.style.WARNING(f'Found {products_with_empty_slug.count()} products with empty slugs')
        )
        
        for product in products_with_empty_slug:
            base_slug = slugify(product.name, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=product.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            product.slug = slug
            product.save()
            self.stdout.write(
                self.style.SUCCESS(f'✓ Product "{product.name}" → slug: "{product.slug}"')
            )
        
        # Fix Category slugs
        categories_with_empty_slug = Category.objects.filter(slug='')
        self.stdout.write(
            self.style.WARNING(f'Found {categories_with_empty_slug.count()} categories with empty slugs')
        )
        
        for category in categories_with_empty_slug:
            base_slug = slugify(category.name, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=category.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            category.slug = slug
            category.save()
            self.stdout.write(
                self.style.SUCCESS(f'✓ Category "{category.name}" → slug: "{category.slug}"')
            )
        
        self.stdout.write(self.style.SUCCESS('✓ All slugs have been fixed successfully!'))
