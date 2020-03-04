import requests

#Para poder usarla debemos:
#   -Poner el logo de ListenApi cuando se use el buscador de podcasts
#   -No guardar ningun podcast en la BD
#   -Permite 10000 peticiones al mes
class Podcasts_api:

    def __init__(self, url = 'https://listen-api.listennotes.com/api/v2', key = 'COMPLETAME_PORFA'):
        self.url = url
        self.headers = {
            'X-ListenAPI-Key' = key
        }
        self.querystring = {}   ## TODO: lo dejo porque pensaba hacer una cosa, pero se puede eliminar

    # Existen muchos parámetros, de momento creo que los más importantes son los siguientes
    #   -name: nombre del podcast (obligatorio)
    #   -type: episode, podcast, curated (default: episode)
    #   -language: lenguaje del podcast (default: all languages)
    #   -sort_by_date: indica si muestra los podcast ordenados por fecha (0 = NO y muestra por relevancia)
    def get_podcast(self, nombre, type, language, sort_by_date ):
        #Contiene los parámetros para la búsqueda de podcast
        querystring = { "q": nombre, "type": type, "language": language,
        "sort_by_date": sort_by_date
        }
        response = requests.request('GET', url, headers=self.headers, params=querystring)
        if response.status_code != 200:
            return 'Not podcast found (error: ' + str(response.status_code) + ')'

        return response.json()[] ## TODO: Cuando tenga la API KEY, se podrá terminar


# Para probar que funciona
if __name__ == '__main__':
    pd = Podcasts_api()
    querystring = {"q":"Wismichu"}
    headers = {
      'X-ListenAPI-Key': '<SIGN UP FOR API KEY>',
    }
    response = requests.request('GET', url, headers=headers, params=querystring)
    print(response.json())
