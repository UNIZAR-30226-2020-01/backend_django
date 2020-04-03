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
# para señales (ahora no las usamos):
# from django.db.models.signals import post_save
# from django.dispatch import receiver

class Artist(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, blank=True)
    image = models.FileField(null=True, blank=True)
    biography = models.TextField(blank=True)
    # biografia no necesita null porque al ser texto en la bd sera '' ()https://stackoverflow.com/a/8609425

    #albumes = models.ManyToManyField(Album) # cambiado a album

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
    number_songs = models.IntegerField(default=0) # TODO: implementar actualizacion automatica, pensar en a�adirlo a playlist
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums') # principal
    other_artists = models.ManyToManyField(Artist, blank=True, related_name='featured_in_album') # otros


    class Meta:
        managed = True
        db_table = 'Album'

    def __str__(self):
        return self.title

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'Genre'

class Podcast(models.Model):
    title = models.CharField(max_length=50)
    RSS = models.FileField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, default='')

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

class S7_user(User):
    podcasts = models.ManyToManyField(Podcast)
    siguiendo = models.ManyToManyField('self', symmetrical=False, related_name='seguidor')
    #seguido = models.ManyToManyField('self', symmetrical=False, related_name='seguido')
    reproduciendo = models.ForeignKey(Audio, on_delete=models.CASCADE, null=True)
    segundos = models.IntegerField(null=True) # segundo de reproduccion del audio guardado
    favorito = models.ManyToManyField(Audio, related_name='favorito')

    class Meta:
        managed = True
        db_table = 'S7_user'

    def __str__(self):
        return self.name

class Folder(models.Model):
    title = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(S7_user, on_delete=models.CASCADE)
    icon = models.FileField(blank=True)

    class Meta:
        managed = True
        db_table = 'Folder'
    def __str__(self):
        return self.title


class Song(Audio):
    track = models.IntegerField()
    times_played = models.IntegerField(default=0)
    lyrics = models.TextField(blank=True)
    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE)
    duration = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'Song'

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


    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(Song, self).save()#commit=False)
        #print("Listas: " + self.lists)

        for lista in self.playlist_set.all():
            print("Duracion antes de actualizar: %s" % lista.duration)
            lista.duration = lista.duration + self.duration
            print("Duracion despues de actualizar: %s" % lista.duration)
            lista.save()
        # my custom code was here

        # if commit:
        #     m.save()
        return m
##TODO: hay que hacer que las playlist tenga owner, tuto de autenticacion
## de django como referencia https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
class Playlist(models.Model):
    title = models.CharField(max_length=50, unique=True)
    icon = models.FileField(blank=True)
    folders = models.ManyToManyField(Folder)
    duration = models.IntegerField(default=0)
    songs = models.ManyToManyField(Song, blank=True)

    def __str__(self):
        return self.title
    class Meta:
        managed = True
        db_table = 'Playlist'

class PodcastEpisode(Audio):
    URI = models.FileField()
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'PodcastEpisode'
