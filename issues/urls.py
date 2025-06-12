
#? Import Necessary modules
from django.urls import path
from .views import (
    IssueListView
)

#? URL patterns for the issues app
urlpatterns = [
    path('', IssueListView.as_view(), name='issues_list'),        #* List of issues URL
]