import random
from decimal import Decimal

import cloudinary.uploader
from django.core.management.base import BaseCommand
from django.db import transaction

from Product.models import Category, Product, ProductImage


CATEGORY_NAMES = [
    "Electronics",
    "Fashion",
    "Home and Living",
    "Sports",
    "Beauty",
    "Books",
    "Toys",
    "Groceries",
    "Automotive",
    "Office Supplies",
]

PRODUCT_PREFIXES = [
    "Premium",
    "Classic",
    "Smart",
    "Eco",
    "Ultra",
    "Compact",
    "Deluxe",
    "Pro",
]

PRODUCT_ITEMS = [
    "Headphones",
    "Backpack",
    "Lamp",
    "Shoes",
    "Watch",
    "Chair",
    "Bottle",
    "Keyboard",
    "Notebook",
    "Speaker",
    "Jacket",
    "Camera",
]


class Command(BaseCommand):
    help = "Seed fake categories, products, and product images for local development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--categories",
            type=int,
            default=5,
            help="Number of categories to create (default: 5)",
        )
        parser.add_argument(
            "--products-per-category",
            type=int,
            default=8,
            help="Number of products per category (default: 8)",
        )
        parser.add_argument(
            "--images-per-product",
            type=int,
            default=3,
            help="Number of images per product (default: 3)",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing category/product/image data before seeding.",
        )
        parser.add_argument(
            "--skip-image-upload",
            action="store_true",
            help="Skip Cloudinary upload and use existing demo IDs (images may not render).",
        )

    def _upload_placeholder(self, folder, public_id_seed, width, height):
        remote_url = f"https://picsum.photos/seed/{public_id_seed}/{width}/{height}"
        uploaded = cloudinary.uploader.upload(
            remote_url,
            folder=folder,
            public_id=public_id_seed,
            overwrite=True,
            unique_filename=False,
            resource_type="image",
        )
        return uploaded["public_id"]

    @transaction.atomic
    def handle(self, *args, **options):
        categories_count = max(1, options["categories"])
        products_per_category = max(1, options["products_per_category"])
        images_per_product = max(1, options["images_per_product"])
        reset = options["reset"]
        skip_image_upload = options["skip_image_upload"]

        created_categories = 0
        created_products = 0
        created_images = 0

        if reset:
            ProductImage.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing Product data deleted."))

        for category_index in range(categories_count):
            category_name = f"{CATEGORY_NAMES[category_index % len(CATEGORY_NAMES)]} {category_index + 1}"

            category_image_id = f"ecom_demo/categories/category_{category_index + 1}"
            if not skip_image_upload:
                category_image_id = self._upload_placeholder(
                    folder="ecom_demo/categories",
                    public_id_seed=f"category_{category_index + 1}",
                    width=800,
                    height=800,
                )

            category = Category.objects.create(
                name=category_name,
                image=category_image_id,
                is_active=True,
            )
            created_categories += 1

            for product_index in range(products_per_category):
                product_name = (
                    f"{random.choice(PRODUCT_PREFIXES)} "
                    f"{random.choice(PRODUCT_ITEMS)} "
                    f"{category_index + 1}-{product_index + 1}"
                )
                price = Decimal(str(round(random.uniform(10, 500), 2)))

                product = Product.objects.create(
                    category=category,
                    name=product_name,
                    description=(
                        "Demo product generated for development and UI testing."
                    ),
                    stock=random.randint(0, 120),
                    price=price,
                    is_active=True,
                    is_feature=random.choice([True, False]),
                )
                created_products += 1

                for image_index in range(images_per_product):
                    product_image_id = (
                        "ecom_demo/products/"
                        f"product_{category_index + 1}_{product_index + 1}_{image_index + 1}"
                    )

                    if not skip_image_upload:
                        product_image_id = self._upload_placeholder(
                            folder="ecom_demo/products",
                            public_id_seed=(
                                f"product_{category_index + 1}_{product_index + 1}_{image_index + 1}"
                            ),
                            width=1000,
                            height=1000,
                        )

                    ProductImage.objects.create(
                        product=product,
                        image=product_image_id,
                        alt_text=f"{product.name} image {image_index + 1}",
                        sort_img=image_index + 1,
                        is_primary=image_index == 0,
                    )
                    created_images += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Fake data created successfully: "
                f"{created_categories} categories, "
                f"{created_products} products, "
                f"{created_images} images."
            )
        )
