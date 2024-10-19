from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transfer, PlayerSeasonStatistics, TeamMapping
from django.utils import timezone

@receiver(post_save, sender=Transfer)
def update_player_season_status(sender, instance, created, **kwargs):

    team_mapping = TeamMapping.objects.filter(transfer_team_name=instance.team).first()

    if team_mapping:
        # Lấy ID của team từ mapping
        team_id = team_mapping.team.api_id

        # Lấy tất cả các PlayerSeasonStatistics liên quan đến cầu thủ và đội bóng trong Transfer
        player_statistics = PlayerSeasonStatistics.objects.filter(
            player__name=instance.player,  # Giả sử bạn đang sử dụng api_id để liên kết với Player
            team__api_id=team_id  # Sử dụng api_id từ mapping
        )
        
        today = timezone.now().date()
        latest_transfer = Transfer.objects.filter(
            player=instance.player,
            team=instance.team,
            date__lte=today
        ).order_by('-date').first()

        # Cập nhật trạng thái cho từng PlayerSeasonStatistics
        for stats in player_statistics:
            if latest_transfer:
                if latest_transfer.direction == 'In':
                    stats.status = 'Current'
                elif latest_transfer.direction == 'Out':
                    stats.status = 'Transferred'
            else:
                stats.status = 'Current'  # Mặc định nếu không có chuyển nhượng

            stats.save()  # Lưu thay đổi