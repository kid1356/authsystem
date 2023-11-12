from django.db import models
from systemauth.models import User
# Create your models here.


class Team(models.Model):
    captain = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True )
    team_name = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    coach_name = models.CharField(max_length=200, null= True, blank=True)
    coach_email = models.EmailField(max_length=200, null=True, blank=True, unique=True)


class Player(models.Model):
    captain = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Team_Id = models.ForeignKey(Team, models.CASCADE, null=True, blank=True)
    player_name = models.CharField(max_length=200, null=True, blank=True)
    player_email = models.EmailField(max_length=200, null=True, blank=True, unique=True)