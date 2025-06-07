
#? Nesesary imports
from django.contrib.auth.forms import (
    UserCreationForm,                                                          #* form for creating a new user
    UserChangeForm,                                                            #* form for changing an existing user
)
from django.utils.translation import gettext_lazy as _                         #* translation support
from .models import CustomUser                                                 #* import the CustomUser model

#? Custom user creation 
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):                                         #* create a new user with additional fields for email, role, and team
        model = CustomUser                                                     #* use the CustomUser model
        fields = UserCreationForm.Meta.fields + ('email', 'role', 'team')      #* include email, role, and team fields in the form
        labels = {
            'email': _('Email Address'),                                       #* label for the email field
            'role': _('Role'),                                                 #* label for the role field
            'team': _('Team'),                                                 #* label for the team field
        }
        help_texts = {
            'email': _('Enter a valid email address.'),                        #* help text for the email field
            'role': _('Enter your role int he team'),                          #* help text for the role field
            'team': _('which team are you assigned to?'),                      #* help text for the team field
        }
        
#? Custom change forms
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):                                           #* change an existing user with additional fields for email, role, and team
        model = CustomUser                                                     #* use the CustomUser model
        fields = UserChangeForm.Meta.fields                                    #* it will be handled by the admin interface