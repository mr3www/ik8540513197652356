from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    # RENDER
    path('admin88888888/fetch-data/', lambda request: render(request, 'fetch_data.html'), name='fetch_data'),

    # ACTIONS
    path('fetch-leagues/', views.fetch_and_save_leagues, name='fetch_and_save_leagues'),
    path('fetch-matches/', views.fetch_and_save_matches, name='fetch_and_save_matches'),
    path('fetch-standings/', views.fetch_and_save_standings, name='fetch_and_save_standings'),
    path('fetch-teams/', views.fetch_and_save_teams, name='fetch_and_save_teams'),
    path('fetch-team-season-statistics/', views.fetch_and_save_teams_statistic, name='fetch_and_save_teams_statistic'),
    path('fetch_and_save_players/', views.fetch_and_save_players, name='fetch_and_save_players'),
    path('fetch_and_save_news/', views.fetch_and_save_news, name='fetch_and_save_news'),




    path('update_legend_color/', views.update_legend_colors, name='update_legend_colors'),
    path('scrape_team_link/', views.scrape_team_link, name='scrape_team_link'),

]