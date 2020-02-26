# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Album(models.Model):
    id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=100)
    fecha = models.DateField(db_column='Fecha')  # Field name made lowercase.
    icono = models.FileField()
    tipo = models.ForeignKey('TipoAlbum', models.DO_NOTHING, db_column='tipo')

    class Meta:
        managed = False
        db_table = 'Album'


class Amigos(models.Model):
    uno = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='uno', primary_key=True)
    otro = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='otro')

    class Meta:
        managed = False
        db_table = 'Amigos'
        unique_together = (('uno', 'otro'),)


class Audio(models.Model):
    id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=100)
    archivo = models.FileField()
    pista = models.IntegerField()
    album = models.ForeignKey(Album, models.DO_NOTHING, db_column='album')
    tipo = models.ForeignKey('TipoAudio', models.DO_NOTHING, db_column='tipo')

    class Meta:
        managed = False
        db_table = 'Audio'


class Cancionenlista(models.Model):
    cancion = models.ForeignKey(Audio, models.DO_NOTHING, db_column='cancion', primary_key=True)
    lista = models.ForeignKey('Lista', models.DO_NOTHING, db_column='lista')

    class Meta:
        managed = False
        db_table = 'CancionEnLista'
        unique_together = (('cancion', 'lista'),)


class Carpeta(models.Model):
    id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=100)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario')

    class Meta:
        managed = False
        db_table = 'Carpeta'


class Favoritos(models.Model):
    audio = models.ForeignKey(Audio, models.DO_NOTHING, db_column='audio', primary_key=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario')

    class Meta:
        managed = False
        db_table = 'Favoritos'
        unique_together = (('audio', 'usuario'),)


class Lista(models.Model):
    id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=100)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario')

    class Meta:
        managed = False
        db_table = 'Lista'


class Listaencarpeta(models.Model):
    carpeta = models.ForeignKey(Carpeta, models.DO_NOTHING, db_column='carpeta', primary_key=True)
    lista = models.ForeignKey(Lista, models.DO_NOTHING, db_column='lista')

    class Meta:
        managed = False
        db_table = 'ListaEnCarpeta'
        unique_together = (('carpeta', 'lista'),)


class Usuario(models.Model):
    id = models.IntegerField(primary_key=True)
    correo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    contrase?a = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'Usuario'


class TipoAlbum(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'tipo_album'


class TipoAudio(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'tipo_audio'
