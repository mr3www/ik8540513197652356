from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *
import http.client
import json, requests, time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Create your views here.
# Đặt headers cho API
headers = {
	"x-rapidapi-key": "69add1c8a2mshd66c5aa11eccb10p1c1f6bjsnd3f6750e5f0a",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

headers_news = {
    "x-rapidapi-key": "69add1c8a2mshd66c5aa11eccb10p1c1f6bjsnd3f6750e5f0a",
	"x-rapidapi-host": "football-news11.p.rapidapi.com"
}

headers_scrape_transfermarkt = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

leagues_id_list = [39]  # ID các giải đấu , 140, 135, 78, 61
season_list = [2024]

url_league_map_transfermarkt = {
        'https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1': 'Italy Serie A',
        'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1': 'England Premier League',
        'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1': 'Spain LaLiga',
        'https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1': 'Germany Bundesliga',
        'https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1': 'France Ligue 1',
    }

#---------------------------------------------------------------------------------------------------------------
def fetch_and_save_leagues(request): #Just need to call 1 per season
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
def fetch_and_save_standings(request): # Change the code on the Top to get more leagues (leagues_id_list, season_list)
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
                        description = team_standing['description']
                        update_time = team_standing['update']
                        
                        all_stats = team_standing['all']
                        played = all_stats['played']
                        win = all_stats['win']
                        draw = all_stats['draw']
                        lose = all_stats['lose']
                        goals_for = all_stats['goals']['for']
                        goals_against = all_stats['goals']['against']

                        home_stats = team_standing['home']
                        home_played = home_stats['played']
                        home_win = home_stats['win']
                        home_draw = home_stats['draw']
                        home_lose = home_stats['lose']
                        home_goals_for = home_stats['goals']['for']
                        home_goals_against = home_stats['goals']['against']

                        away_stats = team_standing['away']
                        away_played = away_stats['played']
                        away_win = away_stats['win']
                        away_draw = away_stats['draw']
                        away_lose = away_stats['lose']
                        away_goals_for = away_stats['goals']['for']
                        away_goals_against = away_stats['goals']['against']

                        deduction_value = points - ((win * 3) + draw)
                        if deduction_value >= 0:
                            description_deduction = None
                        else:
                            description_deduction = f"{deduction_value} Points"

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
                                'home_played': home_played,
                                'home_win': home_win,
                                'home_draw': home_draw,
                                'home_lose': home_lose,
                                'home_goals_for': home_goals_for,
                                'home_goals_against': home_goals_against,
                                'away_played': away_played,
                                'away_win': away_win,
                                'away_draw': away_draw,
                                'away_lose': away_lose,
                                'away_goals_for': away_goals_for,
                                'away_goals_against': away_goals_against,
                                'description': description,
                                'description_deduction': description_deduction,
                                'update_time': update_time,
                            }
                        )
        time.sleep(5)  # Thêm thời gian tạm dừng 2 giây giữa mỗi giải đấu (league)

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

    time.sleep(5)  # Thêm thời gian tạm dừng 2 giây giữa mỗi giải đấu (league)

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
def fetch_and_save_teams_statistic(request):  # Client need add dropdown select season before fetch team data.
    season = 2024
    grouped_data = LeagueStanding.objects.filter(season=season).values('league_id').distinct()

    # Duyệt qua từng mùa giải và giải đấu
    for group in grouped_data:
        league_id = group['league_id']
        print(f"Processing league_id: {league_id}")

        # Lấy danh sách các đội bóng theo league_id và season
        teams_in_league = LeagueStanding.objects.filter(league_id=league_id).values('team_id')
        print(f"Teams in league {league_id}: {list(teams_in_league)}")  # In ra danh sách đội

        # Gọi API cho từng team và lưu dữ liệu
        for team in teams_in_league:
            team_id = team['team_id']
            print(f"Processing team_id: {team_id}")

            # Gọi hàm fetch_and_save_team_data để gọi API và lưu dữ liệu vào model Team
            # fetch_and_save_team_statistics_data(league_id, season, team_id)
        time.sleep(5)  # Thêm thời gian tạm dừng 2 giây giữa mỗi giải đấu (league)

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

            # Lưu hoặc cập nhật dữ liệu team vào cơ sở dữ liệu
            try:
                team_instance = Team.objects.get(api_id=team_data['id'])
                league_instance = League.objects.get(api_id=league_data['id'])
                team, created = TeamSeasonStatistics.objects.update_or_create(
                    team=team_instance,  # Ensure this matches the field name in your model
                    league=league_instance,
                    defaults={
                        'team': team_instance,
                        'league': league_instance,
                        'season': season,
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
                        'goals_0_15': goals_data_for_minute_0_15_total if goals_data_for_minute_0_15_total is not None else 0,
                        'goals_16_30': goals_data_for_minute_16_30_total if goals_data_for_minute_16_30_total is not None else 0,
                        'goals_31_45': goals_data_for_minute_31_45_total if goals_data_for_minute_31_45_total is not None else 0,
                        'goals_46_60': goals_data_for_minute_46_60_total if goals_data_for_minute_46_60_total is not None else 0,
                        'goals_61_75': goals_data_for_minute_61_75_total if goals_data_for_minute_61_75_total is not None else 0,
                        'goals_76_90': goals_data_for_minute_76_90_total if goals_data_for_minute_76_90_total is not None else 0,
                        'goals_91_105': goals_data_for_minute_91_105_total if goals_data_for_minute_91_105_total is not None else 0,
                        'goals_106_120': goals_data_for_minute_106_120_total if goals_data_for_minute_106_120_total is not None else 0,
                        
                        'against_0_15': goals_data_against_minute_0_15_total if goals_data_against_minute_0_15_total is not None else 0,
                        'against_16_30': goals_data_against_minute_16_30_total if goals_data_against_minute_16_30_total is not None else 0,
                        'against_31_45': goals_data_against_minute_31_45_total if goals_data_against_minute_31_45_total is not None else 0,
                        'against_46_60': goals_data_against_minute_46_60_total if goals_data_against_minute_46_60_total is not None else 0,
                        'against_61_75': goals_data_against_minute_61_75_total if goals_data_against_minute_61_75_total is not None else 0,
                        'against_76_90': goals_data_against_minute_76_90_total if goals_data_against_minute_76_90_total is not None else 0,
                        'against_91_105': goals_data_against_minute_91_105_total if goals_data_against_minute_91_105_total is not None else 0,
                        'against_106_120': goals_data_against_minute_106_120_total if goals_data_against_minute_106_120_total is not None else 0,

                        # New: Favorite lineups
                        'favorite_lineups': lineups_data_0_formation,
                        'favorite_lineups_count': lineups_data_0_played if lineups_data_0_played != '' else 0,
                        'secondary_lineups': lineups_data_1_formation,
                        'secondary_lineups_count': lineups_data_1_played if lineups_data_1_played != '' else 0,
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
def fetch_and_save_matches(request):  # Client need add dropdown select season before fetch team data.
    season = 2024
    grouped_data = LeagueStanding.objects.filter(season=season).values('league_id').distinct()

    for group in grouped_data:
        league_id = group['league_id']
        print(f"Processing league_id: {league_id} , season {season}")

        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        querystring = {"league": league_id, "season": season}

        response = requests.get(url, headers=headers, params=querystring)
        matches = response.json()

        for match in matches['response']:
            fixture_data = match['fixture']
            league_data = match['league']
            teams_data = match['teams']
            score_data = match['score']

            # Trích xuất thông tin từ fixture
            match_id = fixture_data['id'] # api_id
            date = fixture_data['date'] #date
            venue_id = fixture_data['venue']['id'] #venue_id
            venue_name = fixture_data['venue']['name'] #venue_name
            venue_city = fixture_data['venue']['city'] #venue_city
            status = fixture_data['status']['short'] #status
            referee = fixture_data.get('referee', 'Unknown') #referee  # Tránh lỗi nếu referee không có trong dữ liệu

            # Trích xuất thông tin từ league
            league_id = league_data['id'] #league_id
            country_name = league_data['country'] #country_name
            season = league_data['season'] #season

            # Trích xuất thông tin từ teams
            home_team_id = teams_data['home']['id'] #home
            away_team_id = teams_data['away']['id'] #away

            # Trích xuất thông tin từ score
            ht_score_data = score_data['halftime']
            ft_score_data = score_data['fulltime']
            et_score_data = score_data['extratime']
            pk_score_data = score_data['penalty']

            ht_home = ht_score_data['home'] #ht_home
            ht_away = ht_score_data['away'] #ht_away
            ft_home = ft_score_data['home'] #ft_home
            ft_away = ft_score_data['away'] #ft_away
            et_home = et_score_data.get('home') #et_home  # Xử lý trường hợp extratime là null
            et_away = et_score_data.get('away') #et_away
            pk_home = pk_score_data.get('home') #pk_home
            pk_away = pk_score_data.get('away') #pk_away

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

        print(f"League {league_id} processed. Sleeping for 10 seconds...")
        time.sleep(2)  # Thêm thời gian tạm dừng 2 giây giữa mỗi giải đấu (league)

    return HttpResponse("Matches imported successfully.")


#---------------------------------------------------------------------------------------------------------------
def fetch_and_save_players(request):  # Client need add dropdown select season before fetch team data.
    season = 2024
    grouped_data = LeagueStanding.objects.filter(season=season).values('league_id').distinct()

    # Duyệt qua từng mùa giải và giải đấu
    for group in grouped_data:
        league_id = group['league_id']
        print(f"Processing league_id: {league_id}, season {season}")
        teams_in_league = LeagueStanding.objects.filter(league_id=league_id).values('team_id')
        print(f"Teams in league {league_id}: {list(teams_in_league)}")  # In ra danh sách đội

        # # Gọi API cho từng team và lưu dữ liệu
        for team in teams_in_league:
            team_id = team['team_id']
            print(f"Processing players from team_id: {team_id}")

            url = "https://api-football-v1.p.rapidapi.com/v3/players"

            all_players = []
            current_page = 1

            while True:
                querystring = {"team": team_id, "season": season, "page": current_page}
                response = requests.get(url, headers=headers, params=querystring)
                data = response.json()

                if 'response' not in data or not data['response']:
                    break

                players_data = data['response']
                all_players.extend(players_data)

                for player_data in players_data:
                    player_info = player_data['player']
                    stats = player_data['statistics'][0]

                    # Save player information
                    player, created = Player.objects.update_or_create(
                        api_id=player_info['id'],
                        defaults={
                            'api_id': player_info['id'],
                            'name': player_info['name'],
                            'first_name': player_info['firstname'],
                            'last_name': player_info['lastname'],
                            'date_of_birth': player_info['birth']['date'],
                            'nationality': player_info['nationality'],
                            'height': player_info['height'],
                            'position': stats['games']['position'],
                            'image': player_info['photo']
                        }
                    )

                    # Get or create team and league
                    team, _ = Team.objects.get_or_create(api_id=stats['team']['id'], defaults={'name': stats['team']['name']})
                    league, _ = League.objects.get_or_create(api_id=stats['league']['id'], defaults={'name': stats['league']['name']})

                    # Save player statistics
                    PlayerSeasonStatistics.objects.update_or_create(
                        api_id=player_info['id'],
                        player=player,
                        team=team,
                        league=league,
                        season=season,
                        defaults={
                            'api_id': player_info['id'],
                            'appearances': stats['games'].get('appearences', 0),  # Đặt giá trị mặc định 0 nếu không tồn tại
                            'starting': stats['games'].get('lineups', 0),
                            'subs_in': stats['substitutes'].get('in', 0),
                            'subs_out': stats['substitutes'].get('out', 0),
                            'bench': stats['substitutes'].get('bench', 0),
                            'minutes': stats['games'].get('minutes', 0),
                            'captain': stats['games'].get('captain', False),  # Đặt mặc định False cho captain nếu không có dữ liệu
                            'rating': stats['games'].get('rating', None),  # Rating có thể là None
                            'position': stats['games'].get('position', ''),
                            'shots_on': stats['shots'].get('on', 0),
                            'shots_total': stats['shots'].get('total', 0),
                            'goals': stats['goals'].get('total', 0),
                            'conceded': stats['goals'].get('conceded', 0),
                            'assists': stats['goals'].get('assists', 0),
                            'saves': stats['goals'].get('saves', 0),
                            'passes_total': stats['passes'].get('total', 0),
                            'passes_key': stats['passes'].get('key', 0),
                            'passes_accuracy': stats['passes'].get('accuracy', 0.0),
                            'tackles_total': stats['tackles'].get('total', 0),
                            'blocks': stats['tackles'].get('blocks', 0),
                            'interceptions': stats['tackles'].get('interceptions', 0),
                            'duels_total': stats['duels'].get('total', 0),
                            'duels_won': stats['duels'].get('won', 0),
                            'dribbles_attempts': stats['dribbles'].get('attempts', 0),
                            'dribbles_success': stats['dribbles'].get('success', 0),
                            'dribbles_past': stats['dribbles'].get('past', 0),
                            'fouls_drawn': stats['fouls'].get('drawn', 0),
                            'fouls_committed': stats['fouls'].get('committed', 0),
                            'yellow_card': stats['cards'].get('yellow', 0),
                            'yellowred_card': stats['cards'].get('yellowred', 0),
                            'red_card': stats['cards'].get('red', 0),
                            'penalty_won': stats['penalty'].get('won', 0),
                            'penalty_committed': stats['penalty'].get('commited', 0),  # Chú ý: Lỗi chính tả 'commited'
                            'penalty_scored': stats['penalty'].get('scored', 0),
                            'penalty_missed': stats['penalty'].get('missed', 0),
                            'penalty_saved': stats['penalty'].get('saved', 0),
                        }
                    )
                print(f"Page {current_page} of {data['paging']['total']} fetched successfully.")
                if current_page == data['paging']['total']:
                    break

                current_page += 1

            print(f"League {league_id}, season {season}, total players fetched: {len(all_players)}")

            time.sleep(10) # Sleep between each team call API
            # for player_data in all_players:
            #     print(f"{player_data['player']['id']} & {player_data['player']['name']} & {player_data['player']['age']}")

    return HttpResponse("Team Statistics imported successfully.")


#---------------------------------------------------------------------------------------------------------------
def fetch_and_save_news(request): #Limit 10/day
    today = datetime.today().strftime('%Y-%m-%d')
    url = "https://football-news11.p.rapidapi.com/api/news-by-date"
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    querystring_news = {"date": "2024-10-12", "lang": "en", "page": "1"}

    response = requests.get(url, headers=headers_news, params=querystring_news)
    data = response.json()

    if not data['result']:
        print("No news data returned from the API.")
        return HttpResponse("No news data returned from the API.")

    for item in data['result']:
        # Kiểm tra nếu 'categories' tồn tại và không rỗng
        if not item.get('categories', []):
            print("News from date not exist, please try again once API updated!")
            return HttpResponse("News from date not exist, please try again once API updated!")

        # Tạo hoặc cập nhật bản ghi News
        news, created = News.objects.update_or_create(
            api_id=item['id'],
            defaults={
                'title': item['title'],
                'image_url': item.get('image', None),
                'original_url': item['original_url'],
                'categories': item['categories'][0],
                'published_at': datetime.strptime(item['published_at'], '%d-%m-%Y %H:%M:%S'),
            }
        )

    return HttpResponse(f"News data of {yesterday} fetched and saved successfully.")


#---------------------------------------------------------------------------------------------------------------
def scrape_team_link(request):
        base_url = 'https://www.transfermarkt.com'
        for url, league in url_league_map_transfermarkt.items():
            for season in season_list:
                print(f"Đang xử lý team link cho giải đấu: {league}, mùa giải: {season}")
                response = requests.get(url, headers=headers_scrape_transfermarkt)

                if response.status_code != 200:
                    print(f"Không thể truy cập {url}, bỏ qua...")
                    continue

                soup = BeautifulSoup(response.content, 'html.parser')

                # Tìm bảng dữ liệu
                table = soup.find('table', class_='items')

                if table is None:
                    print(f"Không tìm thấy bảng dữ liệu tại {url}, bỏ qua...")
                    continue

                for row in table.find('tbody').find_all('tr', class_=['odd', 'even']):
                    team = row.find('td', class_='hauptlink').find('a').text.strip()
                    team_link = row.find('td', class_='hauptlink').find('a')['href']
                    team_link = base_url + team_link.replace('startseite', 'kader')
                    team_link = '/'.join(team_link.split('/')[:-1]) + f"/{season}/plus/1"
                    img_tag = row.find('td', class_='zentriert no-border-rechts').find('img')
                    image = img_tag['src'] if img_tag else None
                    if image:
                        image = image.replace('tiny', 'head')
                        # Lấy ID từ tên file hình ảnh (ví dụ: "281.png")
                        team_image_id = image.split('/')[-1].split('.')[0]  # Lấy "281" từ "281.png"
                    else:
                        team_image_id = None
                    LeagueTeamLinkTransfermarktData.objects.update_or_create(
                        league=league,
                        season=season,
                        team=team,
                        defaults={'link': team_link,'image': image, 'trfmt_team_id': team_image_id}
                        )
        return HttpResponse(f"Transfermarkt Team Link Data crawling & saved successfully.")

def scrape_team_details(team_link, team_name, league_name):
    print(f"Đang xử lý đội bóng: {team_name} ({league_name})")
    response = requests.get(team_link, headers=headers)
    
    # Kiểm tra xem truy cập thành công không
    if response.status_code != 200:
        print(f"Không thể truy cập {team_link}, bỏ qua...")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Tìm bảng dữ liệu cầu thủ
    table = soup.find('table', class_='items')
    
    # Nếu không tìm thấy bảng thì trả về danh sách rỗng
    if table is None:
        print(f"Không tìm thấy bảng dữ liệu tại {team_link}, bỏ qua...")
        return []

    players_data = []

    # Duyệt qua các hàng trong bảng dữ liệu
    for row in table.find('tbody').find_all('tr', class_=['odd', 'even']):
        player = row.find('td', class_='hauptlink').find('a').text.strip()  # Lấy tên cầu thủ
        player_pos = row.find('table', class_='inline-table').find_all('tr')[1].text.strip()  # Lấy vị trí cầu thủ
        
        player_number = row.find('div', class_='rn_nummer').text.strip() if row.find('div', class_='rn_nummer') else None
        
        if player_number == "-":
            player_number = None  # Nếu số áo là "-", gán giá trị None
        elif not player_number.isdigit():  # Nếu không phải là số, gán giá trị None
            player_number = None
            
        market_value = row.find('td', class_='rechts').text.strip()  # Lấy giá trị cầu thủ

        # Hàm chuyển đổi giá trị thị trường
        def convert_market_value(value):
            if value == '-':
                return 0
            value = value.replace('€', '')  # Loại bỏ ký hiệu €
            if value[-1] == 'm':
                return float(value[:-1]) * 1_000_000  # Chuyển đổi từ triệu sang số nguyên
            elif value[-1] == 'k':
                return float(value[:-1]) * 1_000  # Chuyển đổi từ nghìn sang số nguyên
            else:
                return float(value)  # Trường hợp không có 'm' hoặc 'k', giả sử là số trực tiếp
            
        market_value_transformed = convert_market_value(market_value)
        market_value_cleaned = market_value.replace('€', '')

        # Tìm hình ảnh cầu thủ
        player_image_tag = row.find('img', class_='bilderrahmen-fixed')
        player_image = player_image_tag['data-src'] if player_image_tag else None
        
        # Lưu cầu thủ vào cơ sở dữ liệu
        player_data, created = PlayerTransfermarktData.objects.update_or_create(
            name=player,
            team=team_name,
            league=league_name,
            position=player_pos,
            defaults={
                'number': player_number,
                'market_value': market_value_transformed,
                'market_value_cleaned': market_value_cleaned,
                'market_value_transformed': market_value_transformed,
                'image': player_image
            }
        )







#---------------------------------------------------------------------------------------------------------------
def update_legend_colors(request):
    # Định nghĩa màu sắc tương ứng với thứ tự
    color_map = {
        1: "#28a745",  # Màu cho thứ tự đầu tiên (Xanh lá)
        2: "#000080",  # Màu cho thứ hai trung tính (Xanh dương đậm)
        3: "#6f42c1",  # Màu ch thứ ba trung tính (Tím)
        4: "#4682b4",  # Màu cho thứ tư trung tính (Xanh navy)
        5: "#99709b70", # Màu cho thứ 5 trung tính (Tím nhạt)
        6: "#ffa90670", # Màu cho thứ 6 trung tính (Màu cam nhạt)
        7: "#ffc106",  # Màu cho thứ 7 trung tính (Màu cam)
        8: "#f33c59",  # Màu cho thứ tự cuối cùng (Đỏ)
    }

    # Lấy tất cả các league_id và season duy nhất
    leagues_and_seasons = LeagueStanding.objects.values('league_id', 'season').distinct()

    # Duyệt qua từng league_id và season
    for item in leagues_and_seasons:
        league_id = item['league_id']
        season = item['season']

        # Lấy tất cả các standings cho league và season cụ thể
        standings = LeagueStanding.objects.filter(league_id=league_id, season=season)

        # Lấy danh sách các description duy nhất (bỏ qua null) và sắp xếp theo thứ tự
        descriptions = list(
            standings.filter(description__isnull=False)  # Lọc ra các description không null
            .values_list('description', flat=True)
            .distinct()
        )

        # Tạo một từ điển ánh xạ từ description sang thứ tự
        description_order = {desc: idx + 1 for idx, desc in enumerate(descriptions)}

        # Tìm thứ tự cuối cùng (có thể là thứ tự lớn nhất trong description_order)
        last_order = len(description_order)

        # Duyệt qua tất cả các standing và gán màu sắc tương ứng
        for standing in standings:
            if standing.description is None:
                # Nếu description là null, gán legend_color là null
                standing.legend_color = None
            else:
                # Gán màu sắc theo thứ tự nếu có description
                order = description_order.get(standing.description)
                if order:
                    standing.legend_color = color_map.get(order, None)  # Gán màu sắc từ color_map theo thứ tự

                    # Nếu là thứ tự cuối cùng, áp dụng màu đỏ
                    if order == last_order:
                        standing.legend_color = color_map[8]  # Gán màu cho thứ tự cuối cùng
                else:
                    standing.legend_color = None  # Nếu không có thứ tự hoặc màu sắc không xác định

            standing.save()  # Lưu lại thay đổi

    return HttpResponse("Update Done")