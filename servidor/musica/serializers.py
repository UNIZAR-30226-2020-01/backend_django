from django.contrib.auth.models import User, Group
#from musica.models import Song, Album, Artist, PodcastEpisode, Podcast
from musica.models import *
from rest_framework import serializers


# Tambien copiado del tutorial https://www.django-rest-framework.org/tutorial/quickstart/#project-setup .........
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'
        depth = 2

class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'
        depth = 2

class SongSerializer(serializers.HyperlinkedModelSerializer):
    # Obtenemos los datos del audio así: https://stackoverflow.com/a/27851778
    # todo esto solo es necesario para cambiarle el nombre de la bd
    # title = serializers.CharField(read_only=True, source="cancion.titulo")
    # file = serializers.FileField(read_only=True, source="cancion.archivo")
    #
    #

    #album =
    #album = serializers.CharField(read_only=True, source="song.album.title")
    #CharField(read_only=True, source="song.album.artists")
    #serializers.CharField(read_only=True, source="song.album.artists.name")#
    #artists = serializers.CharField(read_only=True, source="song.album.artists.name", many=True)#ArtistSerializer(source='song.album.artists', many=True)
    class Meta:
        model = Song
        #album_detail = AlbumSerializer()
        fields = '__all__'
        depth = 1
        #fields = ['url', 'title', 'artists', 'album', 'file'] #'__all__'#

class PlayListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'
        depth = 2


class PodcastSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Podcast
        fields = '__all__'
        depth = 2

class PodcastEpisodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PodcastEpisode
        fields = '__all__'
        depth = 2
