# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from utils.lyrics.lyrics import Lyrics_api

# para señales (ahora no las usamos):
# from django.db.models.signals import post_save
# from django.dispatch import receiver



class Album(models.Model):
    TIPOS_ALBUM = (
        ('N', 'Normal'),
        ('EP', 'EP'),
        ('S', 'Single'),
    )
    titulo = models.CharField(max_length=100)
    fecha = models.DateField(db_column='Fecha')  # Field name made lowercase.
    icono = models.FileField()
    tipo = models.CharField(max_length=1, choices=TIPOS_ALBUM)

    class Meta:
        managed = True
        db_table = 'Album'

    def __str__(self):
        return self.titulo

class Artista(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50)
    imagen = models.FileField()
    biografia = models.CharField(max_length=256)
    albumes = models.ManyToManyField(Album)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'Artista'


class Genero(models.Model):
    nombre = CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'Genero'

class Podcast(models.Model):
    titulo = models.CharField(max_length=50)
    RSS = models.FileField()
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    class Meta:
        managed = True
        db_table = 'Podcast'

#Clase padre de Cancion y Podcast. Es abstracta para evitar que se cree una tabla de este tipo.
class Audio(models.Model):
    ##id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=100)
    archivo = models.FileField(blank=True)
    album = models.ForeignKey(Album, models.DO_NOTHING, db_column='album')

    def is_song(self):
        is_song = False
        try:
            is_song = self.tipo.get_tipo() == 'Cancion'
        except TipoAudio.DoesNotExist:
            pass
        return is_song

    def __str__(self):
        return self.titulo

    def __init__(self, *args, **kwargs):
        super(Audio, self).__init__(*args, **kwargs)
        es_cancion = self.is_song() # esto habra que cambiarlo
        if es_cancion: # que solo ponga letras a las canciones, no a los podcasts
            api = Lyrics_api()
            letra = api.get_lyrics(self.titulo, self.artista)
            #print(letra)
            if letra != '':
                self.letra = letra
            else: # revisar
                exit(1)

        # if self.initial.get('account', None):
        #     self.fields['customer'].queryset = Customer.objects.filter(account=self.initial.get('account'))


    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(Audio, self).save()#commit=False)

        # my custom code was here

        # if commit:
        #     m.save()
        return m

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
        abstract = True

class Usuario(models.Model):
    #id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    correo = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=100)
    podcasts = models.ManyToManyField(Podcast)
    siguiendo = models.ManyToManyField(self, related_name='seguidor')
    seguido = models.ManyToManyField(self, related_name='seguido')
    timestamp = models.ForeignKey(Audio, null=True)
    favorito = models.ManyToManyField(Audio)

    class Meta:
        managed = True
        db_table = 'Usuario'

    def __str__(self):
        return self.nombre

class Carpeta(models.Model):
    titulo = models.CharField(max_length=50, unique=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'Carpeta'
    def __str__(self):
        return self.titulo

class Lista(models.Model):
    titulo = models.CharField(max_length=50, unique=True)
    carpetas = models.ManyToManyField(Carpeta)

    def __str__(self):
        return self.titulo

class Cancion(Audio):
    pista = models.IntegerField()
    num_reproducciones = models.IntegerField()
    letra = models.CharField(max_length=400, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    listas = models.ManyToManyField(Lista)

    class Meta:
        managed = True
        db_table = 'Cancion'

class Episodio_podcast(Audio):
    URI = models.FileField()
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'Episodio_podcast'
