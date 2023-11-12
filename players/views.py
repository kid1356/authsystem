from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework import permissions,status
from rest_framework.response import Response
# Create your views here.

class CustomPermissions(permissions.BasePermission):
    def has_permission(self, request, view):

        return request.user.roll == 'Captain'
    
class IsCaptainOfPlayer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.captain == request.user



class TeamRegisterView(APIView):
    permission_classes = [CustomPermissions]

    def post(self, request):
        team = request.data.get('team_name')
        team_exists = Team.objects.filter(team_name = team).first()

        if team_exists:
            return Response('This Team name already Exists', status=status.HTTP_406_NOT_ACCEPTABLE)
        
        serializer = TeamSerializer(data =  request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(captain = request.user)

            return Response({'Team registered Successfully':serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetTeamView(APIView):
    def get(self,request,id=None):
        if id is not None:
            try:
                team = Team.objects.get(id =id)
            except Team.DoesNotExist:
                return Response('Team Not Found!', status= status.HTTP_404_NOT_FOUND)
        
            serializer = TeamSerializer(team)

            return Response({'Team':serializer.data}, status=status.HTTP_200_OK)
        else:
            teams = Team.objects.all()
            serializer = TeamSerializer(teams, many=True)
            return Response({'Teams':serializer.data}, status= status.HTTP_200_OK)


class PlayerRegisterView(APIView):
    permission_classes = [CustomPermissions]

    def post(self, request):
        player_email = request.data.get('player_email')
        player_exists = Player.objects.filter(player_email = player_email).exists()

        if player_exists:
            return Response('This Player email already Exists', status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = PlayerSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(captain = request.user)

            return Response({'Player register successfully':serializer.data}, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class  GetPlayerView(APIView):
    def get(self, request, id=None):
        if id is not None:
            try:
             player = Player.objects.get(pk=id)

            except Player.DoesNotExist:
               return Response("Player not find!", status=status.HTTP_400_BAD_REQUEST)
        
            serializer = PlayerSerializer(player)

            return Response({"Data" : serializer.data}, status=status.HTTP_200_OK)
        
        else:
            players = Player.objects.all()
            serializer = PlayerSerializer(players, many = True)
            return Response({"players": serializer.data}, status= status.HTTP_200_OK)
        

class DeletePlayerView(APIView):
    permission_classes = [IsCaptainOfPlayer]

    def delete(self, request,id):

        try:
            player = Player.objects.get(id =id)
            print('request_user.........', request.user)
            print('capatain..........', player.captain)

            if player.captain != request.user:
              return Response("This Player Not Belongs to Your Team So U can not delete", status=status.HTTP_403_FORBIDDEN)
            
            serializer = PlayerSerializer(player)
            player.delete()
        except Player.DoesNotExist:
            return Response("Player Not found")
        
        return Response({'Player Is Deleted':serializer.data}, status= status.HTTP_200_OK)