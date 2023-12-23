from django.urls import path

from .views import UserLoginView, UserRegistrationView

app_name = 'users'

urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('signin/', UserLoginView.as_view(), name='signin'),
]
