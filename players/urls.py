from django.urls import path
from .views import *

urlpatterns = [
   path('register/', TeamRegisterView.as_view(), name = 'teamregister'),
   path('get-team/<int:id>/', GetTeamView.as_view(), name = 'get-specific-team'),
   path('get-team/', GetTeamView.as_view(), name = 'gettingteams'),
   path('player/register/', PlayerRegisterView.as_view(), name='playerregister'),
   path('getplayer/<int:id>', GetPlayerView.as_view(), name= 'get-specific-Player'),
   path('getplayer', GetPlayerView.as_view(), name= 'gettingPlayers'),
   path('delete/player/<int:id>', DeletePlayerView.as_view(), name='deletePlayer'),
]