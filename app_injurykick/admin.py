from django.contrib import admin
from .models import League, Team, Match, LeagueStanding, Player, LastestSidelined, TeamMapping
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
class TeamAdmin(admin.ModelAdmin):
    list_display = (
            'id', 'api_id', 'name', 'code', 'country', 'founded', 'image', 'image_custom',
            'venue_id', 'venue_name', 'venue_address', 'venue_city', 'venue_capacity',
            'venue_surface', 'venue_image'
        )
    search_fields = ('name', 'country', 'venue_name')
    list_filter = ('country', 'founded')
    ordering = ('name',)
    readonly_fields = ('id', 'venue_id')
    
#---------------------------------------------------------------------------------------------------------------
class MatchAdmin(admin.ModelAdmin):
    # Hiển thị các trường cần thiết trong danh sách
    list_display = (
        'id', 'api_id', 'season', 'league_id', 'country_name', 'home', 'away',
        'date', 'status', 'referee', 'venue_name', 'ht_home', 'ht_away', 'ft_home', 'ft_away'
    )

    # Cho phép tìm kiếm theo các trường quan trọng
    search_fields = ('home__name', 'away__name', 'league_id__name', 'referee')

    # Thêm bộ lọc theo mùa giải, quốc gia, trạng thái và ngày thi đấu
    list_filter = ('season', 'country_name', 'status', 'date')

    # Sắp xếp mặc định theo ngày thi đấu
    ordering = ('date',)
    
    # Hiển thị chi tiết trận đấu
    readonly_fields = ('id', 'api_id')

#---------------------------------------------------------------------------------------------------------------
class PlayerAdmin(admin.ModelAdmin):
    # Hiển thị các trường cần thiết trong danh sách
    list_display = (
        'id', 'api_id', 'name', 'first_name', 'last_name', 
        'date_of_birth', 'nationality', 'height', 'position'
    )

    # Cho phép tìm kiếm theo các trường quan trọng
    search_fields = ('name', 'first_name', 'last_name', 'nationality', 'position')

    # Thêm bộ lọc theo quốc gia và vị trí
    list_filter = ('nationality', 'position')

    # Sắp xếp mặc định theo tên cầu thủ
    ordering = ('name',)

    # Hiển thị chi tiết cầu thủ
    readonly_fields = ('id', 'api_id')

#---------------------------------------------------------------------------------------------------------------
class LastestSidelinedAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'team_name', 'injury_type', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('team_name', 'injury_type', 'status')
    search_fields = ('player_name', 'team_name', 'injury_type')
    ordering = ('-created_at',)

#---------------------------------------------------------------------------------------------------------------
class TeamMappingdAdmin(admin.ModelAdmin):
    list_display = ('id', 'transfer_team_name', 'team')
    search_fields = ('id', 'transfer_team_name', 'team')






# REGISTER ADMIN
admin.site.register(League, LeagueAdmin)
admin.site.register(LeagueStanding, LeagueStandingAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(LastestSidelined, LastestSidelinedAdmin)
admin.site.register(TeamMapping, TeamMappingdAdmin)


