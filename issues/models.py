
#? Necessary imports
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Team

#? Model for Board
class Board(models.Model):
    name = models.CharField(max_length=128)                      #* Name of the board
    
    def __str__(self):                                           #* String representation of the board
        return self.name

#? Model for Status(Section)
class Status(models.Model):
    name = models.CharField(max_length=128)                      #* Name of the status
    description = models.CharField(max_length=256)               #* Description of the status
    board = models.ForeignKey(                                   #* Board to which the status belongs
        Board,
        related_name='statuses',                                 #* Related name for reverse lookup
        on_delete=models.CASCADE                                 #* Delete all statuses if the board is deleted
        )              
    is_fixed = models.BooleanField(default=False)                #* Indicates if its a default status
    
    def __str__(self):                                           #* String representation of the status
        return self.name

#? Model for Issue(card)
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
    
    priority = models.CharField(                                 #* Priority of the issue
        max_length=32,
        choices=[
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High'),
            ('Critical', 'Critical')
        ],
        default='Low'
    )
    
    story_points = models.PositiveIntegerField(default=0)        #* Story points for the issue
    board = models.ForeignKey(                                   #* Board to which the issue belongs
        Board,
        on_delete=models.CASCADE,
        related_name='issues',
        null=True,
        blank=True
    )
    
    created_on = models.DateTimeField(auto_now_add=True)         #* Timestamp when the issue was created
    
    def __str__(self):                                           #* String representation of the issue
        return self.title