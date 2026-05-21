from django.contrib import admin
from .models import Video, VideoWatch


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration_display', 'is_active', 'order', 'created_at')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'url')
    ordering = ('order', 'created_at')

    def duration_display(self, obj):
        return obj.duration_display
    duration_display.short_description = 'Duration'


@admin.register(VideoWatch)
class VideoWatchAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'earned_amount', 'watched_date', 'created_at')
    list_filter = ('watched_date', 'video')
    search_fields = ('user__username', 'video__title')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
