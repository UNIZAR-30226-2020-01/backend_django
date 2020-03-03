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
    #id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=100)
    fecha = models.DateField(db_column='Fecha')  # Field name made lowercase.
    icono = models.FileField()
    tipo = models.ForeignKey('TipoAlbum', models.DO_NOTHING, db_column='tipo', default=0)

    class Meta:
        managed = True
        db_table = 'Album'


class Amigos(models.Model):
    uno = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='uno', primary_key=True)
    otro = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='otro', related_name='otro')

    class Meta:
        managed = True
        db_table = 'Amigos'
        unique_together = (('uno', 'otro'),)


class Audio(models.Model):
    ##id = models.IntegerField(primary_key=True)
    artista = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    archivo = models.FileField()
    pista = models.IntegerField()
    letra = models.TextField(blank=True)
    album = models.ForeignKey(Album, models.DO_NOTHING, db_column='album')
    tipo = models.ForeignKey('TipoAudio', models.DO_NOTHING, db_column='tipo')

    def is_song(self):
        is_song = False
        try:
            is_song = self.tipo.get_tipo() == 'Cancion'
        except TipoAudio.DoesNotExist:
            pass
        return is_song

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
        managed = True
        db_table = 'Audio'


class Cancionenlista(models.Model):
    cancion = models.ForeignKey(Audio, models.DO_NOTHING, db_column='cancion', primary_key=True)
    lista = models.ForeignKey('Lista', models.DO_NOTHING, db_column='lista')

    class Meta:
        managed = True
        db_table = 'CancionEnLista'
        unique_together = (('cancion', 'lista'),)


class Carpeta(models.Model):
    #id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=100)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario')

    class Meta:
        managed = True
        db_table = 'Carpeta'


class Favoritos(models.Model):
    audio = models.ForeignKey(Audio, models.DO_NOTHING, db_column='audio', primary_key=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario')

    class Meta:
        managed = True
        db_table = 'Favoritos'
        unique_together = (('audio', 'usuario'),)


class Lista(models.Model):
    #id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=100)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario')

    class Meta:
        managed = True
        db_table = 'Lista'


class Listaencarpeta(models.Model):
    carpeta = models.ForeignKey(Carpeta, models.DO_NOTHING, db_column='carpeta', primary_key=True)
    lista = models.ForeignKey(Lista, models.DO_NOTHING, db_column='lista')

    class Meta:
        managed = True
        db_table = 'ListaEnCarpeta'
        unique_together = (('carpeta', 'lista'),)


class Usuario(models.Model):
    #id = models.IntegerField(primary_key=True)
    correo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'Usuario'


class TipoAlbum(models.Model):
    #id = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=10)

    class Meta:
        managed = True
        db_table = 'tipo_album'


class TipoAudio(models.Model):
    #id = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=10)

    def get_tipo(self):
        return self.tipo

    class Meta:
        managed = True
        db_table = 'tipo_audio'
