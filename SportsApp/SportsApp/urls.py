"""SportsApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'SportsApp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(route='', view=views.home, name='home'),
    #path(route='a', view=views.clear_nba_schedule, name='clear_nba_schedule'),
    #path(route='b', view=views.populate_nba_schedule_db, name='populate_nba_schedule_db'),
    #path(route='c', view=views.clear_nba_teams_db, name='clear_nba_teams_db'),
    #path(route='d', view=views.populate_nba_teams_db, name='populate_nba_teams_db'),
    path(route='e', view=views.populate_nba_game_stats, name='populate_nba_game_stats'),
    path(route='f', view=views.calculate_nba_team_stats, name='calculate_nba_team_stats'),
    path(route='NBA', view=views.load_nba_home, name='load_nba_home'),
    path(route='NBA/<str:id>', view=views.load_nba_game, name='load_nba_game'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
