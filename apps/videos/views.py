import time
import json
from decimal import Decimal
from datetime import date

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.db import transaction as db_transaction
from django.db.models import Sum

from .models import Video, VideoWatch
from profiles.models import Wallet, Earning, UserPlan


def _get_user_plan(user):
    """Return the user's active UserPlan or None."""
    try:
        up = user.user_plan
        if up.is_active and up.package:
            return up
    except UserPlan.DoesNotExist:
        pass
    return None


@login_required(login_url='accounts:login')
def video_list_view(request):
    """Show all active videos and which ones the user has already earned from today."""
    today = date.today()
    user_plan = _get_user_plan(request.user)
    earning_per_video = user_plan.package.earning_per_video if user_plan else Decimal('0.00')

    videos = Video.objects.filter(is_active=True)

    watched_today_ids = set(
        VideoWatch.objects.filter(
            user=request.user, watched_date=today
        ).values_list('video_id', flat=True)
    )

    video_data = [
        {'video': v, 'already_watched': v.id in watched_today_ids}
        for v in videos
    ]

    today_earned = VideoWatch.objects.filter(
        user=request.user, watched_date=today
    ).aggregate(total=Sum('earned_amount'))['total'] or Decimal('0.00')

    # Full watch history for the "Previous Work" tab
    watch_history = (
        VideoWatch.objects
        .filter(user=request.user)
        .select_related('video')
        .order_by('-created_at')
    )

    total_earned_all = watch_history.aggregate(
        total=Sum('earned_amount')
    )['total'] or Decimal('0.00')

    context = {
        'video_data': video_data,
        'user_plan': user_plan,
        'earning_per_video': earning_per_video,
        'today_earned': today_earned,
        'user_data': request.user,
        'watched_count_today': len(watched_today_ids),
        'total_videos': videos.count(),
        'watch_history': watch_history,
        'total_earned_all': total_earned_all,
    }
    return render(request, 'videos/video_list.html', context)


@login_required(login_url='accounts:login')
@require_POST
@csrf_protect
def start_watch_view(request, video_id):
    """Record when the user starts watching — used for server-side timing check."""
    video = get_object_or_404(Video, id=video_id, is_active=True)
    request.session[f'video_{video_id}_start'] = time.time()
    return JsonResponse({'success': True, 'duration': video.duration})


@login_required(login_url='accounts:login')
@require_POST
@csrf_protect
def mark_complete_view(request, video_id):
    """
    Called via AJAX when the user finishes watching.
    Validates timing, then credits the earning to their wallet.
    """
    video = get_object_or_404(Video, id=video_id, is_active=True)
    today = date.today()

    # 1. User must have an active plan
    user_plan = _get_user_plan(request.user)
    if not user_plan:
        return JsonResponse({'success': False, 'error': 'You need an active plan to earn from videos.'})

    earning = user_plan.package.earning_per_video
    if earning <= 0:
        return JsonResponse({'success': False, 'error': 'Your current plan has no video earning configured.'})

    # 2. Only once per video per day
    if VideoWatch.objects.filter(user=request.user, video=video, watched_date=today).exists():
        return JsonResponse({'success': False, 'error': 'You have already earned from this video today.'})

    # 3. Server-side timing check — user must have had the video open long enough
    session_key = f'video_{video_id}_start'
    start_time = request.session.get(session_key)
    if not start_time:
        return JsonResponse({'success': False, 'error': 'Watch session not found. Please open the video and watch it fully.'})

    elapsed = time.time() - start_time
    required_seconds = video.duration * 0.90  # 10 % tolerance
    if elapsed < required_seconds:
        return JsonResponse({'success': False, 'error': 'You must watch the full video before earning.'})

    # 4. Credit the earning
    try:
        with db_transaction.atomic():
            VideoWatch.objects.create(
                user=request.user,
                video=video,
                watched_date=today,
                earned_amount=earning,
            )
            wallet, _ = Wallet.objects.get_or_create(
                user=request.user,
                defaults={'balance': Decimal('0.00')}
            )
            Earning.objects.create(
                wallet=wallet,
                amount=earning,
                note=f'Video earning: {video.title}',
            )
            # Remove session key now that it's been used
            request.session.pop(session_key, None)
    except Exception:
        return JsonResponse({'success': False, 'error': 'An error occurred. Please try again.'})

    return JsonResponse({
        'success': True,
        'earned': str(earning),
        'message': f'You earned ${earning} for completing this video!',
    })
