from django.urls import path
from . import views

urlpatterns = [
    path('', views.matchresume, name='matchresume'),
    path('matcher/', views.matcher, name='matcher'),
]
