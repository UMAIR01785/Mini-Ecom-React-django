from django.db import models
from django.conf import settings
from Product.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE,null=True)
    session_key = models.CharField(max_length=255 , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        if self.user:
            return f"{self.user.username}-cart"
        return f"{self.session_key}-cart"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE )
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ['cart','product']
    
    
    def __str__(self):
        if self.cart.user:
            return f"{self.product.name}-{self.cart.user.username}"
        return f"{self.product.name}-guest"
