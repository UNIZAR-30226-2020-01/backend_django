from django.shortcuts import render

# Create your views here.


from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from musica.serializers import *

from musica.models import *
from utils.podcasts.podcasts import Podcasts_api

from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# En general, usamos viewsets ya que facilitan la consistencia de la API, documentacion: https://www.django-rest-framework.org/api-guide/viewsets/


# Nuevas:
class ArtistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songs to be viewed.
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistListSerializer # por defecto lista
    # solo acepta GET:
    http_method_names = ['get']

    action_serializers = {
        'retrieve': ArtistDetailSerializer,
        'list': ArtistListSerializer,
        #'create': MyModelCreateSerializer
    }

    def get_serializer_class(self):

        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(MyModelViewSet, self).get_serializer_class()



# Para diferenciar de list y detail, basado en: https://stackoverflow.com/a/30670569
# class AlbumViewSet(viewsets.ModelViewSet):
#
#     queryset = Album.objects.all()
#     serializer_class = AlbumSerializer
#     # solo acepta GET:
#     http_method_names = ['get']

class AlbumViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows albums to be viewed.
    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    http_method_names = ['get']
    action_serializers = {
        'retrieve': AlbumDetailSerializer,
        'list': AlbumListSerializer,
        #'create': MyModelCreateSerializer
    }

    def get_serializer_class(self):

        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(AlbumViewSet, self).get_serializer_class()



# No tendremos endpoint para los audios, desde el punto de vista del cliente las canciones y los podcasts no tienen nada que ver:
class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songs to be viewed.
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    # solo acepta GET:
    http_method_names = ['get']
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows all playlists to be viewed.
    """
    queryset = Playlist.objects.all()
    serializer_class = PlayListSerializer
    # solo acepta GET:
    http_method_names = ['get']
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643



class UserPlaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows all playlists to be viewed.
    """
    #queryset = Playlist.objects.all()

    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PlayListSerializer
    # solo acepta GET:
    http_method_names = ['get']
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643

    # Sobreescribimos el método que devuelve el queryset, para que de las
    # playlists del usuario autentificado
    #(basado en https://www.django-rest-framework.org/api-guide/filtering/#django-rest-framework-full-word-search-filter)
    def get_queryset(self):
        """
        This view should return a list of all the playlists
        for the currently authenticated user.
        """
        user = self.request.user
        print("Usuario en request: ", user)
        return Playlist.objects.filter(user=user)



class PodcastViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songs to be viewed.
    """
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer
    # solo acepta GET:
    http_method_names = ['get']
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643

class PodcastEpisodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songs to be viewed.
    """
    queryset = PodcastEpisode.objects.all()
    serializer_class = PodcastEpisodeSerializer
    # solo acepta GET:
    http_method_names = ['get']
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643


class SearchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to search stuff.
    """
    queryset = Song.objects.all()
    serializer_class = SearchSerializer
    # solo acepta GET:
    http_method_names = ['get']
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643




# Clases predefinidas del mismo tutorial: https://www.django-rest-framework.org/tutorial/quickstart/#project-setup
# TODO: eliminar, la dejo por si es útil
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)



class S7_userViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to search stuff.
    """
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]
    queryset = S7_user.objects.all().order_by('-date_joined')
    serializer_class = S7_userSerializer
    # solo acepta GET:
    http_method_names = ['get']
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643
    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)

#Para trending podcast mediante router
class TrendingPodcastsViewSet(viewsets.ViewSet):
    serializer_class = TrendingPodcastsSerializer

    def list(self, request):
        #Obtenemos los podcast recomendados dinámicamente
        api = Podcasts_api()
        result = api.get_bestpodcast()
        serializer = TrendingPodcastsSerializer(
            instance=result, many=True)
        return Response(serializer.data)

# Vista que muestra información detallada de un podcast dado su id
# Desde aquí se accederá a sus episodios
class PodcastById(APIView):
    def get(self, request, id):
        api = Podcasts_api()
        print(id)
        result = api.get_detailedInfo_podcast(id)
        return Response(result)

class PodcastEpisodeById(APIView):
    def get(self, request, id):
        api = Podcasts_api()
        print(id)
        result = api.get_detailedInfo_episode(id)
        return Response(result)

class debugAuthViewSet(viewsets.ModelViewSet):
    """
    Endpoint provisional para debuguear auth (basicamente como s7-user pero requiere token)
    """
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = S7_user.objects.all().order_by('-date_joined')
    serializer_class = S7_userSerializer
    # solo acepta GET:
    http_method_names = ['get']
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643
    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)
