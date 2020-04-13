import spotipy
import sys
from spotify_credentials import the_secret_function
from spotipy.oauth2 import SpotifyClientCredentials

the_secret_function()

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

print(spotify.artist(birdy_uri))

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])





#spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

if len(sys.argv) > 1:
    name = ' '.join(sys.argv[1:])
else:
    name = 'Radiohead'

results = spotify.search(q='artist:' + name, type='artist,album')
items = results['artists']['items']
if len(items) > 0:
    artist = items[0]
    print(artist['name'])#, artist['images'][0]['url'])
