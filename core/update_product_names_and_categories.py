from django.core.management.base import BaseCommand
from django.utils.text import slugify

from shop.models import Product, Category


CATEGORY_NAMES = [
    "کالای دیجیتال",
    "خانه و آشپزخانه",
    "آرایشی و بهداشتی",
    "مد و پوشاک",
    "خودرو و موتورسیکلت",
    "کتاب و هنر",
    "لپ تاپ",
    "طلا و نقره",
    "سلامت و پزشکی",
    "ابزار آلات و تجهیزات",
]


CATEGORY_PRODUCT_NAMES = {
    "کالای دیجیتال": [
        "گوشی موبایل سامسونگ گلکسی A15",
        "گوشی موبایل شیائومی ردمی نوت ۱۳",
        "هدفون بلوتوث بی‌سیم",
        "اسپیکر بلوتوث قابل حمل",
        "فلش مموری ۶۴ گیگابایت USB 3.0",
        "پاوربانک ۲۰ هزار میلی‌آمپرساعت",
    ],
    "خانه و آشپزخانه": [
        "سرویس قابلمه ۶ پارچه گرانیتی",
        "زودپز استیل ۶ لیتری",
        "چرخ گوشت خانگی",
        "جاروبرقی کیسه‌ای ۲۴۰۰ وات",
        "کتری و قوری شیشه‌ای",
        "سرویس بشقاب و کاسه ۱۸ پارچه",
    ],
    "آرایشی و بهداشتی": [
        "کرم مرطوب‌کننده پوست خشک",
        "شامپو ضد شوره موهای چرب",
        "ماسک مو ترمیم کننده",
        "رژلب مات ماندگار",
        "خط چشم مایع ضد آب",
        "کرم ضد آفتاب SPF50 بی‌رنگ",
    ],
    "مد و پوشاک": [
        "تیشرت مردانه نخی یقه گرد",
        "شلوار جین مردانه جذب",
        "پیراهن مردانه چهارخانه",
        "کفش ورزشی زنانه دویدن",
        "مانتو زنانه تابستانی",
        "هودی کلاه‌دار فری سایز",
    ],
    "خودرو و موتورسیکلت": [
        "روغن موتور ۱۰W40 نیمه سینتتیک",
        "فیلتر هوا خودرو",
        "تیغه برف پاک‌کن سیلیکونی",
        "کلاه کاسکت فک‌دار",
        "کاور صندلی خودرو چرمی",
        "پمپ باد فندکی خودرو",
    ],
    "کتاب و هنر": [
        "رمان فارسی پرفروش",
        "کتاب آموزشی برنامه‌نویسی پایتون",
        "کتاب رنگ‌آمیزی کودک",
        "دفتر طراحی هنری A4",
        "ست آبرنگ ۲۴ رنگ",
        "بوم نقاشی ۵۰ در ۷۰",
    ],
    "لپ تاپ": [
        "لپ تاپ ۱۵ اینچ دانشجویی",
        "لپ تاپ گیمینگ ۱۶ اینچ",
        "لپ تاپ سبک وزن اداری",
        "لپ تاپ لمسی ۱۴ اینچ",
        "کیف لپ تاپ ضد ضربه",
        "پایه خنک‌کننده لپ تاپ",
    ],
    "طلا و نقره": [
        "انگشتر طلا زنانه ظریف",
        "گردنبند نقره سنگ‌دار",
        "دستبند طلا زنجیری",
        "گوشواره طلا میخی",
        "سرویس کامل طلا عروس",
        "آویز گردنبند نقره",
    ],
    "سلامت و پزشکی": [
        "فشارسنج دیجیتال بازویی",
        "تب‌سنج دیجیتال لیزری",
        "اکسی‌متر انگشتی",
        "کمربند طبی ارتوپدی",
        "ماسک تنفسی سه لایه",
        "مکمل ویتامین D 1000",
    ],
    "ابزار آلات و تجهیزات": [
        "دریل شارژی ۱۲ ولت",
        "پیچ‌گوشتی برقی چندکاره",
        "متر لیزری ۵۰ متری",
        "مجموعه آچار بکس ۴۰ پارچه",
        "انبر دست صنعتی",
        "جعبه ابزار پلاستیکی بزرگ",
    ],
}


class Command(BaseCommand):
    help = "Update existing products with realistic names and proper categories."

    def handle(self, *args, **options):
        # Prepare categories (get or create by exact name)
        categories_map = {}
        for name in CATEGORY_NAMES:
            slug = slugify(name, allow_unicode=True)
            category, _ = Category.objects.get_or_create(
                name=name,
                defaults={
                    "slug": slug,
                    "description": name,
                },
            )
            categories_map[name] = category

        products = list(Product.objects.all().order_by("id"))
        total_products = len(products)

        if not products:
            self.stdout.write(self.style.WARNING("هیچ محصولی برای بروزرسانی یافت نشد."))
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"در حال بروزرسانی {total_products} محصول با نام و دسته‌بندی واقعی..."
            )
        )

        # Track used names to avoid duplicates
        used_names = set(
            Product.objects.values_list("name", flat=True)
        )  # قبلاً استفاده شده در DB

        # Index per category for round-robin selection of names
        name_indices = {name: 0 for name in CATEGORY_NAMES}
        category_count = len(CATEGORY_NAMES)

        updated = 0
        for idx, product in enumerate(products):
            # Select category in round-robin fashion
            category_name = CATEGORY_NAMES[idx % category_count]
            category_obj = categories_map[category_name]

            # Pick a base name for this category
            base_names = CATEGORY_PRODUCT_NAMES.get(category_name, [])
            if not base_names:
                # Fallback: generic name if list is empty for some reason
                base_name = f"محصول {category_name}"
            else:
                current_index = name_indices[category_name] % len(base_names)
                base_name = base_names[current_index]
                name_indices[category_name] += 1

            new_name = self._make_unique_name(base_name, used_names)
            used_names.add(new_name)

            new_slug = self._generate_unique_slug(new_name, product)

            old_name = product.name
            old_slug = product.slug

            product.name = new_name
            product.slug = new_slug
            product.category.set([category_obj])
            product.save(update_fields=["name", "slug"])

            updated += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"- Product ID {product.id}: "
                    f"'{old_name}' → '{new_name}' | "
                    f"slug: '{old_slug}' → '{new_slug}' | "
                    f"category: '{category_name}'"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(f"\n✓ بروزرسانی {updated} محصول با موفقیت انجام شد.")
        )

    def _make_unique_name(self, base_name: str, used_names: set) -> str:
        """
        Ensure product name is unique within current dataset.
        """
        if base_name not in used_names:
            return base_name

        counter = 2
        while True:
            candidate = f"{base_name} {counter}"
            if candidate not in used_names:
                return candidate
            counter += 1

    def _generate_unique_slug(self, name: str, product: Product) -> str:
        """
        Generate a unique slug for the given product based on its name.
        """
        base_slug = slugify(name, allow_unicode=True) or "product"
        slug = base_slug
        counter = 2

        # Exclude current product so re-running command is idempotent per product
        while (
            Product.objects.filter(slug=slug)
            .exclude(pk=product.pk)
            .exists()
        ):
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

