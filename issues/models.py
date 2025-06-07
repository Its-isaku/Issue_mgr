
#? Necessary imports
from django.db import models
from django.contrib.auth.models import get_user_model
from django.urls import reverse
from accounts.models import Team

#? Model for Status
class Status(models.Model):
    name = models.CharField(max_length=128)                      #* Name of the status
    description = models.CharField(max_length=256)               #* Description of the status
    
    def __str__(self):                                           #* String representation of the status
        return self.name

#? Model for Issue
class Issue(models.Model):
    title = models.CharField(max_length=128)                     #* Title of the issue
    summary = models.CharField(max_length=512)                   #* Summary of the issue
    description = models.TextField()                             #* Detailed description of the issue
    
    reporter = models.ForeignKey(                                #* User who reported the issue
        get_user_model(), 
        on_delete=models.SET_NULL,
        null=True
    )
    
    assignee = models.ForeignKey(                                #* User assigned to the issue                                  
        get_user_model(), 
        on_delete=models.SET_NULL,
        null=True,
        related_name='assignee'
    )
    
    status = models.ForeignKey(                                  #* Current status of the issue
        Status, 
        on_delete=models.SET_NULL,
        null=True
    )
    
    assigned_team = models.ForeignKey(                           #* Team assigned to the issue
        Team, 
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    
    created_on = models.DateTimeField(auto_now_add=True)         #* Timestamp when the issue was created
    
    def __str__(self):                                           #* String representation of the issue
        return self.name
    
    def get_absolute_url(self):                                  #* Returns the URL for the issue detail view
        return reverse('URL_NAME', args=[self.id])               #! Replace 'URL_NAME' with the actual name of the URL pattern for issue detail view