from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from Product.models import Product
from rest_framework.response import Response
from .serializers import RemoveCartItemSerializer,CartSerializer,AddtoCartSerializer,UpdateCartItemSerializer
from .models import Cart,CartItem
from rest_framework import status
# Create your views here.

def get_cart(request):
    
    if request.user.is_authenticated:

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        return cart
    
    session_key = request.session.session_key
    
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart, created = Cart.objects.get_or_create(
        session_key=session_key,
        user=None
    )

    return cart

class CartView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        cart = get_cart(request)
        serializer = CartSerializer(cart)
        
        return Response({
            "success":True,
            "message":"cart retrieved successfully",
            "data":serializer.data,
            "error":None
        },status=status.HTTP_200_OK)
        


class AddToCartView(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request):
        
        serializer = AddtoCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart =get_cart(request)
        product = get_object_or_404(Product,id=serializer.validated_data['product_id'])
        qty = serializer.validated_data["quantity"]
        item , create = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity":qty}
        )
        
        if not create:
            item.quantity = qty
            item.save()

        
        
        return Response({
            "success":True,
            "message":"Item added to cart",
            "data":serializer.data,
            "error":None
        },status=status.HTTP_201_CREATED)
            
            
class UpdatedCartView(APIView):
    
    def patch(self,request,id):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = serializer.validated_data.get("action")
        quantity = serializer.validated_data.get("quantity")
        cart = get_cart(request)
        item =  get_object_or_404(CartItem.objects.select_related('product'),id=id,cart=cart)
        
        
        if action == "plus":
            if item.quantity > item.product.quantity:
                return Response({
                    "success":False,
                    "message":"The stock is low",
                    "data":None,
                    "error":"Stock is limited",
                },status=status.HTTP_400_BAD_REQUEST)
            
            item.quantity += 1
            item.save()
            
        elif action == "minus":
            item.quantity -= 1
            
            if item.quantity < 1:
                item.delete()
                return Response({
                    "success":True,
                    "message":"the item is Deleted",
                    "data":None,
                    "error":None
                },status=status.HTTP_202_ACCEPTED)
                
            item.save()
            
        elif quantity is not None:
            if quantity > item.stock:
                return Response  ({
                 "success":False,
                    "message":"The stock is low",
                    "data":None,
                    "error":"Stock is limited",
                },status=status.HTTP_400_BAD_REQUEST)    
                
            item.quantity = quantity
            item.save()
        
        return Response({
            "success":True,
            "message":"updated Cart",
            "data":serializer.data,
            "error":None
        },status=status.HTTP_202_ACCEPTED)
        
        
class RemoveCartView(APIView):
    def delete(self,request,id):
        serializer = RemoveCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item_id = serializer.validated_data['item_id']
        
        cart=get_cart(request)
        cartitem = get_object_or_404(CartItem, id=item_id ,cart=cart)
        cartitem.delete()
        return Response({
            "success":True,
            "message":"The cart is remove",
            "data":None,
            "error":None
        },status=status.HTTP_202_ACCEPTED)
        
        
        
        
        
        