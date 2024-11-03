from django.db import models

# Create your models here.

#---------------------------------------------------------------------------------------------------------------
class Country(models.Model): # request("GET", "/v3/fixtures?league=39&season=2020", headers=headers)
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField cho id tự động tăng
    country_code = models.CharField(max_length=2, unique=True)  # Mã quốc gia, ví dụ "AL"
    country_name = models.CharField(max_length=255)  # Tên quốc gia, ví dụ "Albania"
    country_flag = models.URLField(max_length=500)  # URL của cờ quốc gia
    created_at = models.DateTimeField(auto_now_add=True)

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


#---------------------------------------------------------------------------------------------------------------
class LeagueSeason(models.Model):
    api_id = models.ForeignKey(League, to_field='api_id', on_delete=models.CASCADE)  # Liên kết với League thông qua api_id
    season_year = models.IntegerField()  # Năm của mùa giải
    start_date = models.DateField()  # Ngày bắt đầu mùa giải
    end_date = models.DateField()  # Ngày kết thúc mùa giải
    current_season = models.BooleanField(default=False)  # Mùa giải hiện tại hay không

    # Các thông tin về độ phủ sóng của mùa giải
    fixtures_events = models.BooleanField(default=False)
    fixtures_lineups = models.BooleanField(default=False)
    fixtures_statistics_fixtures = models.BooleanField(default=False)
    fixtures_statistics_players = models.BooleanField(default=False)
    standings = models.BooleanField(default=False)
    players = models.BooleanField(default=False)
    top_scorers = models.BooleanField(default=False)
    top_assists = models.BooleanField(default=False)
    top_cards = models.BooleanField(default=False)
    injuries = models.BooleanField(default=False)
    predictions = models.BooleanField(default=False)
    odds = models.BooleanField(default=False)

    class Meta:
        unique_together = ('api_id', 'season_year')  # Đảm bảo mỗi mùa giải chỉ xuất hiện một lần cho mỗi giải đấu

    def __str__(self):
        return f"{self.api_id.name} - Season {self.season_year}"


#---------------------------------------------------------------------------------------------------------------
class LeagueStanding(models.Model):
    league_id = models.ForeignKey(League, on_delete=models.CASCADE, to_field='api_id')
    league_name = models.CharField(max_length=100)
    country_name = models.CharField(max_length=100)
    season = models.IntegerField()
    rank = models.IntegerField()
    team_id = models.IntegerField()
    team_name = models.CharField(max_length=100)
    logo = models.URLField()
    points = models.IntegerField()
    goals_diff = models.IntegerField()
    group = models.CharField(max_length=255, null=True, blank=True)
    form = models.CharField(max_length=50, null=True, blank=True)
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
    update_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    

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
    venue_id = models.IntegerField(null=True, blank=True, db_index=True, unique=False)
    venue_name = models.CharField(max_length=255)
    venue_address = models.CharField(max_length=255, blank=True, null=True)
    venue_city = models.CharField(max_length=255, blank=True, null=True)
    venue_capacity = models.IntegerField(blank=True, null=True)
    venue_surface = models.CharField(max_length=50, blank=True, null=True)
    venue_image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.team.name} - {self.league.name} ({self.id})'


#---------------------------------------------------------------------------------------------------------------
class Match(models.Model):  #request("GET", "/v3/fixtures?league={39}&season={2020}", headers=headers)
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField cho id tự động tăng
    api_id = models.IntegerField(null=True, blank=True, db_index=True, unique=True)  # ID từ API-FOOTBALL
    season = models.IntegerField(null=True, blank=True)
    round = models.CharField(max_length=255, null=True, blank=True)
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
    created_at = models.DateTimeField(auto_now_add=True)
    away_next = models.IntegerField(null=True, blank=True) 
    home_next = models.IntegerField(null=True, blank=True)  

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
    created_at = models.DateTimeField(auto_now_add=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def clean_name(self):
        return self.name.replace("&apos;", "'")

    def __str__(self):
        return f"{self.name}"

    
#-----------------------------------------------------------------------------------------------------------
class PlayerSeasonStatistics(models.Model):    #request("GET", "/v3/players?league={39}&season={2020}", headers=headers)
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField cho ID
    api_id = models.IntegerField()  # Thêm trường api_id để lưu ID từ API
    player = models.ForeignKey('Player', to_field='api_id', related_name='season_statistics' ,on_delete=models.CASCADE)
    team = models.ForeignKey('Team', to_field='api_id', related_name='player_statistics' ,on_delete=models.CASCADE)
    league = models.ForeignKey('League', to_field='api_id', related_name='player_statistics' ,on_delete=models.CASCADE)
    season = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, default="Current")

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.player.name} - {self.team.name} ({self.id})'


