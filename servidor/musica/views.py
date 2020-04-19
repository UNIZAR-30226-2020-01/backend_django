from django.shortcuts import render, get_object_or_404

# Create your views here.


from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from musica.serializers import *

from musica.models import *

from musica.permissions import IsOwnerOrIsAdmin

from utils.podcasts.podcasts import Podcasts_api

from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import permissions


from rest_framework.generics import CreateAPIView # registros de usuarios

from django.views.decorators.csrf import csrf_exempt

from rest_framework import filters

# En general, usamos viewsets ya que facilitan la consistencia de la API, documentacion: https://www.django-rest-framework.org/api-guide/viewsets/


# Nuevas:
class ArtistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows artists to be viewed.
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
    serializer_class = AlbumListSerializer
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
    # solo acepta GET:
    http_method_names = ['get']
    # usamos SearchFilter para buscar (https://www.django-rest-framework.org/api-guide/filtering/#searchfilter)
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    action_serializers = {
        'retrieve': SongDetailSerializer,
        'list': SongListSerializer,
        #'create': MyModelCreateSerializer
    }

    def get_serializer_class(self):

        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(SongViewSet, self).get_serializer_class()


    # TODO: asegurar que add_favorite no duplique filas
    @action (detail=True, methods=['get'])
    def set_favorite(self, request, pk):
        # Problema: User de Django es DEFAULT_AUTH_USER
        user = self.request.user # Tipo User de Django!
        s7_user = S7_user.objects.get(pk=user.pk) # TODO: ARREGLAR!!!!
        print(user, '------------------', s7_user)
        song = self.get_object()
        # print(song)
        # serializer = SongSerializer(data=request.data)
        # if serializer.is_valid():
        #     user.add_favorite(serializer.data['song'])
        #     user.save()
        # else:
        #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        s7_user.add_favorite(song) # TODO: cambiar por toggle_favorite?
        return Response({'status': 'Maracdo como favorito'})
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643

    # TODO: terminar:
    @action (detail=True, methods=['get'])
    def remove_favorite(self, request, pk):
        # Problema: User de Django es DEFAULT_AUTH_USER
        user = self.request.user # Tipo User de Django!
        s7_user = S7_user.objects.get(pk=user.pk) # TODO: ARREGLAR!!!!
        # TODO: borrar, es solo de prueba:
        if request.user.is_anonymous:
            user = S7_user.objects.first()
        ############## hasta aqui
        song = self.get_object()
        s7_user.remove_favorite(song) # TODO: cambiar por toggle_favorite?
        return Response({'status': 'Eliminado de favoritos'})



class PlaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows all playlists to be viewed.
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistListSerializer # por defectp
    # solo acepta GET:
    http_method_names = ['get', 'post']
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643

    action_serializers = {
        'retrieve': PlaylistDetailSerializer,
        'list': PlaylistListSerializer,
        'create': PlaylistCreateSerializer
    }

    def get_serializer_class(self):
        print('accion:',self.action)
        if hasattr(self, 'action_serializers'):
            #
            # try:
            serializador = self.action_serializers.get(self.action, self.serializer_class)
            print('usando: ', serializador)
            return serializador
            # except KeyError, AttributeError:
        return super(PlaylistViewSet, self).get_serializer_class()


    @action (detail=True, methods=['post'], permission_classes=[IsOwnerOrIsAdmin])
    def add_song(self, request, pk):
        # Problema: User de Django es DEFAULT_AUTH_USER
        # user = self.request.user # Tipo User de Django!
        # s7_user = S7_user.objects.get(pk=user.pk) # TODO: ARREGLAR!!!!
        # print(user, '------------------', s7_user)
        playlist = self.get_object()

        songurl = self.request.query_params.get('song', None)
        print(songurl)
        songpk = songurl.split('/')[-2]
        song = get_object_or_404(Song, pk=songpk)#Song.objects.get_object_or_404(pk=songpk) # si no existe devuelve 404
        print(playlist, '.....', songpk, song)
        playlist.add_song(song)
        estado = 'Añadida ' + str(song) + ' a ' + str(playlist) # TODO: que diga "ya estaba" si ya estaba
        return Response({'status': estado})
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643



class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    http_method_names = ['get']

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

    http_method_names = ['get']

class UserFavoritesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows all playlists to be viewed.
    """
    #queryset = Playlist.objects.all()

    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SongDetailSerializer
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
        return user.favorito.all()

class UserPlaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows all playlists to be viewed.
    """
    #queryset = Playlist.objects.all()

    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PlaylistListSerializer
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

####################### Work in progress #######################
class SearchAPIView(APIView):
    """
    API endpoint that allows to search stuff.
    """
    #queryset = Song.objects.all()
    #serializer_class = SongSerializer
    # # solo acepta GET:
    # http_method_names = ['get']
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Song.objects.all()
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)
        return queryset


    def get(self, request, format=None, **kwargs):
        songs = Song.objects.all()
        serializer = SongSerializer(song)
        # Can't I append anything to serializer class like below ??
        # serializer.append(anotherserialzed_object) ??
        return Response(serializer.data)



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



class CurrentUserView(viewsets.ModelViewSet):
    serializer_class = S7_userSerializer
    authentication_classes = [TokenAuthentication]
    # solo acepta GET:
    http_method_names = ['get']
    def get_queryset(self):
        """
        This view returns the currently authenticated user.
        """
        user = self.request.user
        print("Usuario en request: ", user)
        return S7_user.objects.filter(pk=user.pk)


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

# Para registros de usuarios
class RegisterUserView(CreateAPIView):
    authentication_classes = [] # desactivar comprobacion de CSRF
    model = S7_user
    permission_classes = [
        permissions.AllowAny # usuarios anónimos se tienen que poder registrar
    ]
    serializer_class = RegisterUserSerializer
