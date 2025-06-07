
#? Necessary imports
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm                        #* Import the custom user creation form

# ? User SignUp view
class SignUpView(CreateView):
    template_name = 'registration/signup.html'                   #* Template for the signup page
    form_class = CustomUserCreationForm                          #* Form for user registration
    success_url = reverse_lazy('login')                          #* Redirect to login page after successful registration