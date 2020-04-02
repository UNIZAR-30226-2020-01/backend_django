from django.shortcuts import render

# Create your views here.


from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from musica.serializers import *

from musica.models import Song, Album, Artist, Podcast, PodcastEpisode


# En general, usamos viewsets ya que facilitan la consistencia de la API, documentacion: https://www.django-rest-framework.org/api-guide/viewsets/

# Clases predefinidas del mismo tutorial: https://www.django-rest-framework.org/tutorial/quickstart/#project-setup
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# Nuevas:
class ArtistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songs to be viewed.
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    # solo acepta GET:
    http_method_names = ['get']




class AlbumViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songs to be viewed.
    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    # solo acepta GET:
    http_method_names = ['get']




# No tendremos endpoint para los audios, desde el punto de vista del cliente las canciones y los podcasts no tienen nada que ver:
class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songs to be viewed.
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    # solo acepta GET:
    http_method_names = ['get']
    # fuente de la solución: https://stackoverflow.com/a/31450643

# No tendremos endpoint para los audios, desde el punto de vista del cliente las canciones y los podcasts no tienen nada que ver:
class PlaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songs to be viewed.
    """
    queryset = Playlist.objects.all()
    serializer_class = PlayListSerializer
    # solo acepta GET:
    http_method_names = ['get']
    # fuente de la solución: https://stackoverflow.com/a/31450643




class PodcastViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songs to be viewed.
    """
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer
    # solo acepta GET:
    http_method_names = ['get']
    # fuente de la solución: https://stackoverflow.com/a/31450643



class PodcastEpisodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songs to be viewed.
    """
    queryset = PodcastEpisode.objects.all()
    serializer_class = PodcastEpisodeSerializer
    # solo acepta GET:
    http_method_names = ['get']
    # fuente de la solución: https://stackoverflow.com/a/31450643
