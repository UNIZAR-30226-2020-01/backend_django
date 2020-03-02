import spotipy
import sys
from spotify_credentials import the_secret_function
from spotipy.oauth2 import SpotifyClientCredentials

the_secret_function()

class Spotisearcher:
    def __init__(self):
        the_secret_function() # credenciales
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    def get_artist_uri(self, name):
        results = self.sp.search(q='artist:' + name, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            #print(artist['uri'])#, artist['images'][0]['url'])
            return artist['uri']
        else:
            return 'spotify uri unknown'

    def list_albums(self, artist_uri):
        results = self.sp.artist_albums(artist_uri, album_type='album')
        albums = results['items']
        while results['next']:
            results = self.sp.next(results)
            albums.extend(results['items'])
        return albums


#spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
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
