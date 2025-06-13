
#? Import Necessary modules
from django.urls import path
from .views import (
    IssueListView, add_board, add_issue, delete_issue, edit_issue, move_issue
)

#? URL patterns for the issues app
urlpatterns = [
    path('', IssueListView.as_view(), name='issues_list'),                    #* List of issues URL
    path('add_board/', add_board, name='add_board'),                          #* Add a new board URL for js(AJAX)
    path('add_issue/', add_issue, name='add_issue'),                          #* Add a new issue URL for js(AJAX)
    path('delete_issue/<int:issue_id>/', delete_issue, name='delete_issue'),  #* Delete an issue URL for js(AJAX) 
    path('edit_issue/<int:issue_id>/', edit_issue, name='edit_issue'),        #* Edit an issue URL for js(AJAX)
    path('move_issue/<int:issue_id>/', move_issue, name='move_issue'),        #* Move an issue URL for js(AJAX) - drag and drop
]