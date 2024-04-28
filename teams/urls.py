from django.urls import path
from teams.views import TeamsView, TeamsDetailView


urlpatterns = [
    path('teams/', TeamsView.as_view()),
    path('teams/<int:team_id>/', TeamsDetailView.as_view()),
]
