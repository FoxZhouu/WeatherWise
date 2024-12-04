from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_weather, name='get_weather'),  # 根 URL 指向 get_weather 视图
    path('weather/', views.get_weather, name='get_weather'),
    path('news/', views.news, name='news'),
    path('live_cameras/', views.live_cameras, name='live_cameras'),
    path('photos/', views.photos, name='photos'),
    path('contact/', views.contact, name='contact'),
]