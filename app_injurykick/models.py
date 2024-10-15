from django.db import models

# Create your models here.

#---------------------------------------------------------------------------------------------------------------
class Country(models.Model): # request("GET", "/v3/fixtures?league=39&season=2020", headers=headers)
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField cho id tự động tăng
    country_code = models.CharField(max_length=2, unique=True)  # Mã quốc gia, ví dụ "AL"
    country_name = models.CharField(max_length=255)  # Tên quốc gia, ví dụ "Albania"
    country_flag = models.URLField(max_length=500)  # URL của cờ quốc gia

    def __str__(self):
        return self.country_name


#---------------------------------------------------------------------------------------------------------------
class League(models.Model):  # request("GET", "/v3/leagues", headers=headers)
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField cho id tự động tăng
    api_id = models.IntegerField(null=True, blank=True, db_index=True, unique=True)  # ID từ API-FOOTBALL
    name = models.CharField(max_length=255, db_index=True)
    name_custom = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=50)  # Type ('League' or 'Cup')
    type_custom = models.CharField(max_length=50, null=True, blank=True)
    image = models.URLField(blank=True, null=True)
    image_custom = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=255, null=True)
    country_custom = models.CharField(max_length=255, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    country_code_custom = models.CharField(max_length=10, null=True, blank=True)
    country_flag = models.URLField(blank=True, null=True)
    country_flag_custom = models.URLField(blank=True, null=True)
    url_league_trfmt = models.URLField(blank=True, null=True)
    url_league_injury_trfmt = models.URLField(blank=True, null=True)
    url_league_suspend_trfmt = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


#---------------------------------------------------------------------------------------------------------------
class LeagueStanding(models.Model):
    league_id = models.IntegerField()
    league_name = models.CharField(max_length=100)
    country_name = models.CharField(max_length=100)
    season = models.IntegerField()
    rank = models.IntegerField()
    team_id = models.IntegerField()
    team_name = models.CharField(max_length=100)
    logo = models.URLField()
    points = models.IntegerField()
    goals_diff = models.IntegerField()
    played = models.IntegerField(null=True, blank=True)
    win = models.IntegerField(null=True, blank=True)
    draw = models.IntegerField(null=True, blank=True)
    lose = models.IntegerField(null=True, blank=True)
    goals_for = models.IntegerField(null=True, blank=True)
    goals_against = models.IntegerField(null=True, blank=True)
    home_played = models.IntegerField(null=True, blank=True)
    home_win = models.IntegerField(null=True, blank=True)
    home_draw = models.IntegerField(null=True, blank=True)
    home_lose = models.IntegerField(null=True, blank=True)
    home_goals_for = models.IntegerField(null=True, blank=True)
    home_goals_against = models.IntegerField(null=True, blank=True)
    away_played = models.IntegerField(null=True, blank=True)
    away_win = models.IntegerField(null=True, blank=True)
    away_draw = models.IntegerField(null=True, blank=True)
    away_lose = models.IntegerField(null=True, blank=True)
    away_goals_for = models.IntegerField(null=True, blank=True)
    away_goals_against = models.IntegerField(null=True, blank=True)    
    description = models.CharField(max_length=255, null=True, blank=True)
    description_custom = models.CharField(max_length=255, null=True, blank=True)
    description_deduction = models.CharField(max_length=255, null=True, blank=True)
    legend_color = models.CharField(max_length=50, null=True, blank=True)  # Cột màu sắc
    legend_color_custom = models.CharField(max_length=55, null=True, blank=True)
    update_time = models.DateTimeField()

    class Meta:
        unique_together = ('league_id', 'season', 'rank')    


#---------------------------------------------------------------------------------------------------------------
class Team(models.Model):  # request("GET", "/v3/teams?id={33}", headers=headers) . Need to find teamsid from League Standing
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField cho id tự động tăng
    api_id = models.IntegerField( null=True, blank=True, db_index=True, unique=True)  # ID từ API-FOOTBALL
    name = models.CharField(max_length=255, db_index=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=255)
    founded = models.IntegerField(null=True, blank=True)
    image = models.URLField(blank=True, null=True)
    image_custom = models.URLField(blank=True, null=True)
    venue_id = models.IntegerField(null=True, blank=True, db_index=True, unique=True)
    venue_name = models.CharField(max_length=255)
    venue_address = models.CharField(max_length=255, blank=True, null=True)
    venue_city = models.CharField(max_length=255, blank=True, null=True)
    venue_capacity = models.IntegerField(blank=True, null=True)
    venue_surface = models.CharField(max_length=50, blank=True, null=True)
    venue_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


#---------------------------------------------------------------------------------------------------------------
class TeamSeasonStatistics(models.Model):  #request("GET", "/v3/teams/statistics?league={39}&season={2020}&team={33}", headers=headers)
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField cho ID
    team = models.ForeignKey('Team', to_field='api_id', on_delete=models.CASCADE, related_name='season_statistics')
    league = models.ForeignKey('League', to_field='api_id', on_delete=models.CASCADE, related_name='season_statistics')
    season = models.IntegerField(null=True, blank=True)
    # Các thống kê lớn
    biggest_goals_home = models.IntegerField(default=0)
    biggest_goals_away = models.IntegerField(default=0)
    biggest_against_home = models.IntegerField(default=0)
    biggest_against_away = models.IntegerField(default=0)
    biggest_lose_home = models.CharField(max_length=10, null=True, blank=True)  # Ví dụ: "1-6"
    biggest_lose_away = models.CharField(max_length=10, null=True, blank=True)
    
    # Chuỗi trận lớn nhất
    biggest_streak_draws = models.IntegerField(default=0)
    biggest_streak_loses = models.IntegerField(default=0)
    biggest_streak_wins = models.IntegerField(default=0)
    
    # Chiến thắng lớn nhất
    biggest_wins_home = models.CharField(max_length=10, null=True, blank=True)  # Ví dụ: "9-0"
    biggest_wins_away = models.CharField(max_length=10, null=True, blank=True)  # Ví dụ: "1-4"
    
    # Clean sheet và không ghi bàn
    clean_sheet_home = models.IntegerField(default=0)
    clean_sheet_away = models.IntegerField(default=0)
    failed_to_score_home = models.IntegerField(default=0)
    failed_to_score_away = models.IntegerField(default=0)
    
    # Kết quả trận đấu
    draws_away = models.IntegerField(default=0)
    draws_home = models.IntegerField(default=0)
    loses_away = models.IntegerField(default=0)
    loses_home = models.IntegerField(default=0)
    wins_away = models.IntegerField(default=0)
    wins_home = models.IntegerField(default=0)
    played_away = models.IntegerField(default=0)
    played_home = models.IntegerField(default=0)

    # Phong độ gần đây
    form = models.CharField(max_length=10, null=True, blank=True)  # Ví dụ: "LWLWD"
    
    # Tổng số bàn thắng và bị thủng lưới
    goals_total_home = models.IntegerField(default=0)
    goals_total_away = models.IntegerField(default=0)
    against_total_home = models.IntegerField(default=0)
    against_total_away = models.IntegerField(default=0)
    
    # Trung bình bàn thắng và thủng lưới
    goals_avg_home = models.FloatField(default=0.0)
    goals_avg_away = models.FloatField(default=0.0)
    against_avg_home = models.FloatField(default=0.0)
    against_avg_away = models.FloatField(default=0.0)
    
    # Bàn thắng theo thời gian
    goals_0_15 = models.IntegerField(default=0)
    goals_16_30 = models.IntegerField(default=0)
    goals_31_45 = models.IntegerField(default=0)
    goals_46_60 = models.IntegerField(default=0)
    goals_61_75 = models.IntegerField(default=0)
    goals_76_90 = models.IntegerField(default=0)
    goals_91_105 = models.IntegerField(default=0)
    goals_106_120 = models.IntegerField(default=0)
    
    # Bị thủng lưới theo thời gian
    against_0_15 = models.IntegerField(default=0)
    against_16_30 = models.IntegerField(default=0)
    against_31_45 = models.IntegerField(default=0)
    against_46_60 = models.IntegerField(default=0)
    against_61_75 = models.IntegerField(default=0)
    against_76_90 = models.IntegerField(default=0)
    against_91_105 = models.IntegerField(default=0)
    against_106_120 = models.IntegerField(default=0)
    
    # Đội hình yêu thích
    favorite_lineups = models.CharField(max_length=20, null=True, blank=True)  # Ví dụ: "4-2-3-1"
    favorite_lineups_count = models.IntegerField(default=0)
    secondary_lineups = models.CharField(max_length=20, null=True, blank=True)  # Ví dụ: "4-3-1-2"
    secondary_lineups_count = models.IntegerField(default=0)
    
    # Phạt đền
    penalty_missed = models.IntegerField(default=0)
    penalty_scored = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.team.name} - {self.league.name} ({self.id})'


