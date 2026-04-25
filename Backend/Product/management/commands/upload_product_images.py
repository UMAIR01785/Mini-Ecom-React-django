import cloudinary.uploader
from django.core.management.base import BaseCommand
from django.db import transaction
from Product.models import Product, ProductImage


class Command(BaseCommand):
    help = "Upload images for all products that have placeholder images"

    def add_arguments(self, parser):
        parser.add_argument(
            "--product-id",
            type=int,
            help="Upload images for a specific product ID",
        )

    def _upload_image_with_retry(self, folder, public_id_seed, width, height, product_keyword):
        """Try uploading image from multiple reliable sources with retry logic"""
        
        # Image sources in order of preference (most reliable first)
        image_sources = [
            f"https://via.placeholder.com/{width}x{height}?text={product_keyword}",
            f"https://placeholder.co/{width}x{height}?text={product_keyword}",
            f"https://dummyimage.com/{width}x{height}/007bff/ffffff?text={product_keyword}",
        ]
        
        for remote_url in image_sources:
            try:
                uploaded = cloudinary.uploader.upload(
                    remote_url,
                    folder=folder,
                    public_id=public_id_seed,
                    overwrite=True,
                    unique_filename=False,
                    resource_type="image",
                )
                self.stdout.write(
                    self.style.SUCCESS(f"[UPLOADED] {public_id_seed}")
                )
                return uploaded["public_id"]
            except Exception as e:
                continue
        
        # If all sources fail, use placeholder
        self.stdout.write(
            self.style.WARNING(f"[PLACEHOLDER] {public_id_seed}")
        )
        return f"{folder}/{public_id_seed}"

    @transaction.atomic
    def handle(self, *args, **options):
        product_id = options.get("product_id")
        
        if product_id:
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                self.stdout.write(self.style.ERROR(f"Product {product_id} not found"))
                return
        else:
            products = Product.objects.all()
        
        total_updated = 0
        
        for product in products:
            self.stdout.write(f"\nProcessing: {product.name}")
            
            images = product.images.all()
            for idx, product_image in enumerate(images, 1):
                # Create a keyword based on product name
                product_safe_name = product.name.lower().replace(' ', '-').replace('&', 'and')
                new_public_id = f"ecom_products/{product_safe_name}-{idx}"
                
                # Only upload if it's a placeholder (doesn't start with "ecom_products/" but ends with a placeholder format)
                if "ecom_products" not in str(product_image.image):
                    continue
                
                # Try to upload the image
                new_image_id = self._upload_image_with_retry(
                    folder="ecom_products",
                    public_id_seed=f"{product_safe_name}-{idx}",
                    width=1000,
                    height=1000,
                    product_keyword=product.name,
                )
                
                # Update the image if upload was successful
                if new_image_id != f"ecom_products/{product_safe_name}-{idx}":
                    product_image.image = new_image_id
                    product_image.save()
                    total_updated += 1
                    self.stdout.write(f"  [+] Image {idx} updated")
        
        self.stdout.write(
            self.style.SUCCESS(f"\nCompleted! Updated {total_updated} images.")
        )
