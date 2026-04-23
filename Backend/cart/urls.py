from django.urls import path
from .views import AddToCartView,CartView,UpdatedCartView,RemoveCartView


urlpatterns = [
    path('',CartView.as_view()),
    path('add/',AddToCartView.as_view()),
    path('update/<int:id>/',UpdatedCartView.as_view()),
    path('reomve/<int:id>/',RemoveCartView.as_view()),
    
]
