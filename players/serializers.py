from rest_framework import serializers
from .models import *

class TeamSerializer(serializers.ModelSerializer):
    captain_name = serializers.SerializerMethodField()
    class Meta:
        model = Team
        fields = ['captain','captain_name', 'team_name', 'city','coach_name', 'coach_email']
        extra_kwargs = {
            # 'captain':{'required':True},
            'team_name':{'required':True},
            'coach_name': {'required':True},
        }

    def get_captain_name(self, obj):
        return obj.captain.name



class PlayerSerializer(serializers.ModelSerializer):
    captain_name = serializers.SerializerMethodField()
    team_name =  serializers.SerializerMethodField()
    class Meta:
        model = Player
        fields = ['captain','captain_name', 'Team_Id','team_name','player_name','player_email']
        extra_kwargs = {
            # 'captain':{'required':True},
            'Team_Id':{'required':True},
            'player_name':{'required':True},
            'player_email': {'required':True},
        }

    def get_captain_name(self,obj):

        return obj.captain.name
    
    def get_team_name(self,obj):

        return obj.Team_Id.team_name