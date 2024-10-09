from django.contrib import admin
from .models import League, Team, Match, LeagueTeam, LeagueStanding
from django.http import HttpResponse
import http.client, json

# Register your models here.

#---------------------------------------------------------------------------------------------------------------
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'country', 'country_code')  # Các trường bạn muốn hiển thị trong danh sách
    search_fields = ('name', 'country')
    list_filter = ('type', 'country')

#---------------------------------------------------------------------------------------------------------------
class LeagueStandingAdmin(admin.ModelAdmin):
    list_display = ('season', 'rank', 'id', 'country_name', 'league_id', 'league_name', 'team_id', 'team_name', 'points')  # Các trường bạn muốn hiển thị trong danh sách
    search_fields = ('league_id', 'league_name', 'team_id', 'team_name', 'season')

#---------------------------------------------------------------------------------------------------------------
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home', 'away', 'league_id', 'date', 'status')
    search_fields = ('home__name', 'away__name', 'league__name', 'status')
    list_filter = ('league_id', 'status', 'date')

#---------------------------------------------------------------------------------------------------------------
# REGISTER ADMIN
admin.site.register(League, LeagueAdmin)
admin.site.register(LeagueStanding, LeagueStandingAdmin)
admin.site.register(Match, MatchAdmin)
