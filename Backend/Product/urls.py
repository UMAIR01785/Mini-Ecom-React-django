from django.urls import path
from .views import CategoryView,ProductListView,ProductDetailView,CategoryProductView


urlpatterns = [
    path('category/',CategoryView.as_view()),
    path('product/',ProductListView.as_view()),
    path('product/<slug:slug>/',ProductDetailView.as_view()),
    path('category/<slug:slug>/',CategoryProductView.as_view()),
]
