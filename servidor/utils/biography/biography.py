import os
import sys
import json
import requests

from set_credentials import the_secret_function

class LastfmSearcher:
    def __init__(self):
        the_secret_function()
        self.url = 'http://ws.audioscrobbler.com/2.0/'
        self.key = os.getenv('lastfm_key')

    # Devuelve la biografía de un artista dado
    def get_biography(self, name):
        querystring = {
            'method': 'artist.getinfo',
            'artist':  name,
            'api_key': self.key,
            'format': 'json'
        }
        if name:
            result =  requests.get(self.url, params=querystring)

            return result.json()['artist']['bio']['content']
        else:
            return ''

if __name__ == '__main__':

    if len(sys.argv) > 1:
        name = ' '.join(sys.argv[1:])
    else:
        name = 'Nothingface'
    the_secret_function()
    bs = LastfmSearcher()
    result = bs.get_biography(name)
    dumped = json.dumps(result)
    parsed = json.loads(dumped)
    print(json.dumps(parsed, indent=2, sort_keys=True))
