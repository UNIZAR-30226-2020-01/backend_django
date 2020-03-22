import requests

# TODO: Probar otras APIs para buscar en ellas cuando falle la primera:
class Lyrics_api:
    # deberiamos citar a https://lyricsovh.docs.apiary.io en alguna parte
    def __init__(self, api="https://api.lyrics.ovh/v1/", lyrics_key='lyrics'):
        self.api = api
        self.lyrics_key = lyrics_key


    def get_lyrics(self, title, artist):
        uri = self.api + artist + '/' + title
        # print(uri)
        response = requests.get(uri)
        if response.status_code != 200: # arreglar esto que esta feo
            # TODO: aquí se llamaría a otra API
            return '' # de momento mejor la cadena vacia que lo de antes: These lyrics are not available (error: ' + str(response.status_code) + ')
        #print(response.text)
        return response.json()[self.lyrics_key]



if __name__ == '__main__': # para probarlo
    ly = lyrics_api()
    #thelyrics = ly.get_lyrics('verguenza', 'ska-p')#'california dreamin', 'the mamas and the papas')

    thelyrics = ly.get_lyrics('california dreamin', 'the mamas and the papas')
    print(thelyrics)

    #print(ly.get_lyrics('verguenza', 'ska-p'))
