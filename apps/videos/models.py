import re
from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    """A video that users can watch to earn rewards."""
    title = models.CharField(max_length=255)
    url = models.URLField(help_text='YouTube video URL (e.g. https://www.youtube.com/watch?v=xxxx)')
    duration = models.PositiveIntegerField(help_text='Video duration in seconds')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title

    @property
    def youtube_id(self):
        """Extract YouTube video ID from various URL formats."""
        patterns = [
            r'(?:youtube\.com/watch\?(?:.*&)?v=)([^&\s]+)',
            r'(?:youtu\.be/)([^?\s]+)',
            r'(?:youtube\.com/embed/)([^?\s]+)',
            r'(?:youtube\.com/shorts/)([^?\s]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.url)
            if match:
                return match.group(1)
        return None

    @property
    def duration_display(self):
        mins = self.duration // 60
        secs = self.duration % 60
        if mins:
            return f'{mins}m {secs:02d}s'
        return f'{secs}s'


class VideoWatch(models.Model):
    """Records a completed video watch and the earning awarded."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_watches')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='watches')
    watched_date = models.DateField()
    earned_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # One earning per video per user per day
        unique_together = ('user', 'video', 'watched_date')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} — {self.video.title} on {self.watched_date}'
