from django.contrib.auth.models import User
#from musica.models import Song, Album, Artist, PodcastEpisode, Podcast
from musica.models import *
from rest_framework import serializers



# Esta cosa tan fea es la unica forma que he encontrado de poner todos los campos del modelo (__all__) mas uno externo:
# Devuelve una lista, con funcionalidad equivalente a __all__, pero extensible (y sin incluir el identificador)
def todosloscampos(modelo, exclude=['']):
    # lista de los nombres (str) de los campos del modelo que no sean 'id' ni esten en exclude (lista de str)
    return [f.name for f in modelo._meta.get_fields() if f.name != 'id' and f.name not in exclude]


# Tambien copiado del tutorial https://www.django-rest-framework.org/tutorial/quickstart/#project-setup .........
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']



class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'
        depth = 1



class AlbumListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'
        depth = 1

class AlbumDetailSerializer(serializers.HyperlinkedModelSerializer):
    #songs = SongSerializer(many=True) #source='album.song_set',
    class Meta:
        model = Album
        # * convierte la lista en argumentos separados (ej: (*[a,b],c) es equivalente a (a,b,c))
        fields = (*todosloscampos(model), 'songs') # (*[f.name for f in Album._meta.get_fields()], 'songs')
        depth = 1

# Serializador del album sin artista
class AlbumReducedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Album
        fields = (*todosloscampos(model, ['artist','songs']), 'songs') # (*[f.name for f in Album._meta.get_fields()], 'songs')
        depth = 0


class ArtistListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'
        depth = 2

class ArtistDetailSerializer(serializers.HyperlinkedModelSerializer):
    elalbum = AlbumReducedSerializer(many=True, source='albums')
    class Meta:
        model = Artist
        # * convierte la lista en argumentos separados (ej: (*[a,b],c) es equivalente a (a,b,c))
        fields = (*todosloscampos(model), 'elalbum')
        depth = 1

# TODO: AÒadir el artista directamente
class SongSerializer(serializers.HyperlinkedModelSerializer):
    # Obtenemos los datos del audio as√≠: https://stackoverflow.com/a/27851778
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
        depth = 3


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


# TODO: Buena suerte
class SearchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Song
        #album_detail = AlbumSerializer()
        fields = '__all__'
        depth = 1
        #fields = ['url', 'title', 'artists', 'album', 'file'] #'__all__'#
