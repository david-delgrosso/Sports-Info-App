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
    path(route='', view=views.home_view, name='home_view'),
    path(route='NBA', view=views.nba_home_view, name='load_nba_home'),
    path(route='NBA/<str:id>', view=views.nba_game_view, name='load_nba_game'),
    path(route='NBA/models/<str:model_name>', view=views.nba_model_view, name='load_nba_model'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
