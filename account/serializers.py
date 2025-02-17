from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
        
    class Meta:
        model= User
        fields = ['first_name','last_name','username','email','password','confirm_password']
    
    def save(self, **kwargs):
        username = self.validate['username']
        first_name = self.validate['first_name']
        last_name = self.validate['last_name']
        email = self.validate['email']
        password = self.validate['password']
        confirm_password = self.validate['confirm_password']
        
        if password != confirm_password:
            raise serializers.ValidationError({'error':"Password don't match."})
        
        if User.objects.filter(email=email).exist():
            raise serializers.ValidationError({'email':"Email already exist."})
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username':"Username already exist."})
        
        user = User(username=username,first_name=first_name,last_name=last_name,email=email)
        user.set_password('password')
        user.is_active = False
        user.save()
        
        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
        
    