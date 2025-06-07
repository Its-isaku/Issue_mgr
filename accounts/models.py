
#? Necessary imports
from django.db import models
from django.contrib.auth.models import AbstractUser

#? Role model
class Role(models.Model):                                    #* This model defines the roles that users can have in the system
    name  = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    
    def __str__(self):
        return self.name
    
#? Team model
class Team(models.Model):                                    #* This model defines the teams that users can belong to
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    
    def __str__(self):
        return self.name
    
#? Custom model
class CustomUser(AbstractUser):                            #* This model extends the default Django user model to include additional fields for roles and teams
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )