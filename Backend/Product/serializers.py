from rest_framework import serializers
from .models import Category,Product,ProductImage


class CategorySerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Category
        fields = ['id','name','slug','is_active','image','created_at','updated_at']
        
        read_only_fields = ['slug','created_at','updated_at']
        
class ProductImageSerailizer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductImage
        fields = ['id','image','alt_text','sort_img','is_primary','created_at','updated_at']
        
        read_only_fields = ['created_at','updated_at']
        
        
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
        