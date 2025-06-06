
#? Importing necessary modules
from django.views.generic import TemplateView

#! |-----------Class-based views for the pages app-----------|

#? Home page view 
class HomePageView(TemplateView):
    template_name = 'pages/home.html'   #* Template for the home page

#? About page view 
class AboutPageView(TemplateView):
    template_name = 'pages/about.html'  #* Template for the about page
