import spotipy
import sys
from spotify_credentials import the_secret_function
from spotipy.oauth2 import SpotifyClientCredentials


# usamos spotipy, la librería que adapta la api de spotify a python: https://github.com/plamere/spotipy
class Spotisearcher:
    # necesitamos tener las credenciales en las variables de entorno antes de llamar a esta funcion (ejecutando set_credentials.py)
    def __init__(self):
        # the_secret_function() # credenciales
        # podriamos usar herencia, de momento asi vale:
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    # las siguientes dos funciones estan basadas en ejemplos de la documentacion de spotipy:
    # https://spotipy.readthedocs.io/en/2.9.0/

    # devuelve la uri de spotify del artista de nombre 'name'
    def get_artist_uri(self, name):
        results = self.sp.search(q='artist:' + name, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            #print(artist['uri'])#, artist['images'][0]['url'])
            return artist['uri']
        else:
            return 'spotify uri unknown'

    # devuelve la lista de albumes del artista con uri artist_uri
    def list_albums(self, artist_uri):
        results = self.sp.artist_albums(artist_uri, album_type='album')
        albums = results['items']
        while results['next']:
            results = self.sp.next(results)
            albums.extend(results['items'])
        return albums


# programa de prueba:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        name = ' '.join(sys.argv[1:])
    else:
        name = 'Radiohead'
    sps = Spotisearcher()
    uri = sps.get_artist_uri(name)
    print(uri)
    albums =  sps.list_albums(uri)
    for album in albums:
        print(album['name'])
