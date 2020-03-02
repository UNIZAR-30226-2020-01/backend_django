import requests

# Wrapper de la api de lyricsovh:
class Lyrics_api:
    # deberiamos citar a https://lyricsovh.docs.apiary.io en alguna parte
    def __init__(self, api="https://api.lyrics.ovh/v1/", lyrics_key='lyrics'):
        self.api = api # api a buscar
        self.lyrics_key = lyrics_key # key del diccionario cuyo valor es la letra

    def get_lyrics(self, title, artist):
        uri = self.api + artist + '/' + title # uri de la cancion, tipo https://api.lyrics.ovh/v1/ska-p/verguenza
        # print(uri)
        response = requests.get(uri)
        if response.status_code != 200: # se podria poner una excepcion aqui
            return 'These lyrics are not available (error: ' + str(response.status_code) + ')'
        #print(response.text)
        return response.json()[self.lyrics_key] # devuelve la letra (el valor de la clave dada en el diccionario json)




if __name__ == '__main__': # para probarlo
    ly = Lyrics_api()
    #thelyrics = ly.get_lyrics('verguenza', 'ska-p')#'california dreamin', 'the mamas and the papas')

    thelyrics = ly.get_lyrics('california dreamin', 'the mamas and the papas')
    print(thelyrics)

    #print(ly.get_lyrics('verguenza', 'ska-p'))
