import requests


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
            return 'error: ' + response.status_code
        #print(response.text)
        return response.json()[self.lyrics_key]

    def add_lyrics_to_db():
        # idea: guardar las letras en la bd, tampoco ocupan mucho
        # se buscan una unica vez cuando se añaden y fuera
        return


if __name__ == '__main__': # para probarlo
    ly = lyrics_api()
    #thelyrics = ly.get_lyrics('verguenza', 'ska-p')#'california dreamin', 'the mamas and the papas')

    thelyrics = ly.get_lyrics('california dreamin', 'the mamas and the papas')
    print(thelyrics)

    #print(ly.get_lyrics('verguenza', 'ska-p'))
