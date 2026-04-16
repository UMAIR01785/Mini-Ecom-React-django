from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,Profile

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'first_name', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser')}),
        ('Important Dates', {'fields': ('date_joined', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    readonly_fields = ('date_joined', 'updated_at')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'phone_number', 'password1', 'password2'),
        }),
    )

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Profile)