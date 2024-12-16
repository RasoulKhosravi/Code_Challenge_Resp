from django.urls import path
from .views import UserRegistrationView, UserLoginView

urlpatterns = [
    path('users/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('users/login/', UserLoginView.as_view(), name='user-login'),

]