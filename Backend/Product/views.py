from .models import Product,Category
from .serializers import ProductSerializer,ProductDetailSerailizer,CategorySerializer
from rest_framework.generics import ListAPIView,RetrieveAPIView

# Create your views here.

class CategoryView(ListAPIView):
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True).order_by("-created_at")
    
class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return Product.objects.select_related('category').filter(is_active=True).order_by("-is_feature","-created_at")
    
class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerailizer
    lookup_field = "slug"
    
    def get_queryset(self):
        return Product.objects.select_related('category').filter(is_active=True).order_by("-is_feature","-created_at")
    
class CategoryProductView(ListAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Product.objects.select_related('category').filter(
            category__slug=slug,
            is_active=True
        )