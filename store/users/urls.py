from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (EmailVerificationView, UserLoginView, UserLogoutView,
                         UserProfileView, UserRegistrationView)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    # path('login/', login, name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    # path('registration/', registration, name='registration'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    # path('profile/', profile, name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('logout/', logout, name='logout'),
    # path('logout/', logout, name='logout'),
]
