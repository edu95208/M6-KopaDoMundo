from rest_framework.views import APIView, status
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.request import Request
from teams.models import Team
from utils import data_processing
from exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError


# Create your views here.
class TeamsView(APIView):

    def post(self, request: Request) -> Response:
        try:
            data_processing(request.data)
            teamsCreate = Team.objects.create(**request.data)
            return Response(model_to_dict(teamsCreate), 201)
        except (NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError) as e:
            return Response({"error": str(e)}, 400)

    def get(self, request: Request) -> Response:
        teamsAll = Team.objects.all()
        teams_dict = []

        for team in teamsAll:
            teams_dict.append(model_to_dict(team))
        return Response(list(teamsAll.values()))


class TeamsDetailView(APIView):

    def get(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status=status.HTTP_404_NOT_FOUND
            )
        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)

    def delete(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status=status.HTTP_404_NOT_FOUND
            )

        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
        teams_data = request.data
        for field, value in teams_data.items():
            setattr(team, field, value)
        team.save()
        return Response(model_to_dict(team), status.HTTP_200_OK)