#---------------------------------------------------------------------------------------------------------------
class Match(models.Model):  #request("GET", "/v3/fixtures?league={39}&season={2020}", headers=headers)
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField cho id tự động tăng
    api_id = models.IntegerField(null=True, blank=True, db_index=True, unique=True)  # ID từ API-FOOTBALL
    season = models.IntegerField(null=True, blank=True)
    league_id = models.ForeignKey(League, to_field='api_id', related_name='matches', on_delete=models.CASCADE, unique=False)
    country_name = models.CharField(max_length=255)
    home = models.ForeignKey(Team, to_field='api_id', related_name='home_matches', on_delete=models.CASCADE)
    away = models.ForeignKey(Team, to_field='api_id', related_name='away_matches', on_delete=models.CASCADE)
    date = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=100)
    referee = models.CharField(max_length=255, null=True, blank=True)
    venue_id = models.IntegerField(null=True, blank=True)
    venue_name = models.CharField(max_length=255, null=True, blank=True)
    venue_city = models.CharField(max_length=255, null=True, blank=True)
    ht_home = models.IntegerField(null=True, blank=True)
    ht_away = models.IntegerField(null=True, blank=True)
    ft_home = models.IntegerField(null=True, blank=True)
    ft_away = models.IntegerField(null=True, blank=True)
    et_home = models.IntegerField(null=True, blank=True)
    et_away = models.IntegerField(null=True, blank=True)
    pk_home = models.IntegerField(null=True, blank=True)
    pk_away = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.home} vs {self.away} - {self.league_id}"


