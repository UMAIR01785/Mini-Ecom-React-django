from rest_framework import serializers
from .models import Category,Product,ProductImage


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id','name','slug','is_active','image','created_at','updated_at']
        
        read_only_fields = ['slug','created_at','updated_at']
    
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None
        
class ProductImageSerailizer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id','image','alt_text','sort_img','is_primary','created_at','updated_at']
        
        read_only_fields = ['created_at','updated_at']
    
    def get_image(self, obj):
        if obj.image:
            # Check if the image value is already a full URL (external URL)
            image_str = str(obj.image)
            if image_str.startswith('http://') or image_str.startswith('https://'):
                return image_str
            # Otherwise, it's a Cloudinary ID - get the full URL
            return obj.image.url
        return None
        
        
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    primary_image=serializers.SerializerMethodField()
    
    
    class Meta:
        model = Product
        fields = ['id','name','slug','price','description','stock','is_active','is_feature','category','primary_image','created_at','updated_at']
        
        read_only_fields = ['slug','is_active','created_at','updated_at']
        
        
    def get_primary_image(self,obj):
        image = obj.images.filter(is_primary=True).first()
        return image.image.url if image else None
    
    
class ProductDetailSerailizer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    images = ProductImageSerailizer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'price',
            'description',
            'stock',
            'is_active',
            'category',
            'images',
            'created_at',
            'updated_at'
        ]
        