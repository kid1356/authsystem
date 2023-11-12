from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Team)
class AddTeam(admin.ModelAdmin):
    list_display = ['id', 'captain','coach_name','team_name']

@admin.register(Player)
class AddPlayer(admin.ModelAdmin):
    list_display = ['id','captain','player_name', 'Team_name']
    def Team_name(self, obj):
        return obj.Team_Id.team_name if obj.Team_Id else "No Team"

    Team_name.short_description = 'Team'