#---------------------------------------------------------------------------------------------------------------
class Player(models.Model):  # request("GET", "/v3/players?id={276}&season={2020}", headers=headers)
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField cho id tự động tăng
    api_id = models.IntegerField(null=True, blank=True, db_index=True, unique=True)  # ID từ API-FOOTBALL
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    height = models.CharField(max_length=10, blank=True, null=True)  # e.g., "1.80m"
    position = models.CharField(max_length=50)
    position_transformed = models.CharField(max_length=10, null=True, blank=True)
    image = models.URLField(blank=True, null=True)
    image_custom = models.URLField(blank=True, null=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.name}"
    

#---------------------------------------------------------------------------------------------------------------
class PlayerSeasonStatistics(models.Model):    #request("GET", "/v3/players?league={39}&season={2020}", headers=headers)
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField cho ID
    api_id = models.IntegerField()  # Thêm trường api_id để lưu ID từ API
    player = models.ForeignKey('Player', to_field='api_id', related_name='season_statistics' ,on_delete=models.CASCADE)
    team = models.ForeignKey('Team', to_field='api_id', related_name='player_statistics' ,on_delete=models.CASCADE)
    league = models.ForeignKey('League', to_field='api_id', related_name='player_statistics' ,on_delete=models.CASCADE)
    season = models.IntegerField(null=True, blank=True)

    appearances = models.IntegerField(default=0, null=True, blank=True)
    starting = models.IntegerField(default=0, null=True, blank=True)
    subs_in = models.IntegerField(default=0, null=True, blank=True)
    subs_out = models.IntegerField(default=0, null=True, blank=True)
    bench = models.IntegerField(default=0, null=True, blank=True)
    minutes = models.IntegerField(default=0, null=True, blank=True)
    captain = models.BooleanField(default=False, null=True, blank=True)
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # Điểm trên thang 10
    position = models.CharField(max_length=50, null=True, blank=True)
    position_transformed = models.CharField(max_length=10, null=True, blank=True)

    # Thống kê tấn công
    shots_on = models.IntegerField(default=0, null=True, blank=True)
    shots_total = models.IntegerField(default=0, null=True, blank=True)
    goals = models.IntegerField(default=0, null=True, blank=True)
    conceded = models.IntegerField(default=0, null=True, blank=True)
    assists = models.IntegerField(default=0, null=True, blank=True)
    saves = models.IntegerField(default=0, null=True, blank=True)
    
    # Thống kê chuyền bóng
    passes_total = models.IntegerField(default=0, null=True, blank=True)
    passes_key = models.IntegerField(default=0, null=True, blank=True)
    passes_accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Tỷ lệ chính xác
    
    # Thống kê phòng ngự
    tackles_total = models.IntegerField(default=0, null=True, blank=True)
    blocks = models.IntegerField(default=0, null=True, blank=True)
    interceptions = models.IntegerField(default=0, null=True, blank=True)
    
    # Thống kê tranh chấp và đi bóng
    duels_total = models.IntegerField(default=0, null=True, blank=True)
    duels_won = models.IntegerField(default=0, null=True, blank=True)
    dribbles_attempts = models.IntegerField(default=0, null=True, blank=True)
    dribbles_success = models.IntegerField(default=0, null=True, blank=True)
    dribbles_past = models.IntegerField(default=0, null=True, blank=True)
    
    # Thống kê phạm lỗi
    fouls_drawn = models.IntegerField(default=0, null=True, blank=True)
    fouls_committed = models.IntegerField(default=0, null=True, blank=True)
    
    # Thống kê thẻ phạt
    yellow_card = models.IntegerField(default=0, null=True, blank=True)
    yellowred_card = models.IntegerField(default=0, null=True, blank=True)
    red_card = models.IntegerField(default=0, null=True, blank=True)
    
    # Thống kê phạt đền
    penalty_won = models.IntegerField(default=0, null=True, blank=True)
    penalty_committed = models.IntegerField(default=0, null=True, blank=True)
    penalty_scored = models.IntegerField(default=0, null=True, blank=True)
    penalty_missed = models.IntegerField(default=0, null=True, blank=True)
    penalty_saved = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f'{self.player.name} - {self.team.name} ({self.id})'


