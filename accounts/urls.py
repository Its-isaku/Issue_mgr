
#? Import necesary modules for Accounts app
from django.urls import path
from .views import (
    SignUpView,
    )  

#? URL patterns for the accounts app
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),                          #* signup page URLL
]