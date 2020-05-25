# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from utils.lyrics.lyrics import Lyrics_api
from utils.spotipy.spotiapi import Spotisearcher
from utils.podcasts.podcasts import Podcasts_api
from utils.biography.biography import LastfmSearcher
import html2text
import requests

from django.db.models.signals import post_save
from django.dispatch import receiver
# para señales (ahora no las usamos):
# from django.db.models.signals import post_save
# from django.dispatch import receiver

import os.path

class Artist(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, blank=True)
    image = models.FileField(null=True, blank=True)
    biography = models.TextField(blank=True)

    @property
    def number_songs(self):
        return sum([l.number_songs for l in self.albums.all()])

    @property
    def number_albums(self):
        return self.albums.count()


    def __init__(self, *args, **kwargs):
        super(Artist, self).__init__(*args, **kwargs)

        #Comprobamos que no tenga una imagen asignada previamente.
        if not self.image:
            api = Spotisearcher()
            self.image = api.get_artist_image(self.name)

        #Automatización de biografía (en caso de que no posea una)
        if not self.biography:
            api = LastfmSearcher()
            result = api.get_biography(self.name)
            #El resultado de la api es html, asi que lo conertimos a texto plano
            self.biography = html2text.html2text(result)

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(Artist, self).save()

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'Artist'

class Album(models.Model):
    TIPOS_ALBUM = (
        ('N', 'Normal'),
        ('EP', 'EP'),
        ('S', 'Single'),
    )
    title = models.CharField(max_length=100)
    date = models.DateField(db_column='fecha')  # Field name made lowercase.
    icon = models.FileField(blank=True)
    type = models.CharField(max_length=2, choices=TIPOS_ALBUM)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums') # principal
    other_artists = models.ManyToManyField(Artist, blank=True, related_name='featured_in_album') # otros

    @property
    def number_songs(self):
        return self.songs.count()

    class Meta:
        managed = True
        db_table = 'Album'

    def __str__(self):
        return self.title

