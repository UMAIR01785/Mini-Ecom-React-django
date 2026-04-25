import random
from decimal import Decimal
import cloudinary.uploader
from django.core.management.base import BaseCommand
from django.db import transaction
from Product.models import Category, Product, ProductImage


# Real product data with descriptions and images
REAL_PRODUCTS = {
    "Electronics": [
        {
            "name": "Wireless Bluetooth Headphones",
            "description": "Premium noise-cancelling wireless headphones with 30-hour battery life. Features active noise cancellation, comfortable ear cups, and crystal-clear sound quality.",
            "price": 149.99,
            "stock": 45,
            "is_feature": True,
            "images": ["headphones", "headphones", "headphones"]
        },
        {
            "name": "Smart Watch Pro",
            "description": "Advanced smartwatch with heart rate monitor, GPS tracking, and 7-day battery life. Compatible with iOS and Android. Water-resistant up to 50m.",
            "price": 299.99,
            "stock": 32,
            "is_feature": True,
            "images": ["smartwatch", "smartwatch", "smartwatch"]
        },
        {
            "name": "USB-C Fast Charger",
            "description": "65W super fast charger supporting multiple devices. Features dual USB-C ports and smart charging technology.",
            "price": 39.99,
            "stock": 120,
            "is_feature": False,
            "images": ["charger", "charger", "charger"]
        },
        {
            "name": "4K Webcam",
            "description": "Crystal clear 4K webcam with auto-focus and built-in microphone. Perfect for streaming and video calls.",
            "price": 89.99,
            "stock": 28,
            "is_feature": False,
            "images": ["webcam", "webcam", "webcam"]
        },
        {
            "name": "Mechanical Keyboard RGB",
            "description": "Professional mechanical gaming keyboard with customizable RGB lighting. Features tactile switches and programmable keys.",
            "price": 129.99,
            "stock": 55,
            "is_feature": True,
            "images": ["keyboard", "keyboard", "keyboard"]
        },
        {
            "name": "Portable SSD 1TB",
            "description": "Ultra-fast 1TB portable SSD with 1050MB/s read speed. Compact design perfect for travelers and professionals.",
            "price": 159.99,
            "stock": 40,
            "is_feature": False,
            "images": ["ssd", "ssd", "ssd"]
        },
        {
            "name": "Wireless Mouse",
            "description": "Ergonomic wireless mouse with precision tracking and 18-month battery life. Compatible with all devices.",
            "price": 34.99,
            "stock": 85,
            "is_feature": False,
            "images": ["mouse", "mouse", "mouse"]
        },
        {
            "name": "Bluetooth Speaker",
            "description": "Waterproof portable Bluetooth speaker with 360-degree sound and 12-hour battery life.",
            "price": 79.99,
            "stock": 62,
            "is_feature": True,
            "images": ["speaker", "speaker", "speaker"]
        },
    ],
    "Fashion": [
        {
            "name": "Premium Jacket 4-5",
            "description": "High-quality durable jacket perfect for all seasons. Made from premium breathable fabric with multiple pockets and adjustable fit.",
            "price": 145.74,
            "stock": 38,
            "is_feature": True,
            "images": ["jacket", "jacket", "jacket"]
        },
        {
            "name": "Classic White T-Shirt",
            "description": "Essential white cotton t-shirt perfect for any wardrobe. 100% organic cotton, comfortable and durable.",
            "price": 24.99,
            "stock": 150,
            "is_feature": False,
            "images": ["tshirt", "tshirt", "tshirt"]
        },
        {
            "name": "Slim Fit Jeans",
            "description": "Stylish slim-fit jeans with stretchy fabric for comfort. Available in classic blue denim.",
            "price": 64.99,
            "stock": 95,
            "is_feature": False,
            "images": ["jeans", "jeans", "jeans"]
        },
        {
            "name": "Leather Sneakers",
            "description": "Comfortable casual leather sneakers with cushioned sole. Perfect for daily wear and light sports activities.",
            "price": 99.99,
            "stock": 72,
            "is_feature": True,
            "images": ["sneakers", "sneakers", "sneakers"]
        },
        {
            "name": "Winter Beanie",
            "description": "Warm knitted beanie made from soft acrylic fiber. Keeps you warm during cold weather.",
            "price": 19.99,
            "stock": 110,
            "is_feature": False,
            "images": ["beanie", "beanie", "beanie"]
        },
        {
            "name": "Denim Shorts",
            "description": "Casual denim shorts perfect for summer. Classic style with comfortable fit.",
            "price": 44.99,
            "stock": 68,
            "is_feature": False,
            "images": ["shorts", "shorts", "shorts"]
        },
        {
            "name": "Leather Belt",
            "description": "Genuine leather belt with stainless steel buckle. Timeless style for any outfit.",
            "price": 39.99,
            "stock": 85,
            "is_feature": False,
            "images": ["belt", "belt", "belt"]
        },
        {
            "name": "Sports Running Shoes",
            "description": "High-performance running shoes with cushioned insole and breathable mesh. Ideal for jogging and gym workouts.",
            "price": 119.99,
            "stock": 58,
            "is_feature": True,
            "images": ["running-shoes", "running-shoes", "running-shoes"]
        },
    ],
    "Home & Garden": [
        {
            "name": "LED Desk Lamp",
            "description": "Modern LED desk lamp with adjustable brightness and color temperature. Energy-efficient and eye-friendly.",
            "price": 54.99,
            "stock": 76,
            "is_feature": False,
            "images": ["lamp", "lamp", "lamp"]
        },
        {
            "name": "Decorative Plant Pot",
            "description": "Beautiful ceramic plant pot with drainage hole. Perfect for indoor and outdoor plants.",
            "price": 29.99,
            "stock": 92,
            "is_feature": False,
            "images": ["plant-pot", "plant-pot", "plant-pot"]
        },
        {
            "name": "Stainless Steel Water Bottle",
            "description": "Insulated stainless steel water bottle keeps drinks hot or cold for 24 hours. Leak-proof design.",
            "price": 34.99,
            "stock": 138,
            "is_feature": False,
            "images": ["water-bottle", "water-bottle", "water-bottle"]
        },
        {
            "name": "Ergonomic Office Chair",
            "description": "Comfortable ergonomic office chair with lumbar support and adjustable height. Perfect for long work hours.",
            "price": 249.99,
            "stock": 22,
            "is_feature": True,
            "images": ["office-chair", "office-chair", "office-chair"]
        },
        {
            "name": "Coffee Maker",
            "description": "Automatic coffee maker with programmable timer and thermal carafe. Brew perfect coffee every time.",
            "price": 89.99,
            "stock": 44,
            "is_feature": False,
            "images": ["coffee-maker", "coffee-maker", "coffee-maker"]
        },
        {
            "name": "Bed Sheet Set",
            "description": "Luxury Egyptian cotton bed sheet set with deep pockets. Ultra-soft and breathable.",
            "price": 79.99,
            "stock": 65,
            "is_feature": False,
            "images": ["bedsheet", "bedsheet", "bedsheet"]
        },
        {
            "name": "Kitchen Knife Set",
            "description": "Professional 5-piece stainless steel kitchen knife set. Sharp blades and ergonomic handles.",
            "price": 99.99,
            "stock": 35,
            "is_feature": True,
            "images": ["kitchen-knife", "kitchen-knife", "kitchen-knife"]
        },
        {
            "name": "Air Purifier",
            "description": "HEPA air purifier removes 99.97% of air pollutants. Quiet operation with smart controls.",
            "price": 169.99,
            "stock": 28,
            "is_feature": True,
            "images": ["air-purifier", "air-purifier", "air-purifier"]
        },
    ],
    "Sports & Fitness": [
        {
            "name": "Yoga Mat",
            "description": "Premium non-slip yoga mat made from eco-friendly material. Provides excellent cushioning and support.",
            "price": 44.99,
            "stock": 82,
            "is_feature": False,
            "images": ["yoga-mat", "yoga-mat", "yoga-mat"]
        },
        {
            "name": "Dumbbell Set",
            "description": "Adjustable dumbbell set ranging from 5-25 lbs. Space-saving design for home gym.",
            "price": 179.99,
            "stock": 19,
            "is_feature": True,
            "images": ["dumbbell", "dumbbell", "dumbbell"]
        },
        {
            "name": "Resistance Bands",
            "description": "Set of 5 colored resistance bands for strength training and physical therapy.",
            "price": 24.99,
            "stock": 115,
            "is_feature": False,
            "images": ["resistance-band", "resistance-band", "resistance-band"]
        },
        {
            "name": "Fitness Tracker",
            "description": "Advanced fitness tracker monitors steps, heart rate, sleep quality, and calories burned.",
            "price": 119.99,
            "stock": 48,
            "is_feature": True,
            "images": ["fitness-tracker", "fitness-tracker", "fitness-tracker"]
        },
        {
            "name": "Gym Backpack",
            "description": "Spacious gym backpack with separate shoe compartment and water bottle holders.",
            "price": 59.99,
            "stock": 71,
            "is_feature": False,
            "images": ["backpack", "backpack", "backpack"]
        },
        {
            "name": "Basketball",
            "description": "Official size basketball made from durable synthetic leather. Indoor and outdoor use.",
            "price": 34.99,
            "stock": 45,
            "is_feature": False,
            "images": ["basketball", "basketball", "basketball"]
        },
        {
            "name": "Gym Gloves",
            "description": "Professional weightlifting gloves with wrist support and superior grip.",
            "price": 29.99,
            "stock": 88,
            "is_feature": False,
            "images": ["gym-gloves", "gym-gloves", "gym-gloves"]
        },
        {
            "name": "Treadmill",
            "description": "Compact electric treadmill with LCD display and multiple speed settings. Perfect for home workouts.",
            "price": 399.99,
            "stock": 12,
            "is_feature": True,
            "images": ["treadmill", "treadmill", "treadmill"]
        },
    ],
    "Books & Learning": [
        {
            "name": "Python Programming Guide",
            "description": "Comprehensive Python programming book for beginners to advanced users. Learn core concepts and practical applications.",
            "price": 49.99,
            "stock": 56,
            "is_feature": False,
            "images": ["python-book", "python-book", "python-book"]
        },
        {
            "name": "Web Development Essentials",
            "description": "Master HTML, CSS, and JavaScript with practical projects. Includes real-world examples and best practices.",
            "price": 54.99,
            "stock": 43,
            "is_feature": True,
            "images": ["web-book", "web-book", "web-book"]
        },
        {
            "name": "Digital Marketing Strategy",
            "description": "Complete guide to modern digital marketing. Learn SEO, social media, email marketing, and analytics.",
            "price": 44.99,
            "stock": 67,
            "is_feature": False,
            "images": ["marketing-book", "marketing-book", "marketing-book"]
        },
        {
            "name": "Business Administration Handbook",
            "description": "Essential guide for business managers covering leadership, finance, and operations management.",
            "price": 59.99,
            "stock": 38,
            "is_feature": True,
            "images": ["business-book", "business-book", "business-book"]
        },
        {
            "name": "Data Science Fundamentals",
            "description": "Learn machine learning, data analysis, and visualization with practical Python examples.",
            "price": 64.99,
            "stock": 31,
            "is_feature": True,
            "images": ["data-science-book", "data-science-book", "data-science-book"]
        },
        {
            "name": "Personal Development Journal",
            "description": "Interactive journal for goal setting, habit tracking, and personal growth.",
            "price": 19.99,
            "stock": 102,
            "is_feature": False,
            "images": ["journal", "journal", "journal"]
        },
        {
            "name": "Design Thinking Workbook",
            "description": "Practical workbook on design thinking methodology with real-world case studies.",
            "price": 34.99,
            "stock": 52,
            "is_feature": False,
            "images": ["design-book", "design-book", "design-book"]
        },
        {
            "name": "AI & Machine Learning Mastery",
            "description": "Advanced guide to artificial intelligence, deep learning, and neural networks.",
            "price": 79.99,
            "stock": 24,
            "is_feature": True,
            "images": ["ai-book", "ai-book", "ai-book"]
        },
    ]
}


