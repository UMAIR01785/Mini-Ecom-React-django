from django.shortcuts import render
from django.db import transaction
import random
from django.utils import timezone
from django.core.mail import send_mail
from cart.views import get_cart
from rest_framework import status
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import GuestEmailVerification,Order,OrderItem
from rest_framework.response import Response
from decimal import Decimal
from .serializers import SendEmailVerificationSerializer,VerifyEmailSerializer,CheckoutSerializer,OrderSerializer
# Create your views here.
from cart.models import CartItem
def calculate_cart_total(request):
    cart = get_cart(request)
    items = CartItem.objects.select_related('product').filter(
        cart=cart
    )
    sub_total = Decimal("0.00")
    for item in items:
        sub_total += item.product.price * item.quantity
    
    shipped_fee =Decimal("250.00")
    total = sub_total + shipped_fee
    
    return total , sub_total,shipped_fee,items


class SendGuestEmailCodeView(APIView):
    
    def post(self,request):
        serializer = SendEmailVerificationSerializer(data =request.data)
        serializer.is_valid(raise_exception=True)
        email =serializer.validated_data['email']
        code = str(random.randint(100000, 999999))
        
        GuestEmailVerification.objects.create(
            email=email,
            code=code,
            session_key =request.session.session_key
        )
        
        send_mail(
            subject="Your Verification code ",
            message=f"the code is {code}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )
        
        return Response({
            "success":True,
            "message":"the code is send Check your email",
            "data":serializer.data,
            "error":None
        },status=status.HTTP_202_ACCEPTED)
        

class VerifyGuestCodeView(APIView):
    def post(self,request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email =serializer.validated_data['email']
        code =serializer.validated_data['code']
        
        obj = GuestEmailVerification.objects.filter(
            email=email,
            code=code,
            session_key=request.session.session_key,
            is_verified=False,
             expire_at__gt=timezone.now()
        ).last()
        if not obj:
            return Response({
                "success":False,
                "message":"The code is incorrect",
                "data":None,
                "error":True
            },status=status.HTTP_400_BAD_REQUEST)
        
        obj.is_verified=True
        obj.save()
        request.session['guest_email_verified']=True
        request.session['guest_email']=email
        return Response({
            "success":True,
            "message":"the code is send Check your email",
            "data":serializer.data,
            "error":None
        },status=status.HTTP_202_ACCEPTED) 
        
        
class CheckoutView(APIView):
    def post(self,request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        cart = get_cart(request)
        
        total , sub_total,shipped_fee,items = calculate_cart_total(request)
        
        if not items:
            return Response({
                "success":False,
                "message":"the item is not exists",
                "data":None,
                "error":"item is empty"
            },status=status.HTTP_400_BAD_REQUEST)
            
        if request.user.is_authenticated:
            email = request.user.email
            user = request.user
            
        else:
            verified = request.session.get('guest_email_verified')
            email = request.session.get('guest_email')
            
            user =None
            
            if not verified or not email:
                 return Response({
                     "success":False,
                     "message":"the email is not verified",
                     'data':None,
                     "error":'Email is not verified'
                     
                 },status=status.HTTP_400_BAD_REQUEST)
                 
        with transaction.atomic():
            order = Order.objects.create(
                user = user,
                email = email,
                full_name= data['full_name'],
                phone_number =data['phone_number'],
                address = data['address'],
                city = data['city'],
                state = data['state'],
                shipped_fee =shipped_fee,
                total = total,
                sub_total = sub_total,
            )
            
            for item in items:
                OrderItem.objects.create(
                    order = order,
                    product =item.product,
                    product_name=item.product.name,
                    price =item.product.price,
                    sub_total=item.product.price* item.quantity,
                    quantity=item.quantity
                )


                item.product.stock -= item.quantity
                item.product.save()
            
            print(request.session.items())
            print(request.user.is_authenticated)
            print(items)
            print(serializer.errors)
                        
                
            items.delete()
        
        return Response({
            "success":True,
            "message":"The Checkout session is approves",
            'data':serializer.data,
            "error":None,
        },status=status.HTTP_201_CREATED)
        
        

class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        orders = Order.objects.filter(
            user= request.user
        ).prefetch_related('items').order_by("-created_at")
        
        serializer= OrderSerializer(
            orders,many=True
        )
        
        return Response({
            "success":True,
            "mesage":'the order is get',
            'data':serializer.data,
            "error":None,
            
        },status=status.HTTP_202_ACCEPTED)
        
        
class OrderDetailView(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.prefetch_related(
                "items"
            ).get(
                order_id=order_id,
                user=request.user
            )
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderSerializer(order)
        return Response({
            "success":True,
            "mesage":'the order is get',
            'data':serializer.data,
            "error":None,
            
        },status=status.HTTP_202_ACCEPTED)
            
        
        

        
        
        
 

        