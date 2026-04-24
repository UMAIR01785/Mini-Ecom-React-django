from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from cloudinary.models import CloudinaryField

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,username,first_name,last_name,phone_number,email,password=None):
        if not email:
            raise ValueError("Email is required! ")
        if not username:
            raise ValueError("Username is requried !")
        
        user=self.create(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,password,email,phone_number,first_name,last_name):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.email_verifed=True
        user.is_superuser=True
        user.save(using=self._db)
        
        return user
    
    def get_by_natural_key(self, email):
        return self.get(email=email)

class User(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    username=models.CharField(unique=True)
    email=models.EmailField(unique=True)
    phone_number=PhoneNumberField()
    first_name=models.CharField()
    last_name=models.CharField()
    
    
    is_active=models.BooleanField(default=False)
    email_verifed = models.BooleanField(default=False)
    objects = MyAccountManager()
    is_staff=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    
    date_joined=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name','phone_number']
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    
    
class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    bio=models.TextField()
    address=models.TextField()
    city=models.CharField(max_length=40)
    state=models.CharField(max_length=40)
    image=CloudinaryField('Profile_pic')
    
    def __str__(self):
        return f'{self.user.username}'
    
    