class Genre(models.Model):
    name = models.CharField(max_length=50)
    id_listenotes = models.IntegerField(default=0, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'Genre'

class Channel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        managed = True
        db_table = 'Channel'

    def __str__(self):
        return self.name

class Podcast(models.Model):
    title = models.CharField(max_length=300)
    RSS = models.URLField()
    genre = models.ManyToManyField(Genre, blank=True, related_name='podcasts')
    id_listenotes = models.CharField(max_length=50, unique=True)
    image = models.URLField(null=True, blank=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='podcasts')

    @property
    def number_episodes(self):
        return len(self.episodes.all())

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'Podcast'

#Clase padre de Song y Podcast. Es abstracta para evitar que se cree una tabla de este tipo.
class Audio(models.Model):
    ##id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    file = models.FileField(blank=True, null=True)
    duration = models.IntegerField(default=0)
    # album = models.ForeignKey(Album, models.DO_NOTHING, db_column='album') # los podcasts no tienen album


    # Ahora esta funcion es inutil, la dejo por si acaso
    def is_song(self):
        #is_song = False
        #try:
        #is_song = self.tipo.get_tipo() == 'Song'
        #except tipoAudio.DoesNotExist:
        #    pass

        # Pruebo con introspeccion mejor (ej en https://medium.com/better-programming/python-reflection-and-introspection-97b348be54d8):
        is_song = type(self) is Song
        return is_song

    def __str__(self):
        return self.title

    # Version anterior, usando señales (la dejo por si nos es util mas tarde)
    # @receiver(post_save, sender=Audio)
    # def buscar_letra(sender, **kwargs):
    #     es_cancion = True # esto habra que cambiarlo
    #     if es_cancion: # que solo ponga letras a las canciones, no a los podcasts
    #         api = Lyrics_api()
    #         letra = api.get_lyrics(instance.title, instance.artist)
    #         print(letra)
    #         if letra != '':
    #             instance.letra = letra
    #         else:
    #             exit(1)

    # def ready(self): # intento de que se añada la musica
    #     import musica.signals

    class Meta:
        managed = True
        db_table = 'Audio'


# TODO: mas blank=True pls
class S7_user(User):
    podcasts = models.ManyToManyField(Podcast, blank=True)
    siguiendo = models.ManyToManyField('self', symmetrical=False, related_name='seguidor', blank=True)
    #seguido = models.ManyToManyField('self', symmetrical=False, related_name='seguido')
    reproduciendo = models.ForeignKey(Audio, on_delete=models.CASCADE, null=True, blank=True)
    segundos = models.IntegerField(null=True, default=0) # segundo de reproduccion del audio guardado
    favorito = models.ForeignKey('Playlist', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='fav_user')
    icon = models.FileField(default='../static/default-user-pic.png') # imagen por defecto de https://images.app.goo.gl/JR5TrAxvf8eLbbCx5
    class Meta:
        managed = True
        db_table = 'S7_user'

    def add_favorite(self, song):
        song.count_fav()
        self.favorito.songs.add(song)
        song.save()

        #self.favorito.add(song)

    def remove_favorite(self, song):
        self.favorito.songs.remove(song)
    # def __str__(self):
    #     return self.name

    # guarda la canción song y los segundos timestamp como los que está reproduciendo el usuario (para sincronización, etc)
    # ademas, si el t=0, se cuenta una reproduccion de la cancion:
    def set_playing(self, song, timestamp):
        self.reproduciendo = song
        self.segundos = timestamp
        if timestamp == 0: # si t=0, contamos una reproduccion
            song.count_play()
            song.save()
        self.save()

    # Añade "other_user" a los seguidos por self
    def follow(self, other_user):
        assert(self!=other_user) # no te puedes seguir a ti mismo
        self.siguiendo.add(other_user)

    # Añade "other_user" a los seguidos por self
    def unfollow(self, other_user):
        assert(self!=other_user) # no te puedes seguir a ti mismo
        self.siguiendo.remove(other_user)


    # save debe conservar los pars originales, para no especificarlos explicitamente podemos usar
    # args y kwargs (ej: https://stackoverflow.com/a/58157374):
    def save(self, *args, **kwargs):# antiguos parametros: , force_insert=False, force_update=False, commit=True):

        #super(S7_user,self).save(*args, **kwargs)
        if not self.pk: #Comprobamos que no exista: https://stackoverflow.com/questions/2307943/django-overriding-the-model-create-method
            print('Creando user ...')
            name = 'favorite_' + self.username
            super(S7_user,self).save(*args, **kwargs)
            lista_fav = Playlist(title=name, user=self, icon='../static/default-fav-image.jpg') #Creamos la playlist
            lista_fav.save()
            self.favorito = lista_fav
            self.save()
        else:
            print('pues si fijate que bien')
            super(S7_user, self).save(*args, **kwargs)
            print('ah, no')
        #print("Listas: " + self.lists)

    # inicializa el usuario en caso de que se creara antes User (no es lo habitual)
    def create_from_user(self, user):
        # self.pk = user.pk
        # user.save()
        print(user.username, user.pk)
        self.pk = user.pk
        print('Creando s7_user a partir de User:', user)
        name = 'favorite_' + user.username
        lista_fav = Playlist(title=name, user=self, icon='../static/default-fav-image.jpg') #Creamos la playlist
        lista_fav.save()
        self.favorito = lista_fav
        self.save()



# Para aĂąadir un usuario a s7_user cada vez que se aĂąada a User de Django
# (no podemos modificar su metodo save)
# Fuente: https://books.agiliq.com/projects/django-orm-cookbook/en/latest/update_denormalized_fields.html
@receiver(post_save, sender=User, dispatch_uid="add_s7_user")
def add_s7_user(sender, **kwargs):
    user = kwargs['instance']
    # created = kwargs['created']
    # print(S7_user.objects.filter(pk=user.pk).exists())
    # print('created:', created)
    # print('superuser:', user.is_superuser)
    if user.pk and not S7_user.objects.filter(pk=user.pk).exists() and not user.is_superuser: # si existe el usuario pero no el s7_user (y no es un admin)
        print('creating s7_user from', str(user))
        # Category.objects.filter(pk=hero.category_id).update(hero_count=F('hero_count')+1)
        s7_user = S7_user(pk=user.pk, username=user.username)
        s7_user.create_from_user(user)
        s7_user.save()

class Song(Audio):
    track = models.IntegerField()
    times_played = models.IntegerField(default=0)
    lyrics = models.TextField(blank=True)
    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE)
    times_faved = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'Song'

    # No se puede ordenar por propiedades en las views
    # @property
    # def times_faved(self):
    #     print('veces fav:', S7_user.objects.favorito.songs.filter(pk=self.pk).count())
    #     return S7_user.objects.favorito.songs.filter(pk=self.pk).count()# self.songs.count()

    def count_fav(self):
        self.times_faved += 1

    def __init__(self, *args, **kwargs):
        super(Song, self).__init__(*args, **kwargs)
        # es_cancion = self.is_song() # obviamente las canciones son canciones
        # if es_cancion: # que solo ponga letras a las canciones, no a los podcasts
        api = Lyrics_api()

        letra= 'TEST' # TEMPORAL

        try:
            # TODO: planificar otra busqueda si la primera falla y/o probar otra(s) API(s)
            # Metodo antiguo: concatenar todos sus artistas:
            # artistas = self.album.artists.all() # queryset de artistas del album de esta cancion
            # artistas_str = ' '.join([str(artista) for artista in artistas]) # en string, sus nombres separados por espacios
            artista = str(self.album.artist)
            letra = api.get_lyrics(self.title, artista)
        except Album.DoesNotExist: # otro gestion de excepciones posible
            pass

        #print(letra)
        if letra != '':
            self.lyrics = letra
        else: # revisar
            exit(1)

        # if self.initial.get('account', None):
        #     self.fields['customer'].queryset = Customer.objects.filter(account=self.initial.get('account'))

    # cuenta <play> reproducciones de la cancion:
    def count_play(self, play=1):
        self.times_played += play

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(Song, self).save()#commit=False)
        #print("Listas: " + self.lists)


    def __str__(self):
        return self.title

    # TODO: EFICIENCIA, es muy lenta
    # Como ahora depende de la playlist, se busca si pertenece a la playlist favorita del user
    def is_favorite_of(self, user):
        #return user in self.user.all() # ineficiente, se supone que exists es mejor (https://docs.djangoproject.com/en/3.0/ref/models/querysets/#exists) :
        #return self.user.filter(id=user.id).exists()
        if user.is_anonymous:
            s7user = S7_user.objects.first()
        else:
            s7user = S7_user.objects.get(pk=user.pk)

        return self in s7user.favorito.songs.all() ## TODO: ¿alguna forma más eficiente?

    # Cuenta una reproduccion
    def play(self):
        self.times_played += 1

