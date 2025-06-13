
#? Import Necessary Libraries
from django import forms
from django.contrib.auth import get_user_model
from .models import Issue, Status, Board

#? Board form
class BoardForm(forms.ModelForm):
    class Meta:
        model = Board                                              #* Model for Board
        fields = ['name']                                          #* Fields to be included in the form

#? Issue form with team-based assignee selection
class IssueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assignee'].queryset = get_user_model().objects.all() 
        self.fields['assignee'].empty_label = "Select assignee"
    
    class Meta: 
        model = Issue                                               #* Model for Issue
        fields = ['title', 'summary', 'description', 'assignee', 'priority', 'story_points']   #* Fields to be included in the form