
#? Import necessary modules
from django.urls import path
from .views import (
    HomePageView, 
    AboutPageView,
)

#? URL patterns for the pages app
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),              #* Home page URL
    path('about/', AboutPageView.as_view(), name='about'),      #* About page URL
]