from django.contrib import admin
from .models import League, Team, Match

# Register your models here.

admin.site.register(League)
admin.site.register(Team)
admin.site.register(Match)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('league_name', 'league_type', 'country_name', 'country_code')
