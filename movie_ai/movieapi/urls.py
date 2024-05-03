from django.urls import path
from . import views

urlpatterns = [
    path('short_form', views.short_form, name='short_form'),
    path('video_qa', views.video_qa, name='video_qa'),
    path('avatar_chat', views.avatar_chat, name='avatar_chat'),
]

