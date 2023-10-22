
from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', LogInView.as_view(), name = 'login'),
    path('profile/', UserProfileView.as_view(), name = 'profile'),
    path('change-password/', UserChangePasswordView.as_view(), name = 'change-password'),
    path('change-password-email/', UserResetEmailView.as_view(), name = 'change-password-email'),
    path('forget-password/<uid>/<token>/', ResetForgetPasswordView.as_view(), name = 'forget-password'),
]