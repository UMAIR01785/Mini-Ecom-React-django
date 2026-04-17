from . models import Profile,User
from rest_framework import serializers

class Userserializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','phone_number','date_joined']


class ProfileSerializer(serializers.ModelSerializer):
    user=Userserializer(read_only=True)
    image=serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['user','bio','image','address','city','state']

    def get_image(self,obj):
        if obj.image:
            return obj.image.url
        return None
    
    
class RegisterSerializer(serializers.ModelSerializer):
    
    password=serializers.CharField(write_only=True , style={'input_type':'password'})
    confirm_password=serializers.CharField(write_only=True , style={'input_type':'password'})
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','phone_number','password','confirm_password']
        
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                "success":False,
                "message":"Password is not match",
                "data":None,
            })
        return attrs
    
    def validate_email(self,obj):
        if User.objects.filter(email=obj).exists():
            raise serializers.ValidationError({
                "success":False,
                "message":"Email is already exists",
                "data":None,
            })
            
        return obj
    
    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError({
                 "success":False,
                "message":"Username is already exists",
                "data":None,
            })
        return value
    
    
    def create(self,validate_data):
        confirm_password=validate_data.pop('confirm_password')
        password = validate_data.pop('password')
        
        user = User.objects.create_user(
            password=password,
            **validate_data
        )
       
        return user
