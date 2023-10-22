from rest_framework import serializers
from .models import *
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util

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
        class Meta:
            fields = ['email']

        def validate(self, attrs):
            email = attrs.get('email')

            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)

                uid = urlsafe_base64_encode(force_bytes(user.id))

                token  = PasswordResetTokenGenerator().make_token(user)

                link = 'http://Localhost:8000'+'/' + uid + '/' +token

                body = 'click the following link ' + link
                data = {
                    'subject':'Your Password Reset Link',
                    'body':body,
                    'to_email' : user.email
                }
                
                Util.send_mail(data)
                return attrs
            
            raise serializers.ValidationError("Your are not register!")
        

class ResetForgetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255, style = {'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length = 255, style = {'input_type':'password2'}, write_only=True)

    class Meta:
        fields =['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')

        if password != password2:
            raise serializers.ValidationError('Both password should be match!')
        
        id  = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id=id)

        if not PasswordResetTokenGenerator().check_token(user,token):
           raise serializers.ValidationError('Token not valid')
        
        user.set_password(password)
        user.save()

        return attrs