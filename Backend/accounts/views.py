from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from .tokens import activate_account
from rest_framework import status
from .models import Profile
from .serializer import ProfileSerializer,RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from .email import Activate_email
# Create your views here.


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)    
    
    
class RegisterView(APIView):
    
    def post(self,request):
        serializer= RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            Activate_email(user)
            return Response({
                "success":True,
                'message':"the register is done",
                "data":serializer.data,
                "error":None
            },status=status.HTTP_201_CREATED)
            
        return Response({
                "success":False,
                'message':"the register is Fail",
                "data":None,
                "error":serializer.errors,
            },status=status.HTTP_400_BAD_REQUEST)
        
    
    
class ActivateLinkView(APIView):
    def get(self,reuqest,user_id,token):
        try:
            user=User.objects.get(id=user_id)
        except:
            return Response({
                "success":False,
                "message":"user is invlaid",
                "data":None,
                
            },status=status.HTTP_400_BAD_REQUEST)
            
        if activate_account.check_token(user,token):
            user.is_active=True
            user.email_verifed=True
            user.save()
            return Response({
                "success":True,
                "message":"The user is active",
                "data":None
            },status=status.HTTP_202_ACCEPTED)
            
            
class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            
            if not refresh_token:
                return Response({
                    "success": False,
                    "message": "Refresh token is required",
                    "error": "No refresh token provided"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "success": True,
                "message": "Logout successful",
                "error": None
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Logout failed",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

