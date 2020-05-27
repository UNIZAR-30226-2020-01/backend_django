from django.contrib.auth.models import User
#from musica.models import Song, Album, Artist, PodcastEpisode, Podcast
from musica.models import *
from utils.podcasts.podcasts import Podcasts_api # para deshacer redirects
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.podcasts.podcasts import TrendingPodcasts
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

# Para validacion en posts (registros, etc...)
from django.core.exceptions import ValidationError
import django.contrib.auth.password_validation as validators


from rest_framework.fields import CurrentUserDefault




# Esta cosa tan fea es la unica forma que he encontrado de poner todos los campos del modelo (__all__) mas uno externo:
# Devuelve una lista, con funcionalidad equivalente a __all__, pero extensible (y sin incluir el identificador)
def todosloscampos(modelo, exclude=['']):
    # lista de los nombres (str) de los campos del modelo que no sean 'id' ni esten en exclude (lista de str)

    return ['url'] + [f.name for f in modelo._meta.get_fields() if f.name != 'id' and f.name not in exclude]

# para obtener el usuario de la request, basado en: https://stackoverflow.com/a/30203950
def get_user(serializer, validate=False):
    user = None
    request = serializer.context.get("request")
    if request and hasattr(request, "user"):
        user = request.user
        if validate and user.is_anonymous:
            raise serializers.ValidationError(
                    ('No estas autentificado!')
                )
    return user


# extendemos CurrentUserDefault para poder traducirlo a s7_user
class OurCurrentUserDefault(serializers.CurrentUserDefault):
    requires_context = True
    def __call__(self, serializer_field):
        user = get_user(serializer_field, validate=True) # user el por defecto de django...............
        return S7_user.objects.get(id=user.id)
    # def toS7(self) -> S7_user:
    #     return S7_user.objects.get(id=user.id)


class S7_userDefault():
    def __init__(self):
        user


# Para campos mas complejos derivados de relaciones entre modelos:
# https://www.django-rest-framework.org/api-guide/relations/#custom-relational-fields
# Devuelve "True" o "False" en funci�n de si la canci�n est� entre las favoritas del usuario
class IsFavField(serializers.RelatedField):
    # instance es la instancia de la cancion (modelo Song)
    def to_representation(self, instance):
        user = get_user(self)
        # print('Eres', user)
        # print(instance)
        is_fav = instance.is_favorite_of(user)
        # TODO: cambiar la busqueda de usuarios de la cancion a canciones del usuario (+ eficiente seguramente)
        #is_fav = 'dummy'
        return is_fav

# TODO: A�adir el artista directamente
class SongReducedSerializer(serializers.HyperlinkedModelSerializer):
    is_fav = IsFavField(source='song', many=False, read_only=True)

    class Meta:
        model = Song
        #album_detail = AlbumSerializer()
        #fields = '__all__'# (*todosloscampos(model), 'is_favorite')#'__all__'
        fields = ['url', 'title', 'file', 'duration', 'is_fav']# ['is_fav']
        depth = 2
        #fields = ['url', 'title', 'artists', 'album', 'file'] #'__all__'#


# Tambien copiado del tutorial https://www.django-rest-framework.org/tutorial/quickstart/#project-setup .........
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'favorito']


# class AlbumSerializer(serializers.HyperlinkedModelSerializer):
#     songs = SongListSerializer(many=True)
#     class Meta:
#         model = Album
#         fields = (*todosloscampos(model),'number_songs')
#         depth = 1


# TODO: MOVER ANTES DE ALBUM
class ArtistListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist # TODO: excluir biografia, albumes (los dos tipos) y el email
        fields =  ['url', 'name', 'image','number_albums', 'number_songs']#(*todosloscampos(model), 'number_albums', 'number_songs')
        depth = 0

# url, titulo, artista (lista), icono (), number_songs
class AlbumListSerializer(serializers.HyperlinkedModelSerializer):

    artist = ArtistListSerializer()
    class Meta:
        model = Album
        fields = ['url', 'title', 'artist', 'icon', 'number_songs'] # number_songs solo pal detalle, un count menos a la bd
        depth = 1


# TODO: A�adir el artista directamente
class SongDetailSerializer(serializers.HyperlinkedModelSerializer):
    is_fav = IsFavField(source='song', many=False, read_only=True)
    album = AlbumListSerializer()
    class Meta:
        model = Song
        #album_detail = AlbumSerializer()
        #fields = '__all__'# (*todosloscampos(model), 'is_favorite')#'__all__'
        fields ='__all__'# ['is_fav']
        depth = 2
        #fields = ['url', 'title', 'artists', 'album', 'file'] #'__all__'#


class SongListSerializer(serializers.HyperlinkedModelSerializer):
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

    is_fav = IsFavField(source='song', many=False, read_only=True)
    album = AlbumListSerializer()
    class Meta:
        model = Song
        #album_detail = AlbumSerializer()
        fields = ['url', 'title', 'file', 'duration', 'album', 'is_fav', 'times_played', 'times_faved']#,] # todosloscampos(model, ['lyrics', 's7_user', 'playlist'])
        depth = 2
        #fields = ['url', 'title', 'artists', 'album', 'file'] #'__all__'#


