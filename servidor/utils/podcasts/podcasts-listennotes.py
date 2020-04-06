# from __future__ import print_function
# import sys
# import getpass
import os
import requests
import json

from set_credentials import the_secret_function # borrar esta linea, es solo para el hello world


#---------------------------------------------------#
#-----Todo esto pertenece a la api listennotes------#
#Para poder usarla debemos:
#   -Poner el logo de ListenApi cuando se use el buscador de podcasts
#   -No guardar ningun podcast en la BD
#   -Permite 10000 peticiones al mes
class Podcasts_api:

    def __init__(self, url = 'https://listen-api.listennotes.com/api/v2', key = 'COMPLETAME_PORFA'):
        self.url = url
        self.key = os.getenv('LISTENNOTES_KEY')

        self.headers = {
            'X-ListenAPI-Key' : self.key
        }


    # Existen muchos parámetros, de momento creo que los más importantes son los siguientes
    #   -query: nombre del podcast (obligatorio)
    #   -type: episode, podcast, curated (default: episode)
    #   -language: lenguaje del podcast (default: all languages)
    #   -sort_by_date: indica si muestra los podcast ordenados por fecha (0 = NO y muestra por relevancia)
    def search(self, query, type='episode', language='Spanish', sort_by_date=0):

        #Contiene los parámetros para la búsqueda de podcast
        querystring = { 'q': query, 'type': type, 'language': language,
        'sort_by_date': sort_by_date
        }
        #Se debe añadir /search para que la url sea correcta
        response = requests.get(self.url + '/search', headers=self.headers, params=querystring)

        if response.status_code != 200:
            return 'No podcast found (error: ' + str(response.status_code) + ')'

        return response.json()#response.json() ## TODO: Cuando tenga la API KEY, se podrá terminar

    #Devuelve los mejores podcasts en funcion de los parámetros
    #   -genre_id: genero de los podcast. Más info: get_genres()
    #   -region: región del podcast. Más info: get_regions()
    #   -
    def get_bestpodcast(self, genre_id = None , region='es' ):
        querystring = {
            'genre_id': genre_id, 'region': region
        }
        response = requests.get(self.url + '/best_podcasts', headers=self.headers, params=querystring)

        return response.json()

    # Dado un id, devuelve TODA información sobre un podcast, en formato JSON
    def get_detailedInfo_podcast(self, id):
        querystring = {
            'id': id
        }
        response = requests.get(self.url + '/podcasts/'+id, headers=self.headers, params=querystring)

        return response.json()

    # Dado un id, devuelve TODA información sobre un episodio, en formato JSON
    def get_detailedInfo_episode(self, id):
        querystring = {
            'id': id
        }
        response = requests.get(self.url + '/episodes/'+id, headers=self.headers, params=querystring)

        return response.json()

    #Devuelve todos los géneros a los que puede pertenecer podcast
    def get_genres(self):

        response = requests.get(self.url + '/genres', headers=self.headers)
        return response.json()

    #Devuelve las posibles regiones de podcast en forma de json
    def get_regions(self):
        response = requests.get(self.url + '/regions', headers=self.headers)
        return response.json()

    #Devuleve un episodio de un podcast random. No necesita parámetros
    def get_randomEpisode(self):
        response = requests.get(self.url + '/just_listen', headers=self.headers)
        return response.json()

    #Dada una lista de ids de episodios(separadas por comas p.ej: 26326735763,823726372),
    #devuelve sus links de audio.
    def get_audio(self, ids):
        data = {
            'ids': ids
        }
        response = requests.post(self.url + '/episodes', headers=self.headers, data = data)
        print([l["audio"] for l in response.json()["episodes"]])

    #Recomienda términos de búsqueda, géneros de podcasts y Podcasts_api
    #   -query: Término de búsqueda, p.ej: star wars. Si se pone con comillas ("star wars"), la búsqueda es literal
    #   -show_podcasts: 1 para auto-sugerir podcasts(con información mínima). 0 para no sugerir.
    #   -show_genres: 1 para recomendar géneros de acuerdo a 'query'. 0 para no recomendar.
    def get_suggested_podcasts(self, query, show_podcasts=0, show_genres=0):
        querystring = {
            'q': query,
            'show_podcasts': show_podcasts,
            'show_genres' : show_genres
        }
        response = requests.get(self.url + '/typeahead', headers=self.headers, params=querystring)

        return response.json()

    # Copiada de https://www.listennotes.com/api/docs/ tal cual. Al menos confirma que la key funciona
    def helloWorld(self):

        url = 'https://listen-api.listennotes.com/api/v2/search?q=star%20wars&sort_by_date=0&type=episode&offset=0&len_min=10&len_max=30&genre_ids=68%2C82&published_before=1580172454000&published_after=0&only_in=title%2Cdescription&language=English&safe_mode=0'
        headers = {
          'X-ListenAPI-Key': self.key,
        }
        response = requests.request('GET', url, headers=headers)
        print(response.json())

# Para probar que funciona
if __name__ == '__main__':
    the_secret_function()
    pd = Podcasts_api()

    # Este es un ejemplo de uso en el que:
    #   -Se busca un podcast con el método search y se coge el primero. (se muestra su canal)
    #   -Se busca información detallada de ese podcast
    #   -Se busca información detallada de cada uno de los episodios de ese podcast

    result = pd.search(query="La vida moderna", type='podcast', sort_by_date=1)
    #'Results' es la lista de podcast devuelta en el JSON
    pod_id = result["results"][0]["id"]
    result = pd.get_detailedInfo_podcast(id=pod_id)
    print("Nombre de poscast: " + result["title"])
    print("Canal del podcast: " + result["publisher"])
    episodes = result["episodes"]
    lista_final = [(l["title"], l["audio"]) for l in episodes]
    result = json.dumps(lista_final)
    parsed = json.loads(result)

    # Si se quiere acceder al archivo mp3:
    # curl -L -s -w %{url_effective} --request GET <audio_listennotes>
    print(json.dumps(parsed, indent=2, sort_keys=True))
