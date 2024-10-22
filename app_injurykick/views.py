from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *
import http.client
import json, requests, time, html
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

headers_scrape_soccerway = {
    "Referer": "https://int.soccerway.com/",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}
seasons_in_soccerway = ['20242025'] #Soccerway use javascript to load season content. Cannot change url
leagues_id_list = [39, 140, 135, 78, 61]  # ID các giải đấu  39, 140, 135, 78, 61
season_list = [2020, 2021, 2022, 2023]

url_league_sidelined = {
    'https://int.soccerway.com/national/england/premier-league/20242025/regular-season/r81780/sidelined/': 'England Premier League',
    # 'https://int.soccerway.com/national/spain/primera-division/20242025/regular-season/r82318/sidelined/': 'Spain LaLiga',
    # 'https://int.soccerway.com/national/italy/serie-a/20242025/regular-season/r82869/sidelined/': 'Italy Serie A',
    # 'https://int.soccerway.com/national/germany/bundesliga/20242025/regular-season/r81840/sidelined/': 'Germany Bundesliga',
    # 'https://int.soccerway.com/national/france/ligue-1/20242025/regular-season/r81802/sidelined/': 'France Ligue 1',
}

#---------------------------------------------------------------------------------------------------------------
def fetch_and_save_leagues(request): #Just need to call 1 per season
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json().get('response', [])
        
        for item in data:
            # Lấy thông tin giải đấu từ JSON
            league_info = item.get('league', {})
            api_id = league_info.get('id')  # Đây là api_id từ API
            name = league_info.get('name')

            # Lấy hoặc tạo League nếu chưa có, dựa trên api_id
            league, created = League.objects.get_or_create(api_id=api_id, defaults={
                'name': name,
                'type': league_info.get('type'),
                'image': league_info.get('logo'),
                'country': item.get('country', {}).get('name', ''),
                'country_code': item.get('country', {}).get('code', ''),
                'country_flag': item.get('country', {}).get('flag', '')
            })

            # Duyệt qua danh sách các mùa giải trong JSON
            seasons = item.get('seasons', [])
            for season in seasons:
                season_year = season.get('year')
                start_date = season.get('start')
                end_date = season.get('end')
                current_season = season.get('current')

                coverage = season.get('coverage', {})
                fixtures = coverage.get('fixtures', {})
                players = coverage.get('players', False)

                # Lưu thông tin vào LeagueSeason với khóa ngoại là api_id của League
                LeagueSeason.objects.update_or_create(
                    api_id=league,  # Đây là liên kết khóa ngoại qua api_id
                    season_year=season_year,
                    defaults={
                        'start_date': start_date,
                        'end_date': end_date,
                        'current_season': current_season,
                        'fixtures_events': fixtures.get('events', False),
                        'fixtures_lineups': fixtures.get('lineups', False),
                        'fixtures_statistics_fixtures': fixtures.get('statistics_fixtures', False),
                        'fixtures_statistics_players': fixtures.get('statistics_players', False),
                        'standings': coverage.get('standings', False),
                        'players': players,
                        'top_scorers': coverage.get('top_scorers', False),
                        'top_assists': coverage.get('top_assists', False),
                        'top_cards': coverage.get('top_cards', False),
                        'injuries': coverage.get('injuries', False),
                        'predictions': coverage.get('predictions', False),
                        'odds': coverage.get('odds', False),
                    }
                )
        print("Dữ liệu đã được crawling và lưu thành công.")
    else:
        print(f"Lỗi khi gửi yêu cầu API: {response.status_code}")

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
                            team_id = team_id,
                            defaults={
                                'league_name': league_name,
                                'country_name': country_name,
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
        time.sleep(3)  # Thêm thời gian tạm dừng 3 giây giữa mỗi giải đấu (league)

    return HttpResponse("Standings imported successfully.")


#---------------------------------------------------------------------------------------------------------------
def fetch_and_save_teams(request):  
    # Lấy danh sách các đội bóng theo league_id và season
    teams_in_league = LeagueStanding.objects.values('team_id')

    # Gọi API cho từng team và lưu dữ liệu
    for team in teams_in_league:
        team_id = team['team_id']
        print(f"Processing team_id: {team_id}")

        # Kiểm tra xem team với api_id đã tồn tại trong model Team chưa
        try:
            existing_team = Team.objects.get(api_id=team_id)
            print(f"Team with api_id {team_id} already exists, skipping fetch.")
        except Team.DoesNotExist:
            print(f"Team with api_id {team_id} not found, fetching data...")
            # Gọi hàm fetch_and_save_team_info để fetch dữ liệu từ API và lưu vào model Team
            fetch_and_save_team_info(team_id)
        time.sleep(2.5)

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
    for season in season_list:  # Lặp qua từng mùa giải trong season_list
        print(f"Processing season: {season}")
        grouped_data = LeagueStanding.objects.filter(season=season).values('league_id').distinct()

        # Duyệt qua từng mùa giải và giải đấu
        for group in grouped_data:
            league_id = group['league_id']
            print(f"Processing league_id: {league_id} for season: {season}")

            # Lấy danh sách các đội bóng theo league_id và season
            teams_in_league = LeagueStanding.objects.filter(league_id=league_id, season=season).values('team_id')
            print(f"Teams in league {league_id} for season {season}: {list(teams_in_league)}")

            # Gọi API cho từng team và lưu dữ liệu
            for team in teams_in_league:
                team_id = team['team_id']
                print(f"Processing team_id: {team_id} for season: {season}")

                # Kiểm tra xem team_id và season đã tồn tại trong TeamSeasonStatistics chưa
                if not TeamSeasonStatistics.objects.filter(team__api_id=team_id, season=season).exists():
                    print(f"Fetching data for team_id: {team_id}, season: {season}")

                    # Gọi hàm fetch_and_save_team_statistics_data để fetch dữ liệu và lưu
                    fetch_and_save_team_statistics_data(league_id, season, team_id)
                else:
                    print(f"Data for team_id: {team_id}, season: {season} already exists. Skipping...")
                time.sleep(2.5)

            # Tạm dừng giữa mỗi giải đấu (league)
            time.sleep(3)
        time.sleep(3)

    return HttpResponse("Team Statistics imported successfully for all seasons.")

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
    season = 2023
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
            home_team_name = teams_data['home']['name']
            away_team_id = teams_data['away']['id'] #away
            away_team_name = teams_data['away']['name']

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

            try:
                home_team = Team.objects.get(api_id=home_team_id)
            except Team.DoesNotExist:
                print(f"Home team with api_id {home_team_id} team_name {home_team_name} not found, skipping match {match_id}.")
                continue  # Bỏ qua nếu đội bóng không tìm thấy

            try:
                away_team = Team.objects.get(api_id=away_team_id)
            except Team.DoesNotExist:
                print(f"Away team with api_id {away_team_id} team_name {away_team_name} not found, skipping match {match_id}.")
                continue  # Bỏ qua nếu đội bóng không tìm thấy

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

        print(f"League {league_id} processed. Sleeping for 2 seconds...")
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

                     # Xác định position_transformed dựa trên position
                    position = stats['games']['position']
                    position_transformed = ''
                    if position == 'Attacker':
                        position_transformed = 'FW'
                    elif position == 'Defender':
                        position_transformed = 'DF'
                    elif position == 'Midfielder':
                        position_transformed = 'MF'
                    elif position == 'Goalkeeper':
                        position_transformed = 'GK'

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
                            'position_transformed': position_transformed,
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
                            'position_transformed': position_transformed,
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
def fetch_and_save_news(request):  # Limit 10/day
    today = datetime.today().strftime('%Y-%m-%d')
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    url = "https://football-news11.p.rapidapi.com/api/news-by-date"
    querystring_news = {"date": today, "lang": "en", "page": "1"}

    try:
        response = requests.get(url, headers=headers_news, params=querystring_news)
        data = response.json()

        for item in data.get('result', []):
            # Create or update News record
            news, created = NewsData.objects.update_or_create(
                api_id=item['id'],
                defaults={
                    'title': item['title'],
                    'image_url': item.get('image', None),
                    'original_url': item['original_url'],
                    'published_at': datetime.strptime(item['published_at'], '%d-%m-%Y %H:%M:%S'),
                }
            )

            news.save()

        return HttpResponse(f"News data of {yesterday} fetched and saved successfully.")
    
    except requests.exceptions.RequestException as e:
        # Log error and return an error response
        return HttpResponse(f"Failed to fetch news data: {str(e)}", status=500)


#---------------------------------------------------------------------------------------------------------------
def fetch_and_save_sidelined(request):
    # Lấy dữ liệu từ client
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    
    # Kiểm tra xem client yêu cầu scrape nửa đầu hay nửa sau
    scrape_half = body_data.get('scrape_half', 'first')  # Mặc định là nửa đầu nếu không có giá trị

    # Lấy danh sách tất cả các Player có api_id
    players = Player.objects.filter(api_id__isnull=False)
    total_players = players.count()
    
    # Chia player thành nửa đầu và nửa sau
    half_point = total_players // 2
    if scrape_half == 'first':
        # Nửa đầu của danh sách players
        players = players[:half_point]
    else:
        # Nửa sau của danh sách players
        players = players[half_point:]
    
    # Giới hạn của API mỗi phút
    limit_per_minute = 250
    
    # Tính số batch cần thiết
    num_batches = (players.count() // limit_per_minute) + (1 if players.count() % limit_per_minute != 0 else 0)
    
    # Khởi tạo URL API và headers
    url = "https://api-football-v1.p.rapidapi.com/v3/sidelined"

    # Tạo danh sách để lưu trữ kết quả
    results = []

    # Thực hiện request theo batch
    for batch in range(num_batches):
        # Lấy nhóm player cho batch hiện tại
        start_idx = batch * limit_per_minute
        end_idx = start_idx + limit_per_minute
        batch_players = players[start_idx:end_idx]
        
        # Gọi API cho từng Player trong batch
        for player in batch_players:
            querystring = {"player": str(player.api_id)}
            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            # Lưu kết quả vào danh sách
            results.append({
                'player': player.name,
                'data': data.get('response', [])  # lấy thông tin về injury/sidelined
            })

            # Lưu thông tin sidelined vào database
            for sidelined_info in data.get('response', []):
                Sidelined.objects.create(
                    player=player,
                    type=sidelined_info.get('type', ''),
                    start_date=sidelined_info.get('start'),
                    end_date=sidelined_info.get('end')
                )

        # Nếu chưa phải batch cuối cùng, chờ 60 giây trước khi request batch tiếp theo
        if batch < num_batches - 1:
            print(f"Waiting for 60 seconds before next batch ({batch + 1}/{num_batches})...")
            time.sleep(60)  # chờ 60 giây

    # Trả kết quả về template hoặc JSON response
    return HttpResponse('Succesfully fetch and saved!')


#---------------------------------------------------------------------------------------------------------------
def scrape_and_save_sidelined_players(request):
    crawled_data = []
    base_url_sccwa = 'https://int.soccerway.com'
    
    # Fetch data from all the league URLs
    for url, league_name in url_league_sidelined.items():
        response = requests.get(url, headers=headers_scrape_soccerway)
        if response.status_code == 200:
            print(f"Truy cập thành công trang: {league_name}")
            soup = BeautifulSoup(response.content, 'html.parser')
            teams = soup.find_all('tr', class_='group-head')

            for team in teams:
                team_name = team.get_text(strip=True)
                next_row = team.find_next_sibling('tr')
                while next_row and 'sub-head' not in next_row['class']:
                    next_row = next_row.find_next_sibling('tr')

                while next_row and 'group-head' not in next_row['class']:
                    cols = next_row.find_all('td')
                    if cols:
                        player_link = cols[0].find('a')['href']
                        player_name = cols[0].get_text(strip=True)
                        injury_type = cols[1]['title'] if len(cols) > 1 else None
                        start_date = cols[2].get_text(strip=True)
                        end_date = cols[3].get_text(strip=True)
                        
                        # Add player data to the list
                        crawled_data.append({
                            'player': player_name,
                            'team': team_name,
                            'player_link': base_url_sccwa + player_link,
                            'injury_type': injury_type,
                            'start_date': start_date,
                            'end_date': end_date,
                            'league': league_name
                        })
                    next_row = next_row.find_next_sibling('tr')
        else:
            print(f"Không thể truy cập {url}, mã lỗi: {response.status_code}")

    # Update database with the crawled data
    crawl_data(crawled_data)
    return HttpResponse("Success")

def crawl_data(crawled_data):
    # Lấy danh sách các cầu thủ, đội, loại chấn thương và ngày bắt đầu từ dữ liệu đã crawl về
    crawled_entries = {(data['player'], data['team'], data['injury_type'], data['start_date']) for data in crawled_data}

    # Lấy tất cả thông tin chấn thương hiện có trong cơ sở dữ liệu
    existing_injuries = LastestSidelined.objects.all()

    # Tạo tập hợp các mục (cầu thủ, đội, loại chấn thương, ngày bắt đầu) từ cơ sở dữ liệu
    existing_entries = {(injury.player_name, injury.team_name, injury.injury_type, injury.start_date) for injury in existing_injuries}

    # Cập nhật trạng thái cho những cầu thủ đã hồi phục (không còn xuất hiện trong dữ liệu mới)
    for injury in existing_injuries:
        if (injury.player_name, injury.team_name, injury.injury_type, injury.start_date) not in crawled_entries:
            injury.status = 'recovered'
            injury.save()

    # Xử lý dữ liệu vừa crawled
    for data in crawled_data:
        player_name = data['player'].replace("'", "&apos;")
        team_name = data['team']
        injury_type = data['injury_type']
        start_date = data['start_date']
        end_date = data['end_date']
        player_link=data['player_link']
        
        # Sử dụng tên đã chuẩn hóa để tìm cầu thủ trong cơ sở dữ liệu không phân biệt chữ hoa chữ thường
        players = Player.objects.filter(name__iexact=player_name)

        if not players.exists():
            print(f"Cầu thủ không tồn tại: {player_name}")
            continue  # Bỏ qua nếu cầu thủ không tồn tại

        if players.count() > 1:
            # Nếu có nhiều hơn một cầu thủ, xử lý từng cầu thủ
            found_player = None
            for player in players:
                response = requests.get(player_link, headers=headers_scrape_soccerway)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    first_name_tag = soup.find('dd', {'data-first_name': True})
                    if first_name_tag:
                        first_name_from_web = first_name_tag.text.strip().lower()
                        if first_name_from_web == player.first_name.lower():
                            found_player = player
                            break  # Dừng vòng lặp nếu tìm thấy cầu thủ khớp
                else:
                    print(f"Lỗi khi truy cập {player_link}: {response.status_code}")
        else:
            found_player = players.first()

        if not found_player:
            print(f"Không tìm thấy cầu thủ nào khớp với tên: {player_name}")
            continue

        player_instance = found_player

        # Kiểm tra xem chấn thương này đã tồn tại hay chưa
        try:
            injury = LastestSidelined.objects.get(
                player_name=player_name,
                api_id=player_instance,
                team_name=team_name,
                injury_type=injury_type,
                start_date=start_date
            )
            # Nếu tìm thấy, cập nhật thông tin
            injury.end_date = end_date
            injury.status = 'injured'
            injury.save()
        except LastestSidelined.DoesNotExist:
            # Nếu không tìm thấy, tạo mới
            injury = LastestSidelined.objects.create(
                api_id=player_instance,
                player_name=player_name,
                team_name=team_name,
                player_link=player_link,
                injury_type=injury_type,
                start_date=start_date,
                end_date=end_date,
                status='injured'
            )
            injury.save()


#---------------------------------------------------------------------------------------------------------------
def scrape_and_save_transfers(request):

    base_url_scw = 'https://int.soccerway.com'

    base_urls = {
        'https://int.soccerway.com/national/england/premier-league/20242025/regular-season/r81780/transfers/': 39,
        'https://int.soccerway.com/national/spain/primera-division/20242025/regular-season/r82318/transfers/': 140,
        'https://int.soccerway.com/national/italy/serie-a/20242025/regular-season/r82869/transfers/': 135,
        'https://int.soccerway.com/national/germany/bundesliga/20242025/regular-season/r81840/transfers/': 78,
        'https://int.soccerway.com/national/france/ligue-1/20242025/regular-season/r81802/transfers/': 61,
    }

    for season in seasons_in_soccerway:
        season_year = season[:4]
        for url, league_api_id in base_urls.items():
            # Thay thế season hiện tại vào url
            updated_url = url.replace('/20242025/', f'/{season}/')

            response = requests.get(updated_url, headers=headers_scrape_soccerway)
            soup = BeautifulSoup(response.content, 'html.parser')
            transfers_table = soup.find('table', class_='transfers')

            current_team = ''
            current_direction = ''

            for row in transfers_table.find_all('tr'):
                if 'group-head' in row.get('class', []):  # Hàng tên đội
                    current_team = row.find('h3').text.strip()
                elif 'subgroup-head' in row.get('class', []):  # Hàng 'Transfers in' hoặc 'Transfers out'
                    current_direction = 'In' if 'Transfers in' in row.text else 'Out'
                else:  # Hàng dữ liệu cầu thủ
                    columns = row.find_all('td')
                    if len(columns) == 4:
                        date_str = columns[0].text.strip()
                        player = columns[1].text.strip()
                        from_team_element = columns[2].find('a')
                        transfer_type = columns[3].text.strip()

                        # Lấy thêm link và title của team
                        from_team = from_team_element.text.strip()
                        from_team_link = base_url_scw + from_team_element['href']
                        from_team_title = from_team_element['title']

                        # Chuyển đổi chuỗi ngày thành đối tượng date
                        date = datetime.strptime(date_str, '%d/%m/%y').date()

                        try:
                            league = League.objects.get(api_id=league_api_id)

                            # Lưu dữ liệu vào model
                            transfer = Transfer(
                                league=league,  # Sử dụng đối tượng League
                                team=current_team,
                                player=player,
                                date=date,
                                direction=current_direction,
                                from_team=from_team,
                                from_team_link=from_team_link,
                                from_team_title=from_team_title,
                                transfer_type=transfer_type,
                                season=season_year  # Lưu năm đầu tiên của mùa giải
                            )
                            transfer.save()

                            print(f"Saved transfer: {player} ({league_api_id}, {season_year})")

                        except League.DoesNotExist:
                            print(f"League with api_id {league_api_id} does not exist.")


                        print(f"Saved transfer: {player} ({league.name}, {season})")
            time.sleep(2)

        print(f"Finished season {season_year}, waiting 5 seconds before starting the next season...")
        time.sleep(5)
    return HttpResponse("Success")
                





#---------------------------------------------------------------------------------------------------------------
def update_legend_colors(request): #FOR STANDINGS TABLE DESCRIPTION
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
    
def convert_date(date_string):
    try:
        # Parse the date in 'MMM DD, YYYY' format and convert to 'YYYY-MM-DD'
        return datetime.strptime(date_string, '%b %d, %Y').strftime('%Y-%m-%d')
    except ValueError:
        return None  # Return None if the date format is invalid
#----