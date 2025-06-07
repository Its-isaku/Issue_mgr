
#? Necesary imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import CustomUser
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm
)

#? Custom User Admin
class CustomUserAdmin(UserAdmin):
    list_display = [                                               #* Fields to display in the user list
        "username", "last_name", "first_name",
        "role", "team", "last_login", "is_staff"
    ]
    add_form = CustomUserCreationForm                              #* Form for adding a new user
    form = CustomUserChangeForm                                    #* Form for changing an existing user
    add_fieldsets = (                                              #* Fields to display when adding a new user
        (
            None, {
                "classes": ("wide",),
                "fields": (
                    "username", "email", "role",
                    "team", "password1", "password2"
                )
            }
        )
    )
    fieldsets = UserAdmin.fieldsets + (                            #* Additional fields to display in the user change form
        (None, {"fields": ("role", "team")}),             #* Adding email, role, and team fields to the user admin
    )

admin.site.register(CustomUser, CustomUserAdmin)                   #* Registering the CustomUser model with the custom admin interface