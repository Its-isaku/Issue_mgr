
#? import Necessary modules
from django.contrib import admin
from .models import Board, Status, Issue

#? Register models in admin site
admin.site.register(Board)          #* Register Board model
admin.site.register(Status)         #* Register Status model
admin.site.register(Issue)          #* Register Issue model 