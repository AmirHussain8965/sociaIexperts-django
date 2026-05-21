"""
Management command to seed the Video module with sample test data.

Usage:
    python manage.py seed_videos            # add videos (skip if already exist)
    python manage.py seed_videos --clear    # wipe existing videos first, then seed
"""
from django.core.management.base import BaseCommand
from apps.videos.models import Video


SAMPLE_VIDEOS = [
    {
        'title': 'What is Social Media Marketing?',
        'url': 'https://www.youtube.com/watch?v=3E-HFqJ3sxM',
        'duration': 312,   # 5m 12s
        'order': 1,
    },
    {
        'title': 'How to Grow Your Instagram in 2024',
        'url': 'https://www.youtube.com/watch?v=YtPFMkPXxjk',
        'duration': 487,   # 8m 7s
        'order': 2,
    },
    {
        'title': 'Facebook Ads for Beginners — Full Tutorial',
        'url': 'https://www.youtube.com/watch?v=lTPbVmqFXek',
        'duration': 725,   # 12m 5s
        'order': 3,
    },
    {
        'title': 'Content Marketing Strategy Explained',
        'url': 'https://www.youtube.com/watch?v=3E-HFqJ3sxM',
        'duration': 256,   # 4m 16s
        'order': 4,
    },
    {
        'title': 'SEO Tips — Rank #1 on Google',
        'url': 'https://www.youtube.com/watch?v=MYE6T_gd7H0',
        'duration': 601,   # 10m 1s
        'order': 5,
    },
    {
        'title': 'YouTube Channel Growth Secrets',
        'url': 'https://www.youtube.com/watch?v=B_2mn8gM1_8',
        'duration': 441,   # 7m 21s
        'order': 6,
    },
    {
        'title': 'Email Marketing — Build a List Fast',
        'url': 'https://www.youtube.com/watch?v=9RsfpBgFnZY',
        'duration': 390,   # 6m 30s
        'order': 7,
    },
    {
        'title': 'TikTok Marketing for Business',
        'url': 'https://www.youtube.com/watch?v=o-NOdTIwFKg',
        'duration': 534,   # 8m 54s
        'order': 8,
    },
    {
        'title': 'How to Write Viral Social Media Captions',
        'url': 'https://www.youtube.com/watch?v=3E-HFqJ3sxM',
        'duration': 279,   # 4m 39s
        'order': 9,
    },
    {
        'title': 'Building a Personal Brand Online',
        'url': 'https://www.youtube.com/watch?v=9RsfpBgFnZY',
        'duration': 368,   # 6m 8s
        'order': 10,
    },
]


class Command(BaseCommand):
    help = 'Seed the videos module with sample test data.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing videos before seeding.',
        )

    def handle(self, *args, **options):
        if options['clear']:
            count, _ = Video.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {count} existing video(s).'))

        created = 0
        skipped = 0
        for data in SAMPLE_VIDEOS:
            _, was_created = Video.objects.get_or_create(
                title=data['title'],
                defaults={
                    'url': data['url'],
                    'duration': data['duration'],
                    'order': data['order'],
                    'is_active': True,
                }
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Done — {created} video(s) created, {skipped} already existed.'
            )
        )
