from django.contrib import admin
from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.main, name='main'),
    path('<question>', views.questions, name='questions'),
    #path('save_user_answer', views.save_user_answer, name='save_user_answer'),
    ]