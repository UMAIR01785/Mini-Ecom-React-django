from . models import Profile,User
from rest_framework import serializers



class ProfileSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    image=serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['user','bio','image','address','city','state']
        
  

    def get_image(self,obj):
        if obj.image:
            return obj.image.url
        return None
    
    
class RegisterSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','phone_number']