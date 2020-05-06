import spotipy
import sys
# from spotify_credentials import the_secret_function
from spotipy.oauth2 import SpotifyClientCredentials
import json
import urllib.request

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
            return artist['id']
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

    # Busca la primera imagen proporcionada de un artista con ese nombre
    # Además lo guarda en 'servidor/media'
    #Devulve el archivo guardado
    def get_artist_image(self, name):
        if name:
            artist_uri = self.get_artist_uri(name)
            if artist_uri == 'spotify uri unknown':
                return ''

            artist = self.sp.artist(artist_uri)

            imagenes = artist['images']

            if len(imagenes) > 1:
                imagen_url = imagenes[0]['url']
                imagen_name = name + '_artist_image.jpg'
                destino = 'servidor/media/'+name+'_artist_image.jpg'
                urllib.request.urlretrieve(imagen_url, destino)
                return imagen_name

            else:
                return ''
        else:
            return ''
# programa de prueba:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        name = ' '.join(sys.argv[1:])
    else:
        name = 'Radiohead'
    print("Buscando " + name + "...")
    sps = Spotisearcher()

    result = sps.get_artist_image(name)
    print(result)
    # dumped = json.dumps(result)
    # parsed = json.loads(dumped)
    #print(json.dumps(parsed, indent=2, sort_keys=True))

    # albums =  sps.list_albums(uri)
    # for album in albums:
    #     print(album['name'])
