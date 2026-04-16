from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Profile
from .serializer import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
# Create your views here.

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)    

