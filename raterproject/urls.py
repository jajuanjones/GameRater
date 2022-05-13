"""raterproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from gameraterapi.views import GameView
from gameraterapi.views import CategoryView
from gameraterapi.views import PhotoView
from gameraterapi.views import PlayerView
from gameraterapi.views import RatingView
from gameraterapi.views import ReviewView
from django.conf.urls.static import static
import raterproject.settings as settings
from gameraterapi.views.auth import login_user, register_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', GameView, 'game')
router.register(r'categories', CategoryView, 'category')
router.register(r'photos', PhotoView, 'photo')
router.register(r'players', PlayerView, 'player')
router.register(r'ratings', RatingView, 'rating')
router.register(r'reviews', ReviewView, 'review')

urlpatterns = [
    path('login', login_user),
    path('register', register_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls )),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
