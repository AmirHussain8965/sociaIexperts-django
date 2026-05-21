from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.video_list_view, name='list'),
    path('<int:video_id>/start/', views.start_watch_view, name='start_watch'),
    path('<int:video_id>/complete/', views.mark_complete_view, name='mark_complete'),
]
