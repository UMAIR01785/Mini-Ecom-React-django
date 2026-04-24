from django.urls import path
from .views import SendGuestEmailCodeView,VerifyGuestCodeView,CheckoutView,OrderView,OrderDetailView


urlpatterns = [
    path('send_email/',SendGuestEmailCodeView.as_view()),
    path('verify_email/',VerifyGuestCodeView.as_view()),
    path('checkout/',CheckoutView.as_view()),
    path('orders/',OrderView.as_view()),
    path('detail/<uuid:order_id>/',OrderDetailView.as_view())
]
