from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from uuid import uuid4
from Product.models import Product
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class GuestEmailVerification(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    
    session_key=models.CharField(max_length=255 ,blank=True)
    is_verified = models.BooleanField(default=False)
    expire_at =models.DateTimeField()
    created_at =models.DateTimeField(auto_now_add=True)
    
    
    def save(self,*args,**kwargs):
        if not self.expire_at:
            self.expire_at=timezone.now() + timedelta(minutes=10)
        super().save(*args,**kwargs)
        
    
    def __str__(self):
        return self.email
    
    
class Order(models.Model):
    STATUS_CHOICE =(
        ("pending","Pending"),
        ("confirmed","COnfirmed"),
        ("shipped","Shipped"),
        ("delivered","Delivered"),
        ("canceled","Cancled")
    )
    order_id = models.UUIDField(default=uuid4, editable=False,unique=True)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True ,blank=True ,related_name='order')
    
    full_name = models.CharField(max_length=255)
    
    email = models.EmailField()
    phone_number = PhoneNumberField()
    
    
    state = models.CharField(max_length=255) 
    city = models.CharField(max_length=255)
    address = models.TextField()
    
    shipped_fee = models.DecimalField(max_digits=12 ,decimal_places=2)
    total =models.DecimalField(max_digits=12 ,decimal_places=2)
    sub_total = models.DecimalField(max_digits=12 ,decimal_places=2)
    status = models.CharField(choices=STATUS_CHOICE ,default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        if self.user:
            return f"{self.user.username}-{self.order_id}"
        return f"{self.order_id}-{self.full_name}"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE ,related_name="items")
    product = models.ForeignKey(Product ,on_delete=models.CASCADE )
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12,decimal_places=2)
    sub_total = models.DecimalField(max_digits=12,decimal_places=2)
    quantity= models.PositiveIntegerField()
    
    
    def __str__(self):
        return self.product_name
        