from musica.models import *
import urllib.request
import sys
import os
import pathlib #SOURCE: https://j2logo.com/python/listar-directorio-en-python/
import eyed3 #SOURCE: https://stackoverflow.com/questions/8948/accessing-mp3-metadata-with-python
from datetime import date
import time
from django.core.files import File

# Guarda un nuevo artista y devuelve su objeto de models
def poblar_artista(artist):
    mail = artist + '@live.com'
    new_artist = Artist(name = artist, email = mail)
    new_artist.save()
    print('------------------------------')
    print('Artist: ', artist , " saved")
    return new_artist

# Guarda un nuevo album y devuelve su objeto de models
def poblar_album(album, tipo, cover_path, cover_name, artista, recording_year):
    #cover = File(open(cover, 'rb')) #Sino, no funciona
    print(cover_name)
    print(cover_path)
    new_album = Album(title = album, date = recording_year,
        type = tipo, artist = artista)
    new_album.icon.save(cover_name, File(open(cover_path, 'rb')), save = True)

    print('------------------------------')
    print('Album: ', album , " saved")
    return new_album

# Guarda una nueva cancion
def poblar_cancion(can_metadata, song_name, song_path, album):
    print(song_name)
    print(song_path)
    file = File(open(song_path,'rb')) #Sino, no funciona
    title = can_metadata.tag.title
    duration = int(can_metadata.info.time_secs)
    track = can_metadata.tag.track_num[0] #Se coge el primer elemento xq devuelve una tupla
    new_song = Song(title = title, duration = duration,
        track = track, album = album)
    new_song.file.save(song_name, File(open(song_path, 'rb')), save = True)
    print('------------------------------')
    print(title , " saved")


#dir = 'servidor/media/' #Dir raiz
dir = 'Canciones/'
#dir = '/mnt/c/Users/jtamb/Desktop/Canciones/' #Dir raiz

#Obtenemos todas las carpteas(albumes) del directorio

dir_base = pathlib.Path(dir)

albumes = [album.name for album in dir_base.iterdir() if album.is_dir()]

print(albumes)

#for alb in albumes: #Recorremos todos los albumes de la carpeta

alb = albumes[0]

alb = dir + alb #ruta completa
alb_path = pathlib.Path(alb) #Para poder recorrerlo
# Obtenemos el listado de caciones de un album
canciones = [canc.name for canc in alb_path.iterdir() if canc.is_file() and canc.name.endswith('.mp3')]

#Para obtener el artista, el album y el año en que se grabó, debemos obtener los metadatos de una cancion.
can_metadata = eyed3.load(alb + '/' + canciones[0])
artist = can_metadata.tag.artist
album = can_metadata.tag.album
# Tengo que hacer esto para que no de problema la BD
recording_year = can_metadata.tag.recording_date
valid_time= date.today()
valid_time= valid_time.replace(year = recording_year.year)

#Se obtiene la imagen del album a partir de el primero de los elementos en
# formato .jpg que aparezcan en el directorio
cover = [cov.name for cov in alb_path.iterdir() if cov.is_file() and cov.name.endswith('.jpg')]

# "Cover" es la ruta absoluta de la portada del album en cuestion
cover_path = alb + '/' + cover[0]
cover_name = albumes[0] + '/' + cover[0]

# Para hacerlo mas completo, dependiendo del numero de canciones
# hago que sea de un tipo u otro
if len(canciones) == 1:
    tipo = 'S'
elif len(canciones) > 4:
    tipo = 'N'
else:
    tipo = 'EP'

#Inserción de artista en la BD
new_artist = poblar_artista(artist)
#Inserción del album en BD
new_album = poblar_album(album, tipo, cover_path, cover_name, new_artist, valid_time)

#print('Album: ', album, ' Artist: ', artist, 'Tipo: ', tipo, 'Date: ', date)

for can in canciones: #Para cada uno de esos albumes, recorremos sus canciones
    song_path = alb + '/' + can #Ruta absoluta de cancion
    song_name = albumes[0] + '/' + can
    can_metadata = eyed3.load(song_path)
    poblar_cancion(can_metadata, song_name, song_path, new_album)

#temporal = ["Boomer", "Hello World", "Rap", "Rock", "Reggae", "Pop", "Dubstep","With Deepest Regrets", "Viva la vida"]
