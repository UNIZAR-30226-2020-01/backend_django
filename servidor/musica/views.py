from django.shortcuts import render

# Create your views here.


from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from musica.serializers import *

from musica.models import *

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# En general, usamos viewsets ya que facilitan la consistencia de la API, documentacion: https://www.django-rest-framework.org/api-guide/viewsets/


# Clases predefinidas del mismo tutorial: https://www.django-rest-framework.org/tutorial/quickstart/#project-setup
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)

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

# No tendremos endpoint para los audios, desde el punto de vista del cliente las canciones y los podcasts no tienen nada que ver:
class PlaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows playlists to be viewed.
    """
    queryset = Playlist.objects.all()
    serializer_class = PlayListSerializer
    # solo acepta GET:
    http_method_names = ['get']
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643

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


###TODO: Revisar, seguramente habra que eliminar esto
class S7_userViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to search stuff.
    """
    queryset = S7_user.objects.all()
    serializer_class = S7_userSerializer
    # solo acepta GET:
    http_method_names = ['get']
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643