# Mini, para reducir carga de playlists
class ArtistListMiniSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist # TODO: excluir biografia, albumes (los dos tipos) y el email
        fields =  ['url', 'name']#(*todosloscampos(model), 'number_albums', 'number_songs')
        depth = 1

# Mini, para reducir carga de playlists
class AlbumListMiniSerializer(serializers.HyperlinkedModelSerializer):

    artist = ArtistListMiniSerializer()
    class Meta:
        model = Album
        fields = ['url', 'title', 'artist', 'icon']
        depth = 1

# Mini, para reducir carga de playlists
class SongListMiniSerializer(serializers.HyperlinkedModelSerializer):
    is_fav = IsFavField(source='song', many=False, read_only=True)
    album = AlbumListMiniSerializer()

    class Meta:
        model = Song
        #album_detail = AlbumSerializer()
        fields = ['url', 'title', 'file', 'album', 'is_fav'] # todosloscampos(model, ['lyrics', 's7_user', 'playlist'])
        depth = 2
        #fields = ['url', 'title', 'artists', 'album', 'file'] #'__all__'#



# Intento fallido de mejorar eficiencia:
# # Mini, para reducir carga de playlists
# class SongListMiniSerializer_2(serializers.HyperlinkedModelSerializer):
#     is_fav = IsFavField(source='song', many=False, read_only=True)
#     album = serializers.CharField(source='album.title')
#     icon = serializers.FileField(source='album.icon')
#     artist = serializers.CharField(source='album.artist.name')
#     class Meta:
#         model = Song
#         #album_detail = AlbumSerializer()
#         fields = ['url', 'title', 'file', 'album', 'icon', 'artist', 'is_fav'] # todosloscampos(model, ['lyrics', 's7_user', 'playlist'])
#         depth = 0
#         #fields = ['url', 'title', 'artists', 'album', 'file'] #'__all__'#


class AlbumDetailSerializer(serializers.HyperlinkedModelSerializer):
    #songs = SongSerializer(many=True) #source='album.song_set',
    songs = SongReducedSerializer(many=True)
    class Meta:
        model = Album
        # * convierte la lista en argumentos separados (ej: (*[a,b],c) es equivalente a (a,b,c))
        fields = (*todosloscampos(model), 'songs', 'number_songs') # (*[f.name for f in Album._meta.get_fields()], 'songs')
        depth = 1

# Serializador del album sin artista
class AlbumReducedSerializer(serializers.HyperlinkedModelSerializer):
    #songs = SongListSerializer(many=True)
    class Meta:
        model = Album
        fields = (*todosloscampos(model, ['artist','songs']), 'number_songs') # (*[f.name for f in Album._meta.get_fields()], 'songs')
        depth = 1




class ArtistDetailSerializer(serializers.HyperlinkedModelSerializer):
    albums = AlbumReducedSerializer(many=True)
    class Meta:
        model = Artist
        # * convierte la lista en argumentos separados (ej: (*[a,b],c) es equivalente a (a,b,c))
        fields = (*todosloscampos(model),'number_albums', 'number_songs')
        depth = 1


class S7_userListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = S7_user
        fields = ['url', 'username'] #[*todosloscampos(model, ['group', 'groups'])]#'__all__'#(*todosloscampos(model))
        depth = 0


