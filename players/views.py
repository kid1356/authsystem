
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .permissions import *
# Create your views here.


#Team views

class TeamRegisterView(APIView):
    permission_classes = [CaptainPermissions]

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
            return Response({'All Teams':serializer.data}, status= status.HTTP_200_OK)
        

class PatchTeamView(APIView):
    permission_classes = [IsCaptainOfPlayer]
    def patch(self,request, id):
        try:
            team = Team.objects.get(id=id)
        except Team.DoesNotExist:
            return Response("Team not found")
        
        if not IsCaptainOfPlayer().has_object_permission(request, self, team):
            return Response("you are not the captain of this team", status=status.HTTP_403_FORBIDDEN)
        
        serializer= TeamSerializer(team, data=request.data, partial = True)
        if serializer.is_valid(raise_exception=True):
           serializer.save()
           return Response({"Team Updated successfully": serializer.data}, status=status.HTTP_200_OK)


class TeamAllPlayerView(APIView):
    def get(self, request,id):
        try:
            team = Team.objects.get(id =id)
        except Team.DoesNotExist:
            return Response("team does not exists")
        
        team_serializer = TeamSerializer(team)
        players = Player.objects.filter(Team_Id = team)
        player_data = [{'player_name':player.player_name,'Player_email':player.player_email} for player in players]
        response = {
            'Team ': team_serializer.data,
            'Players': player_data
        }

        return Response(response, status=status.HTTP_200_OK )

class DeleteTeamView(APIView):
    permission_classes = [IsCaptainOfPlayer]
    def delete(self,request, id):
        try:
            team = Team.objects.get(id=id)
            print('request_user.........', request.user)
            print('capatain..........', team.captain)

            if team.captain != request.user:
                return Response("You are not the captain so U can not delete it", status=status.HTTP_400_BAD_REQUEST)
            
            serializer = TeamSerializer(team)
            team.delete()
        except Team.DoesNotExist:
            return Response("Team Not Found", status=status.HTTP_404_NOT_FOUND)
        
        return Response({"team is deleted":serializer.data}, status=status.HTTP_200_OK)


# Players Views

class PlayerRegisterView(APIView):
    permission_classes = [CaptainPermissions]

    def post(self, request):
        
        try:
            team  = Team.objects.get(captain = request.user)
        except Team.DoesNotExist:
            return Response("You are not assign to any team", status= status.HTTP_400_BAD_REQUEST)

        player_email = request.data.get('player_email')

        if Player.objects.exclude(Team_Id__captain = request.user).filter(player_email=player_email).exists():
            return Response("Player email is taken already", status=status.HTTP_400_BAD_REQUEST)
        

        if Player.objects.filter(Team_Id = team, player_email = request.data.get('player_email')).exists():
            return Response("player email is already registered in the current team.", status=status.HTTP_400_BAD_REQUEST)

        serializer = PlayerSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):

            if serializer.validated_data['Team_Id'] != team:
                return Response("You can only register players for your own team", status=status.HTTP_403_FORBIDDEN)
            
            serializer.save(captain = request.user, Team_Id = team)

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