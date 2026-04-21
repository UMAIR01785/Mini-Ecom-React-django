from .models import Product,Category
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer,ProductDetailSerailizer,CategorySerializer
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .pagination import ProductPagination
# Create your views here.

class CategoryView(ListAPIView):
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True).order_by("-created_at")
    
class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    pagination_class = ProductPagination
    search_fields = ['name','description']
    ordering_fields = ['created_at','price']
    ordering = ["-is_feature","-created_at"]
    
    filterset_fields = {
        'category': ['exact'],
        'category__slug': ['exact'],
        'price': ['exact', 'gte', 'lte'],
        'stock': ['exact', 'gte', 'lte'],
        'is_feature': ['exact'],
        'is_active': ['exact'],
    }

    def get_queryset(self):
        return Product.objects.select_related('category').filter(is_active=True).order_by("-is_feature","-created_at")
    
class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerailizer
    lookup_field = "slug"
    
    def get_queryset(self):
        return Product.objects.select_related('category').filter(is_active=True).order_by("-is_feature","-created_at")
    
class CategoryProductView(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    search_fields = [
        'name',
        'description'
    ]

    ordering_fields = [
        'price',
        'created_at',
        'name'
    ]

    ordering = ['-created_at']

    filterset_fields = {
        'price': ['gte', 'lte'],
        'stock': ['gte', 'lte'],
        'is_feature': ['exact'],
    }
    
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Product.objects.select_related('category').filter(
            category__slug=slug,
            is_active=True
        )