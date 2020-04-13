"""servidor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

# basado en el tutorial: https://www.django-rest-framework.org/tutorial/quickstart/#project-setup
# Puede que usemos esto de punto de partida, puede que cambiemos todo. Si eso aqui esta:

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from musica import views
# Para ficheros estaticos:
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.authtoken import views as DRF_views

from django.views.decorators.csrf import csrf_exempt # Para registros, https://stackoverflow.com/a/51659083


router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
router.register(r'artists', views.ArtistViewSet)
router.register(r'albums', views.AlbumViewSet)
router.register(r'songs', views.SongViewSet, basename='song')
router.register(r'podcasts', views.PodcastViewSet)
router.register(r'podcast-episodes', views.PodcastEpisodeViewSet)
router.register(r'playlists', views.PlaylistViewSet)
router.register(r'user/playlists', views.UserPlaylistViewSet, basename='UserPlaylists') # Basename necesario si no hay queryset en el viewset
router.register(r's7_user', views.S7_userViewSet)
# debug de autorización, provisional:
router.register(r'debug_auth', views.debugAuthViewSet, basename="debug-auth") # en este caso basename es necesario para diferenciarlo de s7-user
router.register(r'trending-podcast', views.TrendingPodcastsViewSet, basename="TrendingPodcasts")
# busqueda, se viene rayada:
#router.register(r'search', views.SearchViewSet, basename='search')
# Registros de ususarios:
#router.register(r'register', views.RegisterUserView, basename="register")


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    #No las he sabido meter en el router. Aún así lo veo mejor así
    path('podcast/<str:id>/', views.PodcastById.as_view()),
    path('episode/<str:id>/', views.PodcastEpisodeById.as_view()),
    ##Comprobar que esto no falle, en la docu ponia que habia que poner url, no path
    #path(r'accounts/', include('allauth.urls')),
    #path('auth/', include('rest_framework_social_oauth2.urls')),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # Autentificacion con tokens:
    path('api-token-auth/', DRF_views.obtain_auth_token, name='api-token-auth'),
    # Registros de ususarios:
    path(r'register/', csrf_exempt(views.RegisterUserView.as_view()), name='register')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # para los ficheros media (mp3)
