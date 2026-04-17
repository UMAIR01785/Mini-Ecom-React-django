from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,Profile

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'first_name', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)
    
    
    readonly_fields = ('date_joined', 'updated_at')

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Profile)