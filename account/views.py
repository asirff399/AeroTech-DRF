from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.response import Response
from rest_framework import status
# Mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


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