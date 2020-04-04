# from __future__ import print_function
# import sys
# import getpass
import os
import requests

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
        print(self.key)
        self.headers = {
            'X-ListenAPI-Key' : self.key
        }
        self.querystring = {}   ## TODO: lo dejo porque pensaba hacer una cosa, pero se puede eliminar

    # Existen muchos parámetros, de momento creo que los más importantes son los siguientes
    #   -name: nombre del podcast (obligatorio)
    #   -type: episode, podcast, curated (default: episode)
    #   -language: lenguaje del podcast (default: all languages)
    #   -sort_by_date: indica si muestra los podcast ordenados por fecha (0 = NO y muestra por relevancia)
    def get_podcast(self, nombre, type, language, sort_by_date ):
        # TODO: arreglar esta, jeje
        #Contiene los parámetros para la búsqueda de podcast
        querystring = { "q": nombre, "type": type, "language": language,
        "sort_by_date": sort_by_date
        }
        response = requests.request('GET', self.url, headers=self.headers, params=querystring)
        if response.status_code != 200:
            return 'No podcast found (error: ' + str(response.status_code) + ')'

        return response.json()['took']#response.json() ## TODO: Cuando tenga la API KEY, se podrá terminar

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
    the_secret_function() # borrar esta linea, es solo para el hello world
    pd = Podcasts_api()
    querystring = {"q":"Wismichu"}
    headers = {
      'X-ListenAPI-Key': '',
    }

    nombre="Wismichu"
    type="Podcast"
    language="spanish"
    #response = pd.get_podcast(nombre, type, language, 0)
    # response = requests.request('GET', headers=headers, params=querystring)
    response = pd.helloWorld()
    print(response)