#---------------------------------------------------------------------------------------------------------------
class StandingDescription(models.Model): #request("GET", "/v3/standings?league={39}&season={2020}", headers=headers)
    league = models.ForeignKey('League', to_field='api_id', related_name='standing_descriptions', on_delete=models.CASCADE)
    season = models.CharField(max_length=20)  # Ví dụ: '2023-2024'
    rank = models.IntegerField()  # Ví dụ: 1, 2, 3,..., 20
    description = models.CharField(max_length=255, null=True, blank=True)  # Mô tả như "Promotion - Champions League", hoặc null

    def __str__(self):
        return f'League: {self.league.name}, Season: {self.season}, Rank: {self.rank}'

    class Meta:
        unique_together = ('league', 'season', 'rank')  # Đảm bảo mỗi league, season, rank là duy nhất


#---------------------------------------------------------------------------------------------------------------
class StandingDeduction(models.Model):  #Crawling Data to check if whether it have team be deduction points for any reason
    league = models.ForeignKey(League, to_field='api_id', on_delete=models.CASCADE)
    season = models.CharField(max_length=10)  # Ví dụ: "2023-2024"
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='standing_deductions')  # Thêm related_name
    description = models.TextField(null=True, blank=True)
    points_deduction = models.IntegerField(default=0)  # Số điểm bị trừ

    def __str__(self):
        return f"{self.league} - {self.season} - Team: {self.team} - Reason: {self.description} - Points deduction: {self.points_deduction}"


