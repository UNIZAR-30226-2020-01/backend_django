from django.shortcuts import render, get_object_or_404

# Create your views here.


from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from musica.serializers import *

from musica.models import *

from musica.permissions import IsOwnerOrIsAdmin

from utils.podcasts.podcasts import Podcasts_api

from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import status # mas info en errores de http
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import permissions


from rest_framework.generics import CreateAPIView, UpdateAPIView # registros y updates de usuarios

from django.views.decorators.csrf import csrf_exempt

from rest_framework import filters


from django.db.models import Prefetch

from utils.debug.connections import num_queries

import numpy as np
import html2text
import json
# En general, usamos viewsets ya que facilitan la consistencia de la API, documentacion: https://www.django-rest-framework.org/api-guide/viewsets/

def get_real_uri(url):
    real_uri = requests.get(url)
    url = real_uri.url
    return url


# Para permitir paginacion en views y viewsets que no sean genericos, hacemos que
# hereden de este mixin:
# Fuente: https://stackoverflow.com/a/45670649
# class MyPaginationMixin(object):
#     @property
#     def paginator(self):
#         """
#         The paginator instance associated with the view, or `None`.
#         """
#         if not hasattr(self, '_paginator'):
#             if self.pagination_class is None:
#                 self._paginator = None
#             else:
#                  self._paginator = self.pagination_class()
#         return self._paginator
#
#      def paginate_queryset(self, queryset):
#          """
#          Return a single page of results, or `None` if pagination
#          is disabled.
#          """
#          if self.paginator is None:
#              return None
#          return self.paginator.paginate_queryset(
#              queryset, self.request, view=self)
#
#      def get_paginated_response(self, data):
#          """
#          Return a paginated style `Response` object for the given
#          output data.
#          """
#          assert self.paginator is not None
#          return self.paginator.get_paginated_response(data)