class Command(BaseCommand):
    help = "Seed real product categories and products for e-commerce website."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing category/product/image data before seeding.",
        )
        parser.add_argument(
            "--skip-image-upload",
            action="store_true",
            help="Skip Cloudinary upload and use demo image IDs.",
        )

    def _upload_image_with_retry(self, folder, public_id_seed, width, height, product_keyword):
        """Upload image from reliable sources that match the product keyword"""
        
        # Multiple fallback sources for each product keyword
        keyword_specific_images = {
            "headphones": [
                "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2016/11/19/14/51/headphones-1838768_1280.jpg",
            ],
            "smartwatch": [
                "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2017/11/08/14/51/wrist-2930951_1280.jpg",
            ],
            "charger": [
                "https://cdn.pixabay.com/photo/2017/10/31/09/22/electronics-2904849_1280.jpg",
                "https://cdn.pixabay.com/photo/2015/12/10/10/06/charger-1085560_1280.jpg",
            ],
            "webcam": [
                "https://cdn.pixabay.com/photo/2017/07/18/15/38/webcam-2515721_1280.jpg",
                "https://cdn.pixabay.com/photo/2017/09/01/21/54/web-2704589_1280.jpg",
            ],
            "keyboard": [
                "https://images.unsplash.com/photo-1587829191301-dc798b83add3?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2017/10/23/13/59/keyboard-2879768_1280.jpg",
            ],
            "ssd": [
                "https://cdn.pixabay.com/photo/2018/01/09/03/50/data-storage-3069644_1280.jpg",
                "https://cdn.pixabay.com/photo/2016/03/27/07/12/hard-drive-1280680_1280.jpg",
            ],
            "mouse": [
                "https://images.unsplash.com/photo-1527814050087-3793815479db?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2018/01/04/12/47/computer-mouse-3058399_1280.jpg",
            ],
            "speaker": [
                "https://images.unsplash.com/photo-1589003077984-894fbb60b1f7?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2018/10/15/10/43/speaker-3749965_1280.jpg",
            ],
            "jacket": [
                "https://images.unsplash.com/photo-1551028719-00167b16ebc5?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2017/02/04/08/58/jackets-2037952_1280.jpg",
            ],
            "tshirt": [
                "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2016/09/23/19/59/tshirt-1689920_1280.jpg",
            ],
            "jeans": [
                "https://images.unsplash.com/photo-1542272604-787c62d465d1?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2017/01/05/09/57/jeans-1953562_1280.jpg",
            ],
            "sneakers": [
                "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2016/12/13/05/03/shoes-1903081_1280.jpg",
            ],
            "beanie": [
                "https://images.unsplash.com/photo-1589902388646-f9e2bc92ccca?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2015/11/08/00/37/woolly-hat-1033391_1280.jpg",
            ],
            "shorts": [
                "https://cdn.pixabay.com/photo/2017/07/26/14/49/fashion-2539935_1280.jpg",
                "https://cdn.pixabay.com/photo/2019/06/26/19/05/shorts-4299968_1280.jpg",
            ],
            "belt": [
                "https://cdn.pixabay.com/photo/2017/11/24/14/41/leather-2974601_1280.jpg",
                "https://cdn.pixabay.com/photo/2015/01/11/10/28/accessory-594178_1280.jpg",
            ],
            "running-shoes": [
                "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2016/12/13/05/03/shoes-1903081_1280.jpg",
            ],
            "lamp": [
                "https://images.unsplash.com/photo-1565636192335-14c52cb09f5b?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2016/12/04/23/15/light-1883424_1280.jpg",
            ],
            "plant-pot": [
                "https://images.unsplash.com/photo-1578500494198-246f612d03b3?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2015/10/29/14/38/flowerpot-1010908_1280.jpg",
            ],
            "water-bottle": [
                "https://images.unsplash.com/photo-1559056199-641a0ac8b3f4?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2019/09/18/13/17/bottles-4484649_1280.jpg",
            ],
            "office-chair": [
                "https://images.unsplash.com/photo-1592078615290-033ee584e267?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2016/11/23/15/48/armchair-1853333_1280.jpg",
            ],
            "coffee-maker": [
                "https://images.unsplash.com/photo-1517668808822-9ebb02ae2a0e?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2018/04/24/09/29/coffee-maker-3346183_1280.jpg",
            ],
            "bedsheet": [
                "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2016/01/01/19/06/bedroom-1116287_1280.jpg",
            ],
            "kitchen-knife": [
                "https://images.unsplash.com/photo-1593618998160-e34014e67546?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2015/03/26/09/44/kitchen-690122_1280.jpg",
            ],
            "air-purifier": [
                "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2014/12/13/17/48/air-576441_1280.jpg",
            ],
            "yoga-mat": [
                "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2017/09/26/06/14/yoga-mat-2785783_1280.jpg",
            ],
            "dumbbell": [
                "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2015/01/09/11/07/dumbbell-593899_1280.jpg",
            ],
            "resistance-band": [
                "https://cdn.pixabay.com/photo/2018/04/09/15/31/gym-3304603_1280.jpg",
                "https://cdn.pixabay.com/photo/2017/09/04/21/41/fitness-2716524_1280.jpg",
            ],
            "fitness-tracker": [
                "https://images.unsplash.com/photo-1575311373937-040b3e6be5b0?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2018/01/31/14/03/smartwatch-3120383_1280.jpg",
            ],
            "backpack": [
                "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2019/10/04/14/58/backpack-4524315_1280.jpg",
            ],
            "basketball": [
                "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=1000&h=1000&fit=crop",
                "https://cdn.pixabay.com/photo/2017/01/06/17/51/sport-1958959_1280.jpg",
            ],
            "gym-gloves": [
                "https://cdn.pixabay.com/photo/2017/08/01/20/25/fitness-2569101_1280.jpg",
                "https://cdn.pixabay.com/photo/2020/12/13/18/18/gloves-5828546_1280.jpg",
            ],
            "treadmill": [
                "https://cdn.pixabay.com/photo/2015/06/24/15/45/exercise-819022_1280.jpg",
                "https://cdn.pixabay.com/photo/2017/09/04/21/41/fitness-2716524_1280.jpg",
            ],
            "python-book": [
                "https://cdn.pixabay.com/photo/2015/03/04/15/41/python-660894_1280.jpg",
                "https://cdn.pixabay.com/photo/2019/02/09/10/51/education-3983943_1280.jpg",
            ],
            "web-book": [
                "https://cdn.pixabay.com/photo/2018/03/10/12/00/computer-3213925_1280.jpg",
                "https://cdn.pixabay.com/photo/2019/02/09/10/51/education-3983943_1280.jpg",
            ],
            "marketing-book": [
                "https://cdn.pixabay.com/photo/2015/07/17/22/43/student-849825_1280.jpg",
                "https://cdn.pixabay.com/photo/2019/02/09/10/51/education-3983943_1280.jpg",
            ],
            "business-book": [
                "https://cdn.pixabay.com/photo/2019/02/09/10/51/education-3983943_1280.jpg",
                "https://cdn.pixabay.com/photo/2015/07/17/22/43/student-849825_1280.jpg",
            ],
            "data-science-book": [
                "https://cdn.pixabay.com/photo/2019/02/09/10/51/education-3983943_1280.jpg",
                "https://cdn.pixabay.com/photo/2018/03/10/12/00/computer-3213925_1280.jpg",
            ],
            "journal": [
                "https://cdn.pixabay.com/photo/2018/01/10/16/52/planner-3073813_1280.jpg",
                "https://cdn.pixabay.com/photo/2015/03/26/09/39/notebook-690102_1280.jpg",
            ],
            "design-book": [
                "https://cdn.pixabay.com/photo/2019/02/09/10/51/education-3983943_1280.jpg",
                "https://cdn.pixabay.com/photo/2015/07/17/22/43/student-849825_1280.jpg",
            ],
            "ai-book": [
                "https://cdn.pixabay.com/photo/2018/03/10/12/00/computer-3213925_1280.jpg",
                "https://cdn.pixabay.com/photo/2019/02/09/10/51/education-3983943_1280.jpg",
            ],
        }
        
        # Extract keyword from product_keyword and check if we have specific images
        keyword_lower = product_keyword.lower()
        for key, urls in keyword_specific_images.items():
            if key in keyword_lower:
                for url in urls:
                    try:
                        uploaded = cloudinary.uploader.upload(
                            url,
                            folder=folder,
                            public_id=public_id_seed,
                            overwrite=True,
                            unique_filename=False,
                            resource_type="image",
                            timeout=10,  # 10 second timeout
                        )
                        self.stdout.write(
                            self.style.SUCCESS(f"[OK] {public_id_seed} ({product_keyword})")
                        )
                        return uploaded["public_id"]
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f"[SKIP] {public_id_seed}: {str(e)[:50]}")
                        )
                        continue
                # If we tried all URLs for this keyword, stop trying
                break
        
        # If specific images not found or all failed, use unique placeholder URL per product
        placeholder_url = f"https://via.placeholder.com/{width}x{height}/cccccc/ffffff?text={product_keyword.replace('-', '+')}"
        self.stdout.write(
            self.style.WARNING(f"[PLACEHOLDER] {public_id_seed}")
        )
        return placeholder_url

    @transaction.atomic
    def handle(self, *args, **options):
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

        for category_name, products_list in REAL_PRODUCTS.items():
            # Create category
            category_safe_name = category_name.lower().replace(' & ', '-').replace(' ', '-')
            category_image_id = f"ecom_categories/{category_safe_name}"
            
            if not skip_image_upload:
                category_image_id = self._upload_image_with_retry(
                    folder="ecom_categories",
                    public_id_seed=category_safe_name,
                    width=800,
                    height=800,
                    product_keyword=category_name,
                )

            category = Category.objects.create(
                name=category_name,
                image=category_image_id,
                is_active=True,
            )
            created_categories += 1
            self.stdout.write(f"[+] Created category: {category_name}")

            # Create products
            for product_data in products_list:
                product = Product.objects.create(
                    category=category,
                    name=product_data["name"],
                    description=product_data["description"],
                    stock=product_data["stock"],
                    price=Decimal(str(product_data["price"])),
                    is_active=True,
                    is_feature=product_data["is_feature"],
                )
                created_products += 1

                # Create product images
                for idx, image_keyword in enumerate(product_data["images"]):
                    product_safe_name = product_data['name'].lower().replace(' ', '-')
                    product_image_id = f"ecom_products/{product_safe_name}-{idx + 1}"
                    
                    if not skip_image_upload:
                        product_image_id = self._upload_image_with_retry(
                            folder="ecom_products",
                            public_id_seed=f"{product_safe_name}-{idx + 1}",
                            width=1000,
                            height=1000,
                            product_keyword=image_keyword,
                        )

                    ProductImage.objects.create(
                        product=product,
                        image=product_image_id,
                        alt_text=f"{product.name} - Image {idx + 1}",
                        sort_img=idx + 1,
                        is_primary=idx == 0,
                    )
                    created_images += 1

                self.stdout.write(f"    [+] {product_data['name']}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\n[SUCCESS] Created:\n"
                f"  * {created_categories} categories\n"
                f"  * {created_products} products\n"
                f"  * {created_images} images"
            )
        )
