from django.contrib import admin
from .models import GuestEmailVerification ,Order,OrderItem
# Register your models here.

admin.site.register(GuestEmailVerification)
admin.site.register(OrderItem)
admin.site.register(Order)
