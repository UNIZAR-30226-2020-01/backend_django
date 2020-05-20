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
router.register(r'songs', views.SongViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'channels', views.ChannelViewSet)
router.register(r'podcasts', views.PodcastViewSet)
router.register(r'podcast-episodes', views.PodcastEpisodeViewSet)
router.register(r'playlists', views.PlaylistViewSet)
router.register(r'user/playlists', views.UserPlaylistViewSet, basename='UserPlaylists') # Basename necesario si no hay queryset en el viewset
router.register(r'user/followed/playlists', views.FollowedPlaylistViewSet, basename='FollowedPlaylists') # Basename necesario si no hay queryset en el viewset
router.register(r'user/favorites', views.UserFavoritesViewSet, basename='UserFavorites')
router.register(r's7_user', views.S7_userViewSet, basename='s7_user')
# debug de autorización, provisional:
router.register(r'debug_auth', views.debugAuthViewSet, basename="debug-auth") # en este caso basename es necesario para diferenciarlo de s7-user
router.register(r'trending-podcast', views.TrendingPodcastsViewSet, basename="TrendingPodcasts")

router.register(r'current-user', views.CurrentUserView, basename='current-user')
# busqueda, se viene rayada:
#router.register(r'search', views.SearchViewSet)
# Registros de ususarios:
#router.register(r'register', views.RegisterUserView, basename="register")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),#csrf_exempt(admin.site.urls)),
    #No las he sabido meter en el router. Aún así lo veo mejor así
    path('podcast/<str:id>/', views.PodcastById.as_view()),
    path('episode/<str:id>/', views.PodcastEpisodeById.as_view()),
    ##Comprobar que esto no falle, en la docu ponia que habia que poner url, no path
    #path(r'accounts/', include('allauth.urls')),

    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # Autentificacion con tokens:
    path('api-token-auth/', DRF_views.obtain_auth_token, name='api-token-auth'),
	path(r'register/', csrf_exempt(views.RegisterUserView.as_view()), name='register'),
    path('auth/', include('rest_framework_social_oauth2.urls')), # oauth2
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # para los ficheros media (mp3)
