from django.db import models

# Create your models here.
class League(models.Model):
    league_id = models.IntegerField(primary_key=True)  # Primary key for the league
    league_name = models.CharField(max_length=255)     # League or Cup name
    league_type = models.CharField(max_length=50)      # Type ('League' or 'Cup')
    league_logo = models.URLField(max_length=500)      # URL for the league logo

    # Country information
    country_name = models.CharField(max_length=255)    # Name of the country
    country_code = models.CharField(max_length=10)     # Code for the country
    country_flag = models.URLField(max_length=500)     # URL for the country flag

    # Quan hệ: Một League có nhiều Teams và Matches
    # teams = models.ManyToManyField('Team', related_name='leagues', blank=True)
    # matches = models.ManyToManyField('Match', related_name='leagues', blank=True)

    def __str__(self):
        return self.league_name

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=255)
    team_code = models.CharField(max_length=10, blank=True, null=True)
    team_country = models.CharField(max_length=255)
    team_founded = models.IntegerField(blank=True, null=True)
    team_logo_url = models.URLField(blank=True, null=True)
    team_venue_id = models.IntegerField(blank=True, null=True)
    team_venue_name = models.CharField(max_length=255, blank=True, null=True)
    team_venue_address = models.CharField(max_length=255, blank=True, null=True)
    team_venue_city = models.CharField(max_length=255, blank=True, null=True)
    team_venue_capacity = models.IntegerField(blank=True, null=True)
    team_venue_surface = models.CharField(max_length=50, blank=True, null=True)
    team_venue_image = models.URLField(blank=True, null=True)

    # Relations
    # players = models.ManyToManyField('Player', related_name='teams', blank=True)
    # injuries = models.ManyToManyField('Injury', related_name='teams', blank=True)
    def __str__(self):
        return self.team_name
    
class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    match_date = models.DateTimeField()
    timezone = models.CharField(max_length=50)
    timestamp = models.DateTimeField()  # Optional if you want to store a timestamp
    league = models.ForeignKey(League, related_name='matches', on_delete=models.CASCADE)
    league_name = models.CharField(max_length=255)  # Redundant, but for convenience
    league_country = models.CharField(max_length=255)  # Redundant, but for convenience
    league_logo_url = models.URLField()  # Redundant, but for convenience
    league_flag_url = models.URLField()  # Redundant, but for convenience
    league_season = models.CharField(max_length=255)  # e.g., "2024/2025"
    league_round = models.CharField(max_length=255)  # e.g., "Matchday 1"
    match_home_team = models.CharField(max_length=255)
    match_home_id = models.IntegerField()
    match_away_team = models.CharField(max_length=255)
    match_away_id = models.IntegerField()
    match_home_team_logo_url = models.URLField()
    match_away_team_logo_url = models.URLField()
    match_home_winner = models.BooleanField(default=False)
    match_away_winner = models.BooleanField(default=False)
    match_referee = models.CharField(max_length=255, blank=True, null=True)
    match_venue_id = models.IntegerField()
    match_venue_name = models.CharField(max_length=255)
    match_venue_city = models.CharField(max_length=255)
    match_status_long = models.CharField(max_length=50)  # e.g., "Match Finished"
    match_status_short = models.CharField(max_length=10)  # e.g., "FT"
    score_halftime_home = models.IntegerField(blank=True, null=True)
    score_fulltime_home = models.IntegerField(blank=True, null=True)
    score_extratime_home = models.IntegerField(blank=True, null=True)
    score_penalty_home = models.IntegerField(blank=True, null=True)
    score_halftime_away = models.IntegerField(blank=True, null=True)
    score_fulltime_away = models.IntegerField(blank=True, null=True)
    score_extratime_away = models.IntegerField(blank=True, null=True)
    score_penalty_away = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.match_home_team} vs {self.match_away_team} on {self.match_date}"