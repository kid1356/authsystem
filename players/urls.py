from django.urls import path
from .views import *

urlpatterns = [
   path('register/', TeamRegisterView.as_view(), name = 'teamregister'),
   path('get-team/<int:id>/', GetTeamView.as_view(), name = 'get-specific-team'),
   path('team-all-players/<int:id>/', TeamAllPlayerView.as_view(), name = 'all-team-players'),
   path('get-team/', GetTeamView.as_view(), name = 'gettingteams'),
   path('patch-team/<int:id>', PatchTeamView.as_view(), name="patch-team"),
   path('delete-team/<int:id>', DeleteTeamView.as_view(), name='delete-team'),
   path('player/register/', PlayerRegisterView.as_view(), name='playerregister'),
   path('getplayer/<int:id>', GetPlayerView.as_view(), name= 'get-specific-Player'),
   path('getplayer', GetPlayerView.as_view(), name= 'gettingPlayers'),
   path('delete/player/<int:id>', DeletePlayerView.as_view(), name='deletePlayer'),
]