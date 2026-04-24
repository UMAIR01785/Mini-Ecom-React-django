from rest_framework import serializers
from .models import Order,OrderItem


class SendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    
class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source = "product.id" ,read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product_id',
            'product_name',
            'price',
            'quantity',
            'sub_total',
        ]   
        
        
        
        
        
        
        
class OrderSerializer(serializers.ModelSerializer):
    items =OrderItemSerializer(many=True ,read_only=True)
    
    class Meta:
        model = Order
        fields = ['id','order_id','full_name','email','phone_number','address','city','state','shipped_fee','total','sub_total','status','created_at','items']
        
class CheckoutSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=120)
    phone_number = serializers.CharField()
    address = serializers.CharField()
    city = serializers.CharField(max_length=50)
    state = serializers.CharField(max_length=50)