##TODO: hay que hacer que las playlist tenga owner, tuto de autenticacion
## de django como referencia https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
class Playlist(models.Model):
    title = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(S7_user, on_delete=models.CASCADE, related_name='playlists')
    icon = models.FileField(blank=True)
    songs = models.ManyToManyField(Song, blank=True, related_name='playlists')

    @property
    def duration(self):
        return sum([s.duration for s in self.songs.all()])

    @property
    def number_songs(self):
        return self.songs.count()

    def __str__(self):
        return self.title

    # Añade la cancion song a la playlist
    def add_song(self, song):
        self.songs.add(song)


    class Meta:
        managed = True
        db_table = 'Playlist'

class Folder(models.Model):
    title = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(S7_user, on_delete=models.CASCADE, blank=True) #TODO: quitar blank de aqui, es para una prueba
    icon = models.FileField(blank=True)
    playlists = models.ManyToManyField(Playlist, related_name='folder')

    class Meta:
        managed = True
        db_table = 'Folder'
    def __str__(self):
        return self.title

class PodcastEpisode(Audio):
    URI = models.URLField()
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='episodes')
    id_listenotes = models.CharField(max_length=50, unique=True)
    image = models.URLField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        managed = True
        db_table = 'PodcastEpisode'


    # TODO: Tiene que devolver la uri del recurso real al que lleva el 302 de listennotes
    @property
    def real_uri(self):
        # algo como get_uri_real(self.URI)
        extensiones = ['.m4a', '.mp3'] # extensiones que aceptamos
        extension = os.path.splitext(self.URI)[1] # obtenemos la extension
        if extension in extensiones:
            print(extension, 'esta en ', extensiones)
            url = self.URI # ya tiene formato ok
        else: # no lo tiene
            print('busco', extension)
            real_uri = requests.get(self.URI)
            url = real_uri.url
        return url
