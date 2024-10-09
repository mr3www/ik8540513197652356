from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import League, Match, LeagueTeam, LeagueStanding, Team, TeamSeasonStatistics
import http.client
import json, requests

# Create your views here.
# Đặt headers cho API
headers = {
	"x-rapidapi-key": "69add1c8a2mshd66c5aa11eccb10p1c1f6bjsnd3f6750e5f0a",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

leagues_id_list = [39]  # ID các giải đấu , 140, 135, 78, 61
season_list = [2024]

#---------------------------------------------------------------------------------------------------------------
def fetch_and_save_leagues(request):
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
    
    response = requests.get(url, headers=headers)
    leagues = response.json()

    for league in leagues['response']:
        league_data = league['league']
        country_data = league['country']

        league_id = league_data['id']
        league_name = league_data['name']
        league_type = league_data['type']
        league_logo = league_data.get('logo')
        country_name = country_data['name']
        country_code = country_data.get('code')
        country_flag = country_data.get('flag')

        League.objects.update_or_create(
            api_id=league_id,
            defaults={
                'api_id': league_id,
                'name': league_name,
                'type': league_type,
                'image': league_logo,
                'country': country_name,
                'country_code': country_code,
                'country_flag': country_flag,
            }
        )

    return HttpResponse("Leagues imported successfully.")


#---------------------------------------------------------------------------------------------------------------
def fetch_and_save_standings(request):
    url = "https://api-football-v1.p.rapidapi.com/v3/standings"

    for league in leagues_id_list:
        for season in season_list:
            querystring = {"league": league, "season": season}
            response = requests.get(url, headers=headers, params=querystring)
            standings = response.json()

            # Kiểm tra xem có dữ liệu không
            if standings['results'] > 0:
                for standing in standings['response']:
                    league_data = standing['league']
                    league_id = league_data['id']
                    league_name = league_data['name']
                    country_name = league_data['country']
                    season = league_data['season']
                    
                    for team_standing in league_data['standings'][0]:  # Giả sử bạn chỉ cần standings đầu tiên
                        team = team_standing['team']
                        rank = team_standing['rank']
                        team_id = team['id']
                        team_name = team['name']
                        logo = team['logo']
                        points = team_standing['points']
                        goals_diff = team_standing['goalsDiff']
                        
                        all_stats = team_standing['all']
                        played = all_stats['played']
                        win = all_stats['win']
                        draw = all_stats['draw']
                        lose = all_stats['lose']
                        goals_for = all_stats['goals']['for']
                        goals_against = all_stats['goals']['against']
                        update_time = team_standing['update']

                        # Lưu hoặc cập nhật dữ liệu vào cơ sở dữ liệu
                        LeagueStanding.objects.update_or_create(
                            league_id=league_id,
                            season=season,
                            rank=rank,
                            defaults={
                                'league_name': league_name,
                                'country_name': country_name,
                                'team_id': team_id,
                                'team_name': team_name,
                                'logo': logo,
                                'points': points,
                                'goals_diff': goals_diff,
                                'played': played,
                                'win': win,
                                'draw': draw,
                                'lose': lose,
                                'goals_for': goals_for,
                                'goals_against': goals_against,
                                'update_time': update_time,
                            }
                        )

    return HttpResponse("Standings imported successfully.")


#---------------------------------------------------------------------------------------------------------------
def fetch_and_save_teams(request):  # Client need add dropdown select season before fetch team data. 

    # Lấy danh sách các đội bóng theo league_id và season
    teams_in_league = LeagueStanding.objects.filter(season=2024).values('team_id')

    # Gọi API cho từng team và lưu dữ liệu
    for team in teams_in_league:
        team_id = team['team_id']
        print(f"Processing team_id: {team_id}")

        # Gọi hàm fetch_and_save_team_data để gọi API và lưu dữ liệu vào model Team
        fetch_and_save_team_info(team_id)

    return HttpResponse("Teams imported successfully.")

def fetch_and_save_team_info(team_id):

    url = "https://api-football-v1.p.rapidapi.com/v3/teams"

    querystring = {"id": team_id}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()

        # Kiểm tra nếu dữ liệu trả về có trong `response`
        if 'response' in data and data['response']:
            team_data = data['response'][0]['team']  # Lấy dữ liệu team
            venue_data = data['response'][0]['venue']  # Lấy dữ liệu sân vận động
            
            # Lưu hoặc cập nhật dữ liệu team vào cơ sở dữ liệu
            try:
                team, created = Team.objects.update_or_create(
                    api_id=team_data['id'],
                    defaults={
                        'api_id': team_data['id'],
                        'name': team_data['name'],
                        'code': team_data.get('code', ''),
                        'country': team_data.get('country', ''),
                        'founded': team_data.get('founded', None),
                        'image': team_data.get('logo', ''),

                        # Các trường liên quan đến sân vận động (venue)
                        'venue_id': venue_data.get('id'),
                        'venue_name': venue_data.get('name'),
                        'venue_address': venue_data.get('address'),
                        'venue_city': venue_data.get('city'),
                        'venue_capacity': venue_data.get('capacity'),
                        'venue_surface': venue_data.get('surface'),
                        'venue_image': venue_data.get('image'),
                    }
                )
                print(f"{'Created' if created else 'Updated'}: {team.name}")
            except Exception as e:
                print(f"Error saving team: {str(e)}")
        else:
            print("No team data found in the API response.")
    else:
        print(f"Failed to fetch data : {response.status_code}")

#---------------------------------------------------------------------------------------------------------------
def fetch_and_save_teams_statistic(request):
    season = 2024
    grouped_data = LeagueStanding.objects.filter(season=season).values('league_id')

    # Duyệt qua từng mùa giải và giải đấu
    for group in grouped_data:
        league_id = group['league_id']

        # Lấy danh sách các đội bóng theo league_id và season
        teams_in_league = LeagueStanding.objects.filter(league_id=league_id).values('team_id')

        # Gọi API cho từng team và lưu dữ liệu
        for team in teams_in_league:
            team_id = team['team_id']
            print(f"Processing team_id: {team_id}")

            # Gọi hàm fetch_and_save_team_data để gọi API và lưu dữ liệu vào model Team
            fetch_and_save_team_statistics_data(league_id, season, team_id)

    return HttpResponse("Team Statistics imported successfully.")
    

def fetch_and_save_team_statistics_data(league_id, season, team_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"

    querystring = {"league": league_id, "season": season, "team": team_id}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()

        # Kiểm tra nếu dữ liệu trả về có trong `response`
        if 'response' in data and data['response']:
            team_data = data['response']['team']  # Lấy dữ liệu team
            league_data = data['response']['league']
            biggest_data = data['response']['biggest']
            cleansheet_data = data['response']['clean_sheet']
            failed_to_score_data = data['response']['failed_to_score']
            fixtures_data = data['response']['fixtures']
            goals_data = data['response']['goals']
            lineups_data = data['response']['lineups']
            penalty_data = data['response']['penalty']

            biggest_data_goals = biggest_data['goals']
            biggest_data_loses = biggest_data['loses']
            biggest_data_streak = biggest_data['streak']
            biggest_data_wins = biggest_data['wins']
            fixtures_data_draws = fixtures_data['draws']
            fixtures_data_loses = fixtures_data['loses']
            fixtures_data_wins = fixtures_data['wins']
            fixtures_data_played = fixtures_data['played']
            goals_data_for = goals_data['for']
            goals_data_against = goals_data['against']
            lineups_data_0 = lineups_data[0] if len(lineups_data) > 0 else ''
            lineups_data_1 = lineups_data[1] if len(lineups_data) > 1 else ''
            penalty_data_missed = penalty_data['missed']
            penalty_data_scored = penalty_data['scored']

            goals_data_for_total = goals_data_for['total']
            goals_data_for_average = goals_data_for['average']
            goals_data_for_minute = goals_data_for['minute']
            goals_data_against_total = goals_data_against['total']
            goals_data_against_average = goals_data_against['average']
            goals_data_against_minute = goals_data_against['minute']

            goals_data_for_minute_0_15 = goals_data_for_minute['0-15']
            goals_data_for_minute_16_30 = goals_data_for_minute['16-30']
            goals_data_for_minute_31_45 = goals_data_for_minute['31-45']
            goals_data_for_minute_46_60 = goals_data_for_minute['46-60']
            goals_data_for_minute_61_75 = goals_data_for_minute['61-75']
            goals_data_for_minute_76_90 = goals_data_for_minute['76-90']
            goals_data_for_minute_91_105 = goals_data_for_minute['91-105']
            goals_data_for_minute_106_120 = goals_data_for_minute['106-120']

            goals_data_against_minute_0_15 = goals_data_against_minute['0-15']
            goals_data_against_minute_16_30 = goals_data_against_minute['16-30']
            goals_data_against_minute_31_45 = goals_data_against_minute['31-45']
            goals_data_against_minute_46_60 = goals_data_against_minute['46-60']
            goals_data_against_minute_61_75 = goals_data_against_minute['61-75']
            goals_data_against_minute_76_90 = goals_data_against_minute['76-90']
            goals_data_against_minute_91_105 = goals_data_against_minute['91-105']
            goals_data_against_minute_106_120 = goals_data_against_minute['106-120']

            biggest_data_goals_for = biggest_data_goals['for']
            biggest_data_goals_against = biggest_data_goals['against']
            biggest_data_loses_home = biggest_data_loses.get('home', None) #biggest_lose_home
            biggest_data_loses_away = biggest_data_loses.get('away', None) #biggest_lose_away
            biggest_data_streak_wins = biggest_data_streak['wins'] #biggest_streak_wins
            biggest_data_streak_draws = biggest_data_streak['draws'] #biggest_streak_draws
            biggest_data_streak_loses = biggest_data_streak['loses'] #biggest_streak_loses
            biggest_data_wins_home = biggest_data_wins.get('home', None) #biggest_wins_home
            biggest_data_wins_away = biggest_data_wins.get('away', None) #biggest_wins_away

            biggest_data_goals_for_home = biggest_data_goals_for['home'] #biggest_goals_home
            biggest_data_goals_for_away = biggest_data_goals_for['away'] #biggest_goals_away
            biggest_data_goals_against_home = biggest_data_goals_against['home'] #biggest_against_home
            biggest_data_goals_against_away = biggest_data_goals_against['away'] #biggest_against_away

            cleansheet_data_home = cleansheet_data['home'] #clean_sheet_home
            cleansheet_data_away = cleansheet_data['away'] #clean_sheet_away
            failed_to_score_data_home = failed_to_score_data['home'] #failed_to_score_home
            failed_to_score_data_away = failed_to_score_data['away'] #failed_to_score_away
            
            fixtures_data_draws_home = fixtures_data_draws['home'] #draws_home
            fixtures_data_draws_away = fixtures_data_draws['away'] #draws_away
            fixtures_data_loses_home = fixtures_data_loses['home'] #loses_home
            fixtures_data_loses_away = fixtures_data_loses['away'] #loses_away
            fixtures_data_wins_home = fixtures_data_wins['home'] #wins_home
            fixtures_data_wins_away = fixtures_data_wins['away'] #wins_away
            fixtures_data_played_home = fixtures_data_played['home'] #played_home
            fixtures_data_played_away = fixtures_data_played['away'] #played_away

            form_data = data['response']['form'] #form

            goals_data_for_total_home = goals_data_for_total['home'] #goals_total_home
            goals_data_for_total_away = goals_data_for_total['away'] #goals_total_away
            goals_data_for_avg_home = goals_data_for_average['home'] #goals_avg_home
            goals_data_for_avg_away = goals_data_for_average['away'] #goals_avg_away

            goals_data_against_total_home = goals_data_against_total['home'] #against_total_home
            goals_data_against_total_away = goals_data_against_total['away'] #against_total_away
            goals_data_against_avg_home = goals_data_against_average['home'] #against_avg_home
            goals_data_against_avg_away = goals_data_against_average['away'] #against_avg_away

            goals_data_for_minute_0_15_total = goals_data_for_minute_0_15['total'] #goals_0_15
            goals_data_for_minute_16_30_total = goals_data_for_minute_16_30['total'] #goals_16_30
            goals_data_for_minute_31_45_total = goals_data_for_minute_31_45['total'] #goals_31_45
            goals_data_for_minute_46_60_total = goals_data_for_minute_46_60['total'] #goals_46_60 
            goals_data_for_minute_61_75_total = goals_data_for_minute_61_75['total'] #goals_61_75
            goals_data_for_minute_76_90_total = goals_data_for_minute_76_90['total'] #goals_76_90
            goals_data_for_minute_91_105_total = goals_data_for_minute_91_105['total'] #goals_91_105
            goals_data_for_minute_106_120_total = goals_data_for_minute_106_120['total'] #goals_106_120

            goals_data_against_minute_0_15_total = goals_data_against_minute_0_15['total'] #against_0_15
            goals_data_against_minute_16_30_total = goals_data_against_minute_16_30['total'] #against_16_30
            goals_data_against_minute_31_45_total = goals_data_against_minute_31_45['total'] #against_31_45
            goals_data_against_minute_46_60_total = goals_data_against_minute_46_60['total'] #against_46_60
            goals_data_against_minute_61_75_total = goals_data_against_minute_61_75['total'] #against_61_75 
            goals_data_against_minute_76_90_total = goals_data_against_minute_76_90['total'] #against_76_90
            goals_data_against_minute_91_105_total = goals_data_against_minute_91_105['total'] #against_91_105
            goals_data_against_minute_106_120_total = goals_data_against_minute_106_120['total'] #against_106_120

            lineups_data_0_formation = lineups_data_0['formation'] if isinstance(lineups_data_0, dict) else ''
            lineups_data_0_played = lineups_data_0['played'] if isinstance(lineups_data_0, dict) else ''
            lineups_data_1_formation = lineups_data_1['formation'] if isinstance(lineups_data_1, dict) else ''
            lineups_data_1_played = lineups_data_1['played'] if isinstance(lineups_data_1, dict) else ''

            penalty_data_missed_total = penalty_data_missed['total']
            penalty_data_scored_total = penalty_data_scored['total']
            
            team_id_row = team_data['id']
            league_id_row = league_data['id']

            # Retrieve or create the Team instance
            team_instance, _ = Team.objects.get_or_create(
                api_id=team_data['id'],  # or use another unique identifier if needed
                defaults={
                    'name': team_data.get('name'),
                    'country': team_data.get('country'),
                    'founded': team_data.get('founded'),
                    'image': team_data.get('image'),
                    # Add other fields as necessary
                }
            )

            # Lưu hoặc cập nhật dữ liệu team vào cơ sở dữ liệu
            try:
                team, created = TeamSeasonStatistics.objects.update_or_create(
                    team=team_instance,
                    defaults={
                        'team': team_id_row,
                        'league': league_id_row,
                        'biggest_goals_home': biggest_data_goals_for_home,
                        'biggest_goals_away': biggest_data_goals_for_away,
                        'biggest_against_home': biggest_data_goals_against_home,
                        'biggest_against_away': biggest_data_goals_against_away,
                        'biggest_lose_home': biggest_data_loses_home,
                        'biggest_lose_away': biggest_data_loses_away,
                        'biggest_streak_wins': biggest_data_streak_wins,
                        'biggest_streak_draws': biggest_data_streak_draws,
                        'biggest_streak_loses': biggest_data_streak_loses,
                        'biggest_wins_home': biggest_data_wins_home,
                        'biggest_wins_away': biggest_data_wins_away,
                        'clean_sheet_home': cleansheet_data_home,
                        'clean_sheet_away': cleansheet_data_away,
                        'failed_to_score_home': failed_to_score_data_home,
                        'failed_to_score_away': failed_to_score_data_away,
                        'draws_home': fixtures_data_draws_home,
                        'draws_away': fixtures_data_draws_away,
                        'wins_home': fixtures_data_wins_home,
                        'wins_away': fixtures_data_wins_away,
                        'loses_home': fixtures_data_loses_home,
                        'loses_away': fixtures_data_loses_away,
                        'played_home': fixtures_data_played_home,
                        'played_away': fixtures_data_played_away,
                        'goals_total_home': goals_data_for_total_home,
                        'goals_total_away': goals_data_for_total_away,
                        'goals_avg_home': goals_data_for_avg_home,
                        'goals_avg_away': goals_data_for_avg_away,
                        'against_total_home': goals_data_against_total_home,
                        'against_total_away': goals_data_against_total_away,
                        'against_avg_home': goals_data_against_avg_home,
                        'against_avg_away': goals_data_against_avg_away,
                        'penalty_missed': penalty_data_missed_total,
                        'penalty_scored': penalty_data_scored_total,
                        'form': form_data,

                        # New: Goals and conceded goals by time
                        'goals_0_15': goals_data_for_minute_0_15_total,
                        'goals_16_30': goals_data_for_minute_16_30_total,
                        'goals_31_45': goals_data_for_minute_31_45_total,
                        'goals_46_60': goals_data_for_minute_46_60_total,
                        'goals_61_75': goals_data_for_minute_61_75_total,
                        'goals_76_90': goals_data_for_minute_76_90_total,
                        'goals_91_105': goals_data_for_minute_91_105_total,
                        'goals_106_120': goals_data_for_minute_106_120_total,

                        'against_0_15': goals_data_against_minute_0_15_total,
                        'against_16_30': goals_data_against_minute_16_30_total,
                        'against_31_45': goals_data_against_minute_31_45_total,
                        'against_46_60': goals_data_against_minute_46_60_total,
                        'against_61_75': goals_data_against_minute_61_75_total,
                        'against_76_90': goals_data_against_minute_76_90_total,
                        'against_91_105': goals_data_against_minute_91_105_total,
                        'against_106_120': goals_data_against_minute_106_120_total,

                        # New: Favorite lineups
                        'favorite_lineups': lineups_data_0_formation,
                        'favorite_lineups_count': lineups_data_0_played,
                        'secondary_lineups': lineups_data_1_formation,
                        'secondary_lineups_count': lineups_data_1_played,
                    }
                )
                print(f"{'Created' if created else 'Updated'}: {team}")
            except Exception as e:
                print(f"Error saving team: {str(e)}")
        else:
            print("No team data found in the API response.")
    else:
        print(f"Failed to fetch data : {response.status_code}")


#---------------------------------------------------------------------------------------------------------------
def fetch_and_save_matches(request):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"league": "39", "season": "2024"}

    headers = {
        "x-rapidapi-key": "69add1c8a2mshd66c5aa11eccb10p1c1f6bjsnd3f6750e5f0a",
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    matches = response.json()

    for match in matches['response']:
        fixture_data = match['fixture']
        league_data = match['league']
        teams_data = match['teams']
        score_data = match['score']

        # Trích xuất thông tin từ fixture
        match_id = fixture_data['id']
        date = fixture_data['date']
        venue_id = fixture_data['venue']['id']
        venue_name = fixture_data['venue']['name']
        venue_city = fixture_data['venue']['city']
        status = fixture_data['status']['long']
        referee = fixture_data.get('referee', 'Unknown')  # Tránh lỗi nếu referee không có trong dữ liệu

        # Trích xuất thông tin từ league
        league_id = league_data['id']
        league_name = league_data['name']
        country_name = league_data['country']
        season = league_data['season']

        # Trích xuất thông tin từ teams
        home_team_id = teams_data['home']['id']
        away_team_id = teams_data['away']['id']

        home_team_name = teams_data['home']['name']
        away_team_name = teams_data['away']['name']

        # Trích xuất thông tin từ score
        ht_score_data = score_data['halftime']
        ft_score_data = score_data['fulltime']
        et_score_data = score_data['extratime']
        pk_score_data = score_data['penalty']

        ht_home = ht_score_data['home']
        ht_away = ht_score_data['away']
        ft_home = ft_score_data['home']
        ft_away = ft_score_data['away']
        et_home = et_score_data.get('home')  # Xử lý trường hợp extratime là null
        et_away = et_score_data.get('away')
        pk_home = pk_score_data.get('home')
        pk_away = pk_score_data.get('away')

        home_team = Team.objects.get(api_id=home_team_id)
        away_team = Team.objects.get(api_id=away_team_id)
        league_id_new = League.objects.get(api_id=league_id)

        # Cập nhật hoặc tạo mới Match
        Match.objects.update_or_create(
            api_id=match_id,
            defaults={
                'api_id': match_id,
                'season': season,
                'league_id': league_id_new,
                'country_name': country_name,
                'home': home_team,
                'away': away_team,
                'date': date,
                'status': status,
                'referee': referee,
                'venue_id': venue_id,
                'venue_name': venue_name,
                'venue_city': venue_city,
                'ht_home': ht_home,
                'ht_away': ht_away,
                'ft_home': ft_home,
                'ft_away': ft_away,
                'et_home': et_home,
                'et_away': et_away,
                'pk_home': pk_home,
                'pk_away': pk_away,
            }
        )

        # Cập nhật hoặc tạo mới LeagueTeam cho cả đội nhà và đội khách
        LeagueTeam.objects.update_or_create(
            team_id=home_team_id,
            defaults={
                'league_id': league_id_new.id,
                'league_name': league_name,
                'team_id': home_team_id,
                'team_name': home_team_name,
            }
        )

    return HttpResponse("Matches imported successfully.")