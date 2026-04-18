from django.contrib import admin
from .models import Category ,Product,ProductImage
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "slug"]

    readonly_fields = ["slug"]

class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "slug"]
    readonly_fields =["slug"]


admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage)