# Nuevas:
class ArtistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows artists to be viewed.
    Allows searches using the search queryparameter (/?search=something)
    Retrieves artists with a substring of the parameter in the artist's name
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistListSerializer # por defecto lista
    # solo acepta GET:
    http_method_names = ['get']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    action_serializers = {
        'retrieve': ArtistDetailSerializer,
        'list': ArtistListSerializer,
        #'create': MyModelCreateSerializer
    }

    def get_serializer_class(self):

        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(MyModelViewSet, self).get_serializer_class()

    # def get_queryset(self):
    #     if self.action=='list':
    #         return Artist.objects.only('id', 'name', 'image', 'biography')
    #     else:
    #         print('???')
    #         return self.queryset.prefetch_related('albums', 'featured_in_album')

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
    Allows searches using the search queryparameter (/?search=something)
    Retrieves albums with a substring of the parameter in either the title
    or the album's artist's name
    """
    queryset = Album.objects.all().select_related('artist').prefetch_related('songs')
    serializer_class = AlbumListSerializer
    http_method_names = ['get']
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'artist__name']
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
    Allows searches using the search queryparameter (/?search=something)
    Retrieves songs with a substring of the parameter in either the title
    or the song's artist's name
    """
    queryset = Song.objects.select_related('album__artist').all()
    serializer_class = SongListSerializer
    # solo acepta GET:
    http_method_names = ['get']
    # usamos SearchFilter para buscar (https://www.django-rest-framework.org/api-guide/filtering/#searchfilter)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'album__artist__name']
    # filter_backends = []
    ordering_fields = ['times_played', 'times_faved']
    action_serializers = {
        'retrieve': SongDetailSerializer,
        'list': SongListSerializer,
        #'create': MyModelCreateSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            print('eligiendo serializador... num_queries:')
            serializador = self.action_serializers.get(self.action, self.serializer_class)
            num_queries(False)
            return serializador
        return super(SongViewSet, self).get_serializer_class()

    # def get_queryset(self):
    #     if self.action == 'retrieve':
    #         queryset = Song.objects.all()
    #         print('get_queryset')
    #     return super(SongViewSet, self).get_serializer_class()

    # Test de velocidad
    # def list(self, request):
    #     # global serializer_time
    #     # global db_time
    #     #
    #     # db_start = time.time()
    #     # users = list(User.objects.all())
    #     # db_time = time.time() - db_start
    #     #
    #     # serializer_start = time.time()
    #     # serializer = UserSerializer(users)
    #     # data = serializer.data
    #     # serializer_time = time.time() - serializer_start
    #     self.queryset = Song.objects.all().select_related('album__artist')
    #     print('antes del serializador:')
    #     page = self.paginate_queryset(self.queryset)
    #     num_queries(False)
    #     serializer = SongListSerializer(page, context={'request': request}, many=True)
    #     data = serializer.data
    #     print('queries en get:')
    #     num_queries()
    #     return Response(data)

    def retrieve(self, request, pk=None):
        song = self.queryset.select_related('album', 'album__artist', 'audio_ptr').get(pk=pk)
        # Song.objects.prefetch_related('album__artist').get(pk=pk)#.prefetch_related('album__artist')
        print('antes del serializador:')
        num_queries(False)
        serializer = SongDetailSerializer(song, context={'request': request})
        data = serializer.data
        print('retrieve:')
        num_queries()
        return Response(data)

    # TODO: asegurar que add_favorite no duplique filas
    @action (detail=True, methods=['get'])
    def set_favorite(self, request, pk):
        # Problema: User de Django es DEFAULT_AUTH_USER
        user = self.request.user # Tipo User de Django!
        s7_user = S7_user.objects.get(pk=user.pk) # TODO: ARREGLAR!!!!
        print(user, '------------------', s7_user)
        song = self.get_object()
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

    # Añade esta cancion a 'reproduciendo' del usuario actual
    # Ademas, si t=0 significa que el usuario ha pasado a la siguiente cancion, por lo
    # que le contamos la reproduccion
    @action (detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def set_playing(self, request, pk):
        '''
        Saves the song as the user's currently playing song with the timestamp in the
        t queryparam (?t=123) in seconds
        '''
        # Problema: User de Django es DEFAULT_AUTH_USER
        user = self.request.user # Tipo User de Django!
        s7_user = S7_user.objects.get(pk=user.pk)
        print(user, '------------------', s7_user)
        song = self.get_object()

        timestamp = self.request.query_params.get('t', None) # en segundos!
        if timestamp is None: # por defecto, 0
            timestamp = 0
        else: # si no, lo pasamos a entero
            timestamp = int(timestamp)
        s7_user.set_playing(song, timestamp)
        return Response({'status': 'Saved as playing', 'user': str(s7_user), 'song': str(song), 'timestamp (s)': timestamp})
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows all playlists to be viewed.
    Allows searches using the search queryparameter (/?search=something)
    Retrieves playlsits with a substring of the parameter in either the title
    or the playlist's user's username
    """
    # TODO: arreglar esto de prefetch_related/select_related:
    # el eager loading puede mejorar mucho la eficiencia reduciendo el numero de queries
    queryset = Playlist.objects.all().prefetch_related('songs')#,'songs__audio__file')#, 'songs__file', 'songs__album__title', 'songs_album__icon')#.select_related('songs__album__artist__name')
    serializer_class = PlaylistListSerializer # por defectp
    # solo acepta GET:
    http_method_names = ['get', 'post']
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'user__username']

    action_serializers = {
        'retrieve': PlaylistDetailSerializer,
        'list': PlaylistListSerializer,
        'create': PlaylistCreateSerializer
    }

    def get_serializer_class(self):
        # print('accion:',self.action)
        if hasattr(self, 'action_serializers'):
            # try:
            serializador = self.action_serializers.get(self.action, self.serializer_class)
            # print('usando: ', serializador)
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

    queryset = Genre.objects.all().prefetch_related('podcasts__episodes', 'podcasts__channel')#.prefetch_related('podcast__episode')
    serializer_class = GenreSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    # filter_backends = []
    ordering_fields = ['number_podcasts']

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

    authentication_classes = [TokenAuthentication, BasicAuthentication, OAuth2Authentication]
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
        return user.s7_user.favorito.songs.all()

class UserPlaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows the current user's playlists to be viewed.
    Allows searches using the title queryparameter (/?title=something)
    """
    #queryset = Playlist.objects.all()

    authentication_classes = [TokenAuthentication, BasicAuthentication, OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

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

class UserRecomendedPodcast(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication, BasicAuthentication, OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    serializer_class = TrendingPodcastsSerializer

    http_method_names = ['get']

    def list(self, request):
        user = self.request.user
        authent_user = S7_user.objects.get(pk=user.pk) # usuario autentificado
        podcast = authent_user.podcasts.all()
        try:
            to_recommend = podcast[0]
            api = Podcasts_api()
            result = api.get_podcast_recommendation(to_recommend.id_listenotes)
            if result != 'ERROR':
                serializer = TrendingPodcastsSerializer(
                    instance=result, many=True)
                return Response(serializer.data)
            else:
                return Response({'ERROR': "El id no es valido"}, status = status.HTTP_400_BAD_REQUEST)
            return Response(result)
        except Exception as e:
            return Response({'ERROR': 'El usuario no está suscrito a ningún podcast', 'User': user.username},status = status.HTTP_400_BAD_REQUEST)

        # return Response([prueba1, prueba2])
        return Response({'Hola': 'funciona', 'User': user.username})

class UserPodcastsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows the current user's podcasts to be viewed.
    Allows searches using the title queryparameter (/?title=something)
    And (/?genre=something)
    """
    #queryset = Playlist.objects.all()

    authentication_classes = [TokenAuthentication, BasicAuthentication, OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'genre']

    serializer_class = PodcastListSerializer
    # solo acepta GET:
    http_method_names = ['get','post']
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643

    # Sobreescribimos el método que devuelve el queryset, para que de las
    # playlists del usuario autentificado
    #(basado en https://www.django-rest-framework.org/api-guide/filtering/#django-rest-framework-full-word-search-filter)
    def get_queryset(self):
        """
        This view should return a list of all the podcats
        for the currently authenticated user.
        """
        user = self.request.user
        print("Usuario en request: ", user)
        return user.s7_user.podcasts.all()

    @action (detail=False, methods=['post', 'get'], permission_classes=[IsAuthenticated])
    def followPodcast(self, request):
        """
        This view save the Podcast indicated on the request and its episodes
        and add the podcast to the podcast list of the user.
        """
        user = self.request.user
        authent_user = S7_user.objects.get(pk=user.pk) # usuario autentificado
        print('USER:', authent_user)

        pod_id = self.request.query_params.get('id', None)

        #Ahora se comprueba si el podcast pertenece a la base de datos
        pod_object = Podcast.objects.filter(id_listenotes = pod_id)

        #No existe, así que se introduce el podcast y sus episodios
        if not pod_object:
            #Si no aparece en la BD, se busca con la api
            api = Podcasts_api()
            podcast, episodes = api.get_allEpisodes(pod_id) #Para que devuelve todos episodios
            if podcast == 'ERROR':
                return Response({'ERROR': "El id no es valido"}, status = status.HTTP_400_BAD_REQUEST)
            pod_rss = podcast['rss']
            pod_genres =  podcast['genre_ids']
            pod_title = podcast['title']
            pod_image = podcast['image']
            pod_channel = podcast['publisher']
            # titles = [ep['title'] for ep in episodes]
            print("Num. Episodios: ", len(episodes))

            #Primero se almacena el canal (en caso de que no exista con anterioridad)
            new_chan = Channel.objects.filter(name = pod_channel)
            if not new_chan:
                new_chan = Channel(name=pod_channel)
                new_chan.save()
                print('Canal almacenado')
            else:
                new_chan=new_chan[0] #Filter devuelve una lista

            #Ahora creamos un nuevo objeto de Podcast
            pod = Podcast(title=pod_title, RSS=pod_rss, id_listenotes=pod_id,
                image=pod_image, channel=new_chan)

            pod.save()

            #Recorremos los generos y se los introducimos al podcast
            for gen in pod_genres:
                # Esto ha sido error de inserción. Hay varios generos iguales(mismo id)
                found = Genre.objects.get(id_listenotes=gen)
                pod.genre.add(found)

            pod.save()

            authent_user.podcasts.add(pod)
            authent_user.save()

            print('Podcast almacenado')

            # Esto se hace porque
            lista_separada = [episodes]
            if len(episodes) > 10:
                i = len(episodes) // 10
                lista_separada = np.array_split(episodes, i+1)

            for episodes in lista_separada:
                ids = [ep['id'] for ep in episodes]
                # print('IDS:', ids)

                ids = ','.join(ids)
                episodes = api.get_many_episodes(ids)

                #print(episodes)

                for epi in episodes:
                    ep_audio = epi['audio']
                    ep_id = epi['id']
                    ep_title = epi['title']
                    ep_duration = epi['audio_length_sec']
                    ep_image = epi['image']
                    ep_description = epi['description']

                    #Se debe convertir el HTML a texto
                    parsed_description = html2text.html2text(ep_description)
                    # saved_imag = save_image(ep_image, ep_id, 'episode')
                    epi = PodcastEpisode(title=ep_title, duration = ep_duration,
                        URI = ep_audio, id_listenotes=ep_id, podcast=pod, image=ep_image, description=parsed_description)
                    epi.save()
                    print('Episodio almacenado: ' + ep_title)

        else:
            podcast = authent_user.podcasts.filter(id_listenotes = pod_id)
            if podcast:
                print("El user ya sigue a este podcast")
                return Response({'Bad request': "This podcast is already followed by the user"}, status = status.HTTP_400_BAD_REQUEST)
            else:
                pod_object = pod_object[0]
                authent_user.podcasts.add(pod_object)
                authent_user.save()
                print("Ahora se sigue al podcast")

        estado = 'Añadido ' + pod_id+ ' a ' + authent_user.username # TODO: que diga "ya estaba" si ya estaba
        return Response({'status': estado})

    @action (detail=False, methods=['post'])
    def unfollowPodcast(self, request):
        user = self.request.user
        authent_user = S7_user.objects.get(pk=user.pk) # usuario autentificado
        print('USER:', authent_user)
        pod_id = self.request.query_params.get('id', None)
        podcast = authent_user.podcasts.filter(id_listenotes = pod_id)
        if podcast:
            podcast = podcast[0]
            authent_user.podcasts.remove(podcast)
            authent_user.save()
            print("El usuario ya no sigue el podcast")
            return Response({'status': 'Ok'})
        else:
            print("El usuario no esta suscrito al podcast")
            return Response({'Bad request': "The user isn't subscribed to this podcast"}, status = status.HTTP_400_BAD_REQUEST)


class FollowedPlaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows the playlists of the users followed by the current
    user to be viewed.
    Allows searches using the title queryparameter (/?title=something)
    """
    #queryset = Playlist.objects.all()

    authentication_classes = [TokenAuthentication, BasicAuthentication, OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

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
        user = S7_user.objects.get(pk=user.pk) # como s7_user
        return Playlist.objects.filter(user__in=user.siguiendo.all()) # playlists cuyo user es uno de los que sigues

class PodcastViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows podcasts to be viewed.
    """
    queryset = Podcast.objects.all().prefetch_related(Prefetch('episodes', queryset=PodcastEpisode.objects.order_by('title')))
    action_serializers = {
        'retrieve': PodcastDetailSerializer,
        'list': PodcastListSerializer,
        #'create': MyModelCreateSerializer
    }
    # solo acepta GET:
    http_method_names = ['get']
    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643


    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'genre__name']

    def get_serializer_class(self):

        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(PodcastViewSet, self).get_serializer_class()

    @action (detail=False, methods=['get'])
    def search(self, request):
        # user = self.request.user
        # authent_user = S7_user.objects.get(pk=user.pk) # usuario autentificado
        # print('USER:', authent_user)
        pod_title = self.request.query_params.get('title', None)
        pod_genre = self.request.query_params.get('genre', None)
        api = Podcasts_api()
        podcast = api.search(query=pod_title, genres=pod_genre) #Para que devuelve todos episodios
        if podcast != 'ERROR':
            print("Devolviendo podcasts")
            podcast = podcast["results"]
            return Response(podcast)
        else:
            print("No existen podcasts")
            return Response({'ERROR': "No podcast retreived"}, status = status.HTTP_400_BAD_REQUEST)

class PodcastEpisodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songs to be viewed.
    """
    queryset = PodcastEpisode.objects.all()
    action_serializers = {
        'retrieve': PodcastEpisodeDetailSerializer,
        'list': PodcastEpisodeListSerializer,
        #'create': MyModelCreateSerializer
    }
    # solo acepta GET:
    http_method_names = ['get']

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'podcast__title', 'podcast__genre__name']

    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643
    def get_serializer_class(self):

        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(PodcastEpisodeViewSet, self).get_serializer_class()
####################### Work in progress #######################
class SearchAPIView(APIView):
    """
    API endpoint that allows to search stuff.
    """
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
    serializer_class = S7_userDetailSerializer
    authentication_classes = [TokenAuthentication, OAuth2Authentication]
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
    API endpoint that allows to see users and search them through
    """
    authentication_classes = [TokenAuthentication, BasicAuthentication, OAuth2Authentication]
    #permission_classes = [IsAuthenticated]
    queryset = S7_user.objects.all().order_by('-date_joined')
    serializer_class = S7_userListSerializer


    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'playlists__title']

    # solo acepta GET:
    http_method_names = ['get', 'post']

    action_serializers = {
        'retrieve': S7_userDetailSerializer,
        'list': S7_userListSerializer,
        'update': S7_userUpdateSerializer,
        #'create': MyModelCreateSerializer
    }

    # fuente de la soluci贸n: https://stackoverflow.com/a/31450643
    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)

    # diferenciar retrieve y list
    def get_serializer_class(self):

        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(S7_userViewSet, self).get_serializer_class()



    @action (detail=True, methods=['get'])
    def follow(self, request, pk):
        """
        After executing, the currently authenticated user will follow this user
        """
        # Problema: User de Django es DEFAULT_AUTH_USER
        user = self.request.user
        authent_user = S7_user.objects.get(pk=user.pk) # usuario autentificado
        print(user, '------------------', authent_user)
        this_user = self.get_object() # usuario a seguir
        if this_user == authent_user:
            return Response({'silly request': "You can\'t follow yourself"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            authent_user.follow(this_user)
            return Response({'status': 'Ok'})

    @action (detail=True, methods=['get'])
    def unfollow(self, request, pk):
        """
        After executing, the currently authenticated user will stop following this user
        """
        # Problema: User de Django es DEFAULT_AUTH_USER
        user = self.request.user
        authent_user = S7_user.objects.get(pk=user.pk) # usuario autentificado
        print(user, '------------------', authent_user)
        this_user = self.get_object() # usuario a seguir
        if this_user == authent_user:
            return Response({'silly request': 'You can\'t unfollow yourself'}, status = status.HTTP_400_BAD_REQUEST)
        else:
            authent_user.unfollow(this_user)
            return Response({'status': 'Ok'})

#Para trending podcast mediante router
class TrendingPodcastsViewSet(viewsets.ViewSet):
    serializer_class = TrendingPodcastsSerializer

    def list(self, request):
        #Obtenemos los podcast recomendados dinámicamente
        api = Podcasts_api()
        result = api.get_bestpodcast()
        serializer = TrendingPodcastsSerializer(
            instance=result, many=True)
        # page = self.paginate_queryset(self.queryset)
        # if page is not None:
        #     serializer = self.serializer_class(page, many=True)
        #     return self.get_paginated_response(serializer.data)

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
        if result != 'ERROR':
            ep_url = result['audio']
            print('URL:', ep_url)
            result['real_uri'] = get_real_uri(ep_url)
            return Response(result)
        else:
            return Response({'ERROR': "El id no es valido"}, status = status.HTTP_400_BAD_REQUEST)

class debugAuthViewSet(viewsets.ModelViewSet):
    """
    Endpoint provisional para debuguear auth (basicamente como s7-user pero requiere token)
    """
    authentication_classes = [TokenAuthentication, BasicAuthentication, OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    queryset = S7_user.objects.all().order_by('-date_joined')
    serializer_class = S7_userListSerializer
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


class UpdateUserView(UpdateAPIView):
    authentication_classes = [TokenAuthentication, OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = S7_userUpdateSerializer

    lookup_field = 'user'

    # http_method_names = ['post']
    def get_object(self): # get_object en lugar de queryset porque es un solo objeto
        """
        This view returns the currently authenticated user.
        """
        user = self.request.user # el de django
        print("Usuario en request: ", user)
        return S7_user.objects.filter(pk=user.pk).first() # el nuestro
