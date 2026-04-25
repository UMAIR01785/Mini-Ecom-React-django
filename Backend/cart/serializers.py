from rest_framework import serializers
from .models import Cart ,CartItem
from Product.models import Product

class CartitemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="product.id")
    name = serializers.CharField(source="product.name")
    slug = serializers.CharField(source="product.slug")
    stock = serializers.IntegerField(source="product.stock")
    price =serializers.DecimalField(source="product.price",max_digits=10,decimal_places=2)
    image= serializers.SerializerMethodField()
    sub_total = serializers.SerializerMethodField()
    
    
    class Meta:
        model = CartItem
        fields = ['id','product_id','name','slug','price','image','quantity','stock','sub_total']
        read_only_fields = ['product_id','name','slug','price','image','price','stock']
        
        
    def get_sub_total(self,obj):
        return obj.product.price * obj.quantity
    
    def get_image(self,obj):
        primary = obj.product.images.filter(
            is_primary=True
        ).first()

        if primary:
            return primary.image.url
        
        return None
    
    
class CartSerializer(serializers.ModelSerializer):
    items = CartitemSerializer(many=True,read_only=True)
    total_items = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id','items','total_items','total_quantity','total_price']
        
        
    def get_total_items(self,obj):
        return obj.items.count()
    
    def get_total_quantity(self,obj):
        return sum(item.quantity for item in obj.items.all())
    
    def get_total_price(self,obj):
        return sum(item.product.price * item .quantity for item in obj.items.all())
    
    
class AddtoCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(
        min_value=1,
        default=1
    )
    
    
    def validate_product_id(self,value):
        try:
            product = Product.objects.get(
                id=value,
                is_active=True
            )
        except Product.DoesNotExist:
            raise serializers.ValidationError(
                "product is not find"
            )
        return value
    
    def validate(self, attrs):
        product = Product.objects.get(
            id=attrs["product_id"]
        )

        qty = attrs["quantity"]

        if qty > product.stock:
            raise serializers.ValidationError(
                {
                    "quantity":
                    f"Only {product.stock} items available."
                }
            )

        return attrs
    
class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(
        min_value=1,
        required=False
    )
    action = serializers.ChoiceField(
        choices=["plus", "minus"],
        required=False
    )
    

class RemoveCartItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()