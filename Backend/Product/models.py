from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
import uuid
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=255,db_index=True)
    slug=models.SlugField(unique=True,null=True)
    image=CloudinaryField('Category_image')
    is_active=models.BooleanField(default=True,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def save(self,*args,**kwargs):
        self.slug = f"{slugify(self.name)}-{uuid.uuid4().hex[:8]}"
        super().save(*args,**kwargs)
        
        
    def __str__(self):
        return self.name
    
    
        
class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE ,related_name='product')
    name = models.CharField(max_length=255,db_index=True)
    slug = models.SlugField(unique=True , null=True)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8,decimal_places=2,db_index=True)
    is_active =models.BooleanField(default=True,db_index=True)
    is_feature = models.BooleanField(default=False,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def save(self,*args,**kwargs):
        self.slug = f"{slugify(self.name)}-{uuid.uuid4().hex[:8]}"
        
        
        if self.stock == 0:
            self.is_active = False
        else:
            self.is_active = True
        super().save(*args,**kwargs)
    
    @property
    def in_stock(self):
        return self.stock > 0
    
    
    
    def __str__(self):
        return f"{self.name}-{self.category}"
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image = CloudinaryField('Primary_image')
    alt_text = models.CharField(max_length=255)
    sort_img = models.PositiveIntegerField(default=1)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_img','id']
        
        
        
    
        
    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
        
        self.alt_text = f"{self.product.name} image"

        if self.is_primary:
            ProductImage.objects.filter(
                product=self.product
            ).exclude(id=self.id).update(is_primary=False)
        
    def __str__(self):
        return f"{self.product.name}-Images"