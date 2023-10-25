from rest_framework import serializers
from .models import *
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
from pyotp import TOTP
from django.contrib.auth import password_validation
from authentication.settings import *

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type':'password'},write_only = True)
    class Meta:
        model = User
        fields = ['email', 'name', 'roll','CNIC','contact','city','password','password2']

        extra_kwargs = {
            'password':{'write_only' : True},
            'roll':{'required':True},
            "email":{'required': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password!=password2:
            raise serializers.ValidationError("Password and Confirm password does not match")

        return attrs
    
    def create(self, validate_data):
     
     
     return User.objects.create_user(**validate_data)


class LogInSerializer(serializers.ModelSerializer):
   email = serializers.EmailField(max_length = 255)
   class Meta:
      model = User
      fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ['id','email','name', 'roll']

class UserChangePasswordSerializer(serializers.Serializer):
    password= serializers.CharField(max_length = 255, style = {'input_type':'password'}, write_only = True)
    password2= serializers.CharField(max_length = 255, style = {'input_type':'password'}, write_only = True)

    class Meta:
      fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs




class ResetPasswordSendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, attrs):
        email = attrs.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist!")

        # Generate an OTP
        user.generate_and_store_otp_secret_key()

        otp_secret_key = user.secret_key
        print("sssss..............",otp_secret_key)
        otp = TOTP(otp_secret_key, digits= TOTP_DIGITS, interval=TOTP_TIME_STEP, digest=TOTP_ALGORITHM)

        print(".otp..............",otp)
        otp_value = otp.now()
        print(".otp..............",otp_value)


        a= User.objects.get(secret_key=otp_secret_key)
        print("aaaaaaaaaaaaa................",a)
        # Send the OTP to the user's email
        data = {
            'subject': 'Your Password Reset OTP',
            'body': f'Your OTP for password reset is: {otp_value}',
            'to_email': user.email,
        }

        Util.send_mail(data)
        return attrs

class ResetForgetPasswordSerializer(serializers.Serializer):
    otp_value = serializers.CharField(max_length=6, write_only=True)
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        otp_value = attrs.get('otp_value')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
     
        print("otp..............",otp_value)
        print('user.........', user)
        


        
        # print("screst .....................",user.secret_key)
        print("user ..............",user.secret_key)

        # Verify the OTP
        otp = TOTP(user.secret_key, digits= TOTP_DIGITS, interval=TOTP_TIME_STEP, digest=TOTP_ALGORITHM)

        print("validate..........",otp.verify(otp_value))
        if not otp.verify(otp_value):
            raise serializers.ValidationError('Invalid OTP')
        

        # Check if the provided passwords match
        if password != password2:
            raise serializers.ValidationError('Passwords do not match')

        # Validate the new password
        
        password_validation.validate_password(password, user=user)
       
        # Set the new password and save the user
        user.set_password(password)
        user.save()

        return attrs