#---------------------------------------------------------------------------------------------------------------
#https://rapidapi.com/people-api-people-api-default/api/football-news11/playground/apiendpoint_7ba472f9-5c31-4342-a378-3fcfd45c7181
class Category(models.Model):
    CATEGORY_CHOICES = [
        (0, "General"),
        (3, "Transfers"),
        (4, "General"),
        (5, "Match Previews"),
        (6, "Featured"),
        (7, "Internationals"),
    ]
    
    id = models.IntegerField(primary_key=True, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.get_id_display()

class News(models.Model):
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField cho ID
    api_id = models.IntegerField(null=True, blank=True)  # Thêm trường api_id để lưu ID từ API
    title = models.CharField(max_length=255)  # Tiêu đề tin tức
    image_url = models.URLField(max_length=200, null=True, blank=True)  # URL hình ảnh
    original_url = models.URLField(max_length=200)  # URL gốc của tin tức
    published_at = models.DateTimeField()  # Ngày giờ phát hành
    categories = models.ManyToManyField(Category, blank=True, default=None)  # Liên kết với Category model

    def __str__(self):
        return self.title


#---------------------------------------------------------------------------------------------------------------
class Sidelined(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)  # Liên kết với model Player
    type = models.CharField(max_length=255)  # Loại chấn thương hoặc lý do bị đình chỉ
    start_date = models.DateField(null=True, blank=True)  # Ngày bắt đầu chấn thương/đình chỉ
    end_date = models.DateField(null=True, blank=True)    # Ngày kết thúc chấn thương/đình chỉ

    def __str__(self):
        return f"{self.player.name} - {self.type} ({self.start_date} to {self.end_date})"

class LastestSidelined(models.Model):
    STATUS_CHOICES = [
        ('injured', 'Injured'),
        ('recovered', 'Recovered'),
    ]

    team_name = models.CharField(max_length=255)
    player_name = models.CharField(max_length=255)
    player_link = models.URLField()
    injury_type = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.CharField(max_length=50, null=True, blank=True)
    end_date = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='injured')

    def __str__(self):
        return f"{self.player_name} ({self.team_name})"

#---------------------------------------------------------------------------------------------------------------











#---------------------------------------------------------------------------------------------------------------

class LeagueTeamLinkTransfermarktData(models.Model):
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField cho id tự động tăng
    league = models.CharField(max_length=255, null=True, blank=True)
    season = models.IntegerField(null=True, blank=True)
    team = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    trfmt_team_id = models.IntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.league} {self.team} {self.link}"

class PlayerTransfermarktData(models.Model):  # request("GET", "/v3/players?id={276}&season={2020}", headers=headers)
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField cho id tự động tăng
    league = models.CharField(max_length=255, null=True, blank=True)
    season = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, db_index=True)
    team = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    position_transformed = models.CharField(max_length=10, null=True, blank=True)
    number = models.CharField(max_length=10, null=True, blank=True)
    market_value = models.DecimalField(max_digits=15, decimal_places=2)
    market_value_cleaned = models.CharField(max_length=255)
    market_value_transformed = models.CharField(max_length=255)
    image = models.URLField(null=True, blank=True)
    player_link = models.URLField(null=True, blank=True)
    trfmt_player_id = models.IntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.name}"

class Injury(models.Model):  # Crawling Data From Soccerway or Transfermarkt
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    league = models.CharField(max_length=255, null=True, blank=True)  # ForeignKey to League model
    player = models.CharField(max_length=255, null=True, blank=True)
    team = models.CharField(max_length=255, null=True, blank=True)   
    injury_type = models.CharField(max_length=255, null=True, blank=True)  # Type of injury
    since = models.DateField(null=True, blank=True)  # Injury start date
    until = models.DateField(null=True, blank=True)  # Expected return date
    injury_or_suspension = models.CharField(max_length=10, null=True, blank=True)  # Injury or Suspension
    trfmt_player_id = models.IntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return f"Injury: {self.player} ({self.injury_type}) - {self.since}"

class TeamMapping(models.Model):
    team_api = models.ForeignKey(Team, to_field='api_id', related_name='team_mapping', on_delete=models.CASCADE)  # Liên kết với model Team
    team_transfermarkt = models.ForeignKey(LeagueTeamLinkTransfermarktData, to_field='trfmt_team_id', related_name='team_mapping', on_delete=models.CASCADE)  # Liên kết với model LeagueTeamLinkTransfermarktData

    def __str__(self):
        return f"{self.team_api.name} <-> {self.team_transfermarkt.team}"

class PlayerMapping(models.Model):
    player_api = models.ForeignKey(Player, to_field='api_id', related_name='player_mapping', on_delete=models.CASCADE)  # Liên kết với model Player
    player_transfermarkt = models.ForeignKey(PlayerTransfermarktData, to_field='trfmt_player_id', related_name='player_mapping', on_delete=models.CASCADE)  # Liên kết với model PlayerTransfermarktData

    def __str__(self):
        return f"{self.player_api.name} <-> {self.player_transfermarkt.name}"

#---------------------------------------------------------------------------------------------------------------
