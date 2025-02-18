from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer,UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToke,AccessToken
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.response import Response
from rest_framework import status
# Mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model,authenticate,login,logout

User = get_user_model()

# Create your views here.
class UserRegisterAPIView(APIView):
    serializer_class = UserRegisterSerializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            access = AccessToken.for_user(user=user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f'/acount/activate/{uid}/{access}'
            email_subject = 'Confirmation Email'
            email_body = render_to_string('Confirmation_mail.html',{'confirm_link':confirm_link})
            email = EmailMultiAlternatives(email_subject,'',to=[user.email])
            email.attach_alternative(email_body,'text/html')
            email.send()
            
            response = self.serializer_class(user)
            
            return Response({
                "success":True,
                "statusCode": status.HTTP_201_CREATED,
                "message":"Registation successful. Check your mail for confirmation.",
                "data": response.data,
            },status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success":False,
                "statusCode":status.HTTP_400_BAD_REQUEST,
                "message":"Registation failed. Please check the provided data.",
                "error": serializer.errors,
            },status=status.HTTP_400_BAD_REQUEST)

def activate(self,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        # user = User.__default_manager.get(pk=uid)
        user = User.objects.get(pk=uid)
    except(User.DoesNotExist):
        user = None
        return redirect("http://127.0.0.1:8000/account/register/")
    
    try:
        if user is not None and not user.is_active:
            user.is_active = True
            user.save()
            return redirect('http://127.0.0.1:8000/account/login/')
        else:
            return redirect('http://127.0.0.1:8000/account/login/')
    except Exception:
        return redirect('http://127.0.0.1:8000/account/register/')
    
class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            username_or_email = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = User.objects.filter(username=username_or_email).first() or User.objects.filter(email=username_or_email).first()
            if user:
                user = authenticate(username=user.username,password=password)
                if user:
                    refresh = RefreshToke.for_user(user)
                    login(request,user)
                    
                    return Response({
                        "success":True,
                        "statusCode":status.HTTP_200_OK,
                        "message":"Looged in successfully",
                        "data":{
                            "refresh":str(refresh),
                            "access": str(refresh.access_token),
                            "user_id":user.id,
                            "username":user.username,
                        }
                    },status=status.HTTP_200_OK)
                else:
                    return Response({
                    "success":False,
                    "message":"Invalid credentials.",
                    "error":"Please check your username or password.",
                    "statusCode":status.HTTP_400_BAD_REQUEST,
                },status=status.HTTP_400_BAD_REQUEST)
            else:
               return Response({
                "success":False,
                "message":"Invalid username or email.",
                "error":"User not found.",
                "statusCode":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({
                "success":False,
                "message":"Invalid input",
                "error": serializer.errors,
                "statusCode":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
            
                
        
        
        