#---------------------------------------------------------------------------------------------------------------
class StandingDescription(models.Model): #request("GET", "/v3/standings?league={39}&season={2020}", headers=headers)
    league = models.ForeignKey('League', to_field='api_id', related_name='standing_descriptions', on_delete=models.CASCADE)
    season = models.CharField(max_length=20)  # Ví dụ: '2023-2024'
    rank = models.IntegerField()  # Ví dụ: 1, 2, 3,..., 20
    description = models.CharField(max_length=255, null=True, blank=True)  # Mô tả như "Promotion - Champions League", hoặc null
    created_at = models.DateTimeField(auto_now_add=True)

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.league} - {self.season} - Team: {self.team} - Reason: {self.description} - Points deduction: {self.points_deduction}"


#---------------------------------------------------------------------------------------------------------------
#https://rapidapi.com/people-api-people-api-default/api/football-news11/playground/apiendpoint_7ba472f9-5c31-4342-a378-3fcfd45c7181
class NewsData(models.Model):
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField cho ID
    api_id = models.IntegerField(null=True, blank=True)  # Thêm trường api_id để lưu ID từ API
    title = models.CharField(max_length=255)  # Tiêu đề tin tức
    image_url = models.URLField(max_length=200, null=True, blank=True)  # URL hình ảnh
    original_url = models.URLField(max_length=200)  # URL gốc của tin tức
    published_at = models.DateTimeField()  # Ngày giờ phát hành
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#---------------------------------------------------------------------------------------------------------------
class Sidelined(models.Model): 
    player = models.ForeignKey('Player', to_field='api_id', related_name='player_sidelined' ,on_delete=models.CASCADE)  # Liên kết với model Player
    type = models.CharField(max_length=255)  # Loại chấn thương hoặc lý do bị đình chỉ
    start_date = models.DateField(null=True, blank=True)  # Ngày bắt đầu chấn thương/đình chỉ
    end_date = models.DateField(null=True, blank=True)    # Ngày kết thúc chấn thương/đình chỉ
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.name} - {self.type} ({self.start_date} to {self.end_date})"


#---------------------------------------------------------------------------------------------------------------
class LastestSidelined(models.Model):
    
    STATUS_CHOICES = [
        ('injured', 'Injured'),
        ('recovered', 'Recovered'),
    ]

    api_id = models.ForeignKey(Player, to_field='api_id', on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    team_name = models.CharField(max_length=255)
    player_name = models.CharField(max_length=255)
    player_link = models.URLField()
    injury_type = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.CharField(max_length=50, null=True, blank=True)
    end_date = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='injured')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player_name} ({self.team_name})"


#---------------------------------------------------------------------------------------------------------------
class Transfer(models.Model):
    league = models.ForeignKey(League, to_field='api_id', on_delete=models.CASCADE)
    season = models.CharField(max_length=9, null=True, blank=True)
    team = models.CharField(max_length=100)  # Đội bóng hiện tại
    player = models.CharField(max_length=100)  # Tên cầu thủ
    date = models.DateField()  # Ngày chuyển nhượng
    direction = models.CharField(max_length=10, choices=[('In', 'In'), ('Out', 'Out')])  # Hướng chuyển nhượng (vào/ra)
    from_team = models.CharField(max_length=100)  # Đội trước đó của cầu thủ
    from_team_link = models.URLField(max_length=255, blank=True)  # Link đội bóng
    from_team_title = models.CharField(max_length=100, blank=True)  # Title của đội bóng
    transfer_type = models.CharField(max_length=50)  # Loại chuyển nhượng (VD: Transfer, Loan, Free)

    class Meta:
        verbose_name = 'Transfer'
        verbose_name_plural = 'Transfers'
        ordering = ['-date']  # Sắp xếp theo ngày mới nhất

    def __str__(self):
        return f"{self.player} - {self.team} ({self.direction})"


#---------------------------------------------------------------------------------------------------------------
class TeamMapping(models.Model):
    transfer_team_name = models.CharField(max_length=100)  # Tên đội bóng trong Transfer
    team = models.ForeignKey('Team', to_field='api_id', related_name='mappings', on_delete=models.CASCADE)  # Liên kết tới model Team

    class Meta:
        verbose_name = 'Team Mapping'
        verbose_name_plural = 'Team Mappings'
    
    def __str__(self):
        return f"{self.transfer_team_name} -> {self.team.name}"


