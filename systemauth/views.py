from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh":str(refresh),
        "access" : str(refresh.access_token),
    }

class RegisterView(APIView):
    
    def post(self, request):
        serializer = RegisterSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()

        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg':'registered successfully'},status=status.HTTP_201_CREATED)
    

class LogInView(APIView):

    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        role = serializer.data.get('role')

        user =authenticate(email=email, password = password)

        if user is not None:
           token = get_tokens_for_user(user)
           return Response ({'token':token ,"user data":serializer.data,'msg':'Login Successfully'}, status=status.HTTP_200_OK)
        
        return Response({'Errors':'Login credentail is invalid' }, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer =UserProfileSerializer(request.user)

        token = get_tokens_for_user(request.user)
        return Response({'token':token,'user data':serializer.data} , status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)

        return Response({'success':'Password change successfully'}, status=status.HTTP_200_OK)
    
class UserResetEmailView(APIView):
    def post(self,request):
        serializer = ResetPasswordSendEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'msg': 'An Email Sent to Your Gmail Please check it'}, status=status.HTTP_200_OK)
    

class ResetForgetPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ResetForgetPasswordSerializer(data=request.data,context={'user':request.user})
        serializer.is_valid(raise_exception=True)

        return Response({'msg':'Password Reset Successfully'}, status= status.HTTP_200_OK)
     