# Para registrar usuarios, con ayuda de https://stackoverflow.com/questions/16857450/how-to-register-users-in-django-rest-framework
class RegisterUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = S7_user
        fields = ['url', 'username', 'password'] #[*todosloscampos(model, ['group', 'groups'])]#'__all__'#(*todosloscampos(model))
        write_only_fields = ('password',)
        depth = 1

    # Se pueden definir metodos validate_[nombre del campo] en los serializadores
    def validate_password(self, value):
        validators.validate_password(value)
        return value

    def create(self, validated_data):
        user = S7_user.objects.create(
            username=validated_data['username'],
            #email=validated_data['email'], # si a�adimos mas
            # first_name=validated_data['first_name'],
            # last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password']) # usamos set_password por seguridad (guarda un hash)
        user.save()

        return user

class otro(serializers.ModelSerializer):
    class Meta:
        model = S7_user
        fields = ['username']


# TODO: Reducir mucho los campos!
class PlaylistListSerializer(serializers.HyperlinkedModelSerializer):
    user = S7_userListSerializer() # especificamos que use el serializador de lista para user, no hacen falta detalles
    #the_songs = SongListSerializer(source='playlist.songs.all', many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ['url', 'title', 'user', 'icon', 'number_songs']
        depth = 2


class PlaylistDetailSerializer(serializers.HyperlinkedModelSerializer):
    user = S7_userListSerializer() # especificamos que use el serializador de lista para user, no hacen falta detalles
    #the_songs = SongListSerializer(source='playlist.songs.all', many=True, read_only=True)
    songs = SongListMiniSerializer(many=True)
    class Meta:
        model = Playlist
        # artista y foto album y urls
        fields = ['url', 'title', 'user', 'icon', 'songs', 'duration', 'number_songs']
        depth = 3


# class PlaylistDetailSerializer(serializers.HyperlinkedModelSerializer):
#     user = S7_userSerializer() # especificamos que use el serializador de lista para user, no hacen falta detalles
#     #the_songs = SongListSerializer(source='playlist.songs.all', many=True, read_only=True)
#     songs = SongListMiniSerializer(many=True)
#     class Meta:
#         model = Playlist
#         # artista y foto album y urls
#         fields = ['url', 'title', 'user', 'icon', 'songs', 'duration', 'number_songs']
#         depth = 4


#TODO: devolver al menos la url al crear
class PlaylistCreateSerializer(serializers.HyperlinkedModelSerializer):
    user = S7_userListSerializer(default=OurCurrentUserDefault()) # tomamos el s7_user (validacion incluida)
    class Meta:
        model = Playlist
        fields = ['url', 'title', 'user', 'icon']
        read_only_fields = ('user',)
        depth = 1

    # se llama automaticamente con el campo titulo, la usamos para validar el usuario:
    def validate_title(self, title: str) -> str:
        # if no_ok(title): # TODO: validacion de title? long maxima, cosas asi
        #     raise serializers.ValidationError(
        #         ('No estas autentificado!')
        #     )
        return title



class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'
        depth = 2

class PodcastUrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Podcast
        fields = ['url']
        depth = 2

class PodcastEpisodeListSerializer(serializers.HyperlinkedModelSerializer):
    # URI = FinalURIField(many=False)
    podcast = PodcastUrlSerializer()
    class Meta:
        model = PodcastEpisode
        # fields = (*todosloscampos(model,['podcast', 's7_user', 'audio_ptr']), 'real_uri')
        fields = todosloscampos(model,['s7_user', 'audio_ptr'])
        depth = 2

class PodcastDetailSerializer(serializers.HyperlinkedModelSerializer):
    episodes = PodcastEpisodeListSerializer(many=True)
    class Meta:
        model = Podcast
        fields = (*todosloscampos(model,['s7_user','audio_ptr']), 'number_episodes')
        depth = 2

class PodcastListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Podcast
        fields = (*todosloscampos(model, ['episodes', 's7_user', 'audio_ptr','genre']), 'number_episodes')
        depth = 2

class PodcastEpisodeDetailSerializer(serializers.HyperlinkedModelSerializer):
    podcast = PodcastListSerializer()
    class Meta:
        model = PodcastEpisode
        fields = (*todosloscampos(model, ['s7_user', 'audio_ptr']), 'real_uri')
        depth = 2

class GenreSerializer(serializers.HyperlinkedModelSerializer):
    podcasts = PodcastListSerializer(many=True)
    class Meta:
        model = Genre
        fields = ['url', 'name', 'id_listenotes', 'number_podcasts','podcasts']
        depth = 2


#Necesario para devolver los trending podcast dinámicos
# Link: https://medium.com/django-rest-framework/django-rest-framework-viewset-when-you-don-t-have-a-model-335a0490ba6f
class TrendingPodcastsSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=100)
    publisher = serializers.CharField(max_length=100)
    image = serializers.CharField(max_length=256)
    total_episodes = serializers.IntegerField(read_only=True)
    description = serializers.CharField(max_length=256)
    rss = serializers.CharField(max_length=256)
    language = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return TrendingPodcasts(id=None,**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance


# Devuelve o el serializador de detalle de la canción del audio o el del episodio de podcast,
# segun lo que sea el audio dado
class AudioDetailSerializer(serializers.RelatedField):

    # instance es la instancia de la cancion (modelo Song)
    def to_representation(self, instance):
        audio = Song.objects.get(pk=instance.pk)
        is_podcast = audio is None
        if is_podcast:
            audio = PodcastEpisode.objects.get(pk=instance.pk)
            audio = PodcastEpisodeDetailSerializer(source=audio, context=self.context)
            respuesta = {'podcast-ep:', audio.data}
        else:
            audio = SongDetailSerializer(audio, context=self.context)
            respuesta = ('song:', audio.data)

        # print(audio.data)
        return audio.data # TODO: añadir el tipo, se queja de unhashable type: dict


# Devuelve la cancion/podcast que esta reproduciendo (en vista de detalle) junto con su timestamp,
# ademas del nombre de usuario y la url como el s7_userSerializer
class S7_userDetailSerializer(serializers.HyperlinkedModelSerializer):
    playing = AudioDetailSerializer(source='reproduciendo', read_only=True)
    timestamp = serializers.IntegerField(source='segundos')
    following = S7_userListSerializer(source='siguiendo', many=True)
    followers = S7_userListSerializer(source='seguidor', many=True)
    playlists = PlaylistListSerializer(many=True)
    podcast =PodcastListSerializer(source='podcasts', many=True)
    class Meta:
        model = S7_user
        fields = ['url', 'username', 'playing', 'timestamp', 'following', 'podcast','followers', 'icon', 'playlists'] #[*todosloscampos(model, ['group', 'groups'])]#'__all__'#(*todosloscampos(model))
        depth = 0


class S7_userUpdateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = S7_user
        fields = ['url', 'icon']
        read_only_fields = ('url',)
