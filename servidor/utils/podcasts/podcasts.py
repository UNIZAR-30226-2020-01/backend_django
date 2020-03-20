from __future__ import print_function
import sys
import getpass

import mygpoclient

from mygpoclient import simple

def usage():
    print("""
    Usage: python %s {get|put} {username} {device_id} [host_or_url]
    """ % (sys.argv[0],), file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    # Use the default url if not specified
    if len(sys.argv) == 4:
        sys.argv.append(mygpoclient.ROOT_URL)

    # Check for valid arguments
    if len(sys.argv) != 5:
        usage()

    # Split arguments in local variables
    progname, subcommand, username, device_id, root_url = sys.argv

    # Check for valid subcommand
    if subcommand not in ('get', 'put'):
        usage()

    # Read password from the terminal
    password = getpass.getpass("%s@%s's password: " % (username, root_url))

    # Create the client object with username/password/root_url set
    client = simple.SimpleClient(username, password, root_url)

    if subcommand == 'get':
        # Get the URL list and print it, one per line
        print('\n'.join(client.get_subscriptions(device_id)))
    elif subcommand == 'put':
        # Read the URL list from standard input and upload it
        print('Enter podcast URLs, one per line.', file=sys.stderr)
        urls = sys.stdin.read().splitlines()
        if client.put_subscriptions(device_id, urls):
            print('Upload successful.', file=sys.stderr)
        else:
            print('Could not upload list.', file=sys.stderr)


#---------------------------------------------------#
#-----Todo esto pertenece a la api listennotes------#
#Para poder usarla debemos:
#   -Poner el logo de ListenApi cuando se use el buscador de podcasts
#   -No guardar ningun podcast en la BD
#   -Permite 10000 peticiones al mes
# class Podcasts_api:
#
#     def __init__(self, url = 'https://listen-api.listennotes.com/api/v2', key = 'COMPLETAME_PORFA'):
#         self.url = url
#         self.headers = {
#             'X-ListenAPI-Key' = key
#         }
#         self.querystring = {}   ## TODO: lo dejo porque pensaba hacer una cosa, pero se puede eliminar
#
#     # Existen muchos parámetros, de momento creo que los más importantes son los siguientes
#     #   -name: nombre del podcast (obligatorio)
#     #   -type: episode, podcast, curated (default: episode)
#     #   -language: lenguaje del podcast (default: all languages)
#     #   -sort_by_date: indica si muestra los podcast ordenados por fecha (0 = NO y muestra por relevancia)
#     def get_podcast(self, nombre, type, language, sort_by_date ):
#         #Contiene los parámetros para la búsqueda de podcast
#         querystring = { "q": nombre, "type": type, "language": language,
#         "sort_by_date": sort_by_date
#         }
#         response = requests.request('GET', url, headers=self.headers, params=querystring)
#         if response.status_code != 200:
#             return 'Not podcast found (error: ' + str(response.status_code) + ')'
#
#         return response.json()[] ## TODO: Cuando tenga la API KEY, se podrá terminar
#
#
# # Para probar que funciona
# if __name__ == '__main__':
#     pd = Podcasts_api()
#     querystring = {"q":"Wismichu"}
#     headers = {
#       'X-ListenAPI-Key': '<SIGN UP FOR API KEY>',
#     }
#     response = requests.request('GET', url, headers=headers, params=querystring)
#     print(response.json())