#---------------------------------------------------------------------------------------------------------------
class FixtureEvents(models.Model):
    match = models.ForeignKey(Match, to_field='api_id', on_delete=models.CASCADE, related_name='fixture_events')
    events_time_elapsed = models.PositiveIntegerField()
    events_time_extra = models.PositiveIntegerField(null=True, blank=True)
    events_team = models.ForeignKey(Team, to_field='api_id', on_delete=models.CASCADE)
    events_player = models.ForeignKey(Player, to_field='api_id', related_name='events', on_delete=models.CASCADE)
    events_player_assist = models.ForeignKey(Player, to_field='api_id', null=True, blank=True, related_name='assists', on_delete=models.CASCADE)
    events_type = models.CharField(max_length=50)
    events_detail = models.TextField()
    events_comment = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ()

class FixtureLineupPlayer(models.Model):
    match = models.ForeignKey(Match, to_field='api_id', on_delete=models.CASCADE, related_name='lineup_players')
    team = models.ForeignKey(Team, to_field='api_id', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, to_field='api_id', on_delete=models.CASCADE)
    position = models.CharField(max_length=10)
    shirt_number = models.PositiveIntegerField(null=True, blank=True)
    grid = models.CharField(max_length=10, null=True, blank=True)
    is_starting = models.BooleanField(default=True)
    color_primary = models.CharField(max_length=7, blank=True, null=True)
    color_number = models.CharField(max_length=7, blank=True, null=True)
    color_border = models.CharField(max_length=7, blank=True, null=True)
    color_gk_primary = models.CharField(max_length=7, blank=True, null=True)
    color_gk_number = models.CharField(max_length=7, blank=True, null=True)
    color_gk_border = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        unique_together = ()

class FixtureTeamStatistics(models.Model):
    match = models.ForeignKey(Match, to_field='api_id', on_delete=models.CASCADE, related_name='team_statistics')
    team = models.ForeignKey(Team, to_field='api_id', on_delete=models.CASCADE)
    stat_type = models.CharField(max_length=50)
    value = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = ()

class FixturePlayerStatistics(models.Model):
    match = models.ForeignKey(Match, to_field='api_id', on_delete=models.CASCADE, related_name='player_statistics')
    team = models.ForeignKey(Team, to_field='api_id', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, to_field='api_id', on_delete=models.CASCADE)
    minutes = models.PositiveIntegerField(null=True, blank=True)
    number = models.PositiveIntegerField(null=True, blank=True)
    position = models.CharField(max_length=10, null=True, blank=True)
    rating = models.CharField(max_length=5, null=True, blank=True)
    captain = models.BooleanField(default=False)
    substitute = models.BooleanField(default=False, null=True, blank=True)
    offsides = models.PositiveIntegerField(null=True, blank=True)
    shots_total = models.PositiveIntegerField(null=True, blank=True)
    shots_on = models.PositiveIntegerField(null=True, blank=True)
    goals_total = models.PositiveIntegerField(null=True, blank=True)
    goals_conceded = models.PositiveIntegerField(null=True, blank=True)
    goals_assists = models.PositiveIntegerField(null=True, blank=True)
    goals_saves = models.PositiveIntegerField(null=True, blank=True)
    passes_total = models.PositiveIntegerField(null=True, blank=True)
    passes_key = models.PositiveIntegerField(null=True, blank=True)
    passes_accuracy = models.CharField(max_length=10, null=True, blank=True)
    tackles_total = models.PositiveIntegerField(null=True, blank=True)
    tackles_blocks = models.PositiveIntegerField(null=True, blank=True)
    tackles_interceptions = models.PositiveIntegerField(null=True, blank=True)
    duels_total = models.PositiveIntegerField(null=True, blank=True)
    duels_won = models.PositiveIntegerField(null=True, blank=True)
    dribbles_attempts = models.PositiveIntegerField(null=True, blank=True)
    dribbles_success = models.PositiveIntegerField(null=True, blank=True)
    dribbles_past = models.PositiveIntegerField(null=True, blank=True)
    fouls_drawn = models.PositiveIntegerField(null=True, blank=True)
    fouls_committed = models.PositiveIntegerField(null=True, blank=True)
    cards_yellow = models.PositiveIntegerField(null=True, blank=True)
    cards_red = models.PositiveIntegerField(null=True, blank=True)
    penalty_won = models.PositiveIntegerField(null=True, blank=True)
    penalty_committed = models.PositiveIntegerField(null=True, blank=True)
    penalty_scored = models.PositiveIntegerField(null=True, blank=True)
    penalty_missed = models.PositiveIntegerField(null=True, blank=True)
    penalty_saved = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
            unique_together = ()

















