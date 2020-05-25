from musica.models import *
from utils.podcasts.podcasts import Podcasts_api
import urllib.request
import sys
import numpy as np

# Para poblar generos de podcast
# api = Podcasts_api()
# generos = api.get_genres()
# i = 0
# for gen in generos:
#     print(gen)
#     temp = Genre(name = gen['name'], id_listenotes = gen['id'])
#     temp.save()
#     print("Almacenado: " +  gen['name'] + " , " +str(gen['id']))
#     i+=1

def save_image(pod_imag, pod_id, type):
    image_name = type + '_' + str(pod_id) + '.jpg'
    destino = 'servidor/media/'+ image_name
    try:
        urllib.request.urlretrieve(pod_imag, destino)
        return image_name
    except:
        e = sys.exc_info()[0]
        print(e)

#Para poblar podcast y sus episodios
api = Podcasts_api()
# podcast, episodes = api.get_by_name('cronocine')
episodes = api.get_allEpisodes('d844c50b6b864fca8effc6088c8162ce')
pod_tit = podcast['title']
pod_rss = podcast['rss']
genres = podcast['genre_ids']
pod_id = podcast['id']
pod_imag = podcast['image']

pod_chan = podcast['publisher']
new_chan = Channel(name=pod_chan)
new_chan.save()
print('Canal almacenado')

#saved_imag = save_image(pod_imag, pod_id, 'podcast')
pod = Podcast(title=pod_tit, RSS=pod_rss, id_listenotes=pod_id,
    image=pod_imag, channel=new_chan)

pod.save()

for gen in genres:
    # Esto ha sido error de inserción. Hay varios generos iguales(mismo id)
    found = Genre.objects.filter(id_listenotes=gen)[0]
    pod.genre.add(found)

pod.save()
print('Podcast almacenado')

print('-'*20)

# print('All episodes')
# titles = [ep['id'] for ep in episodes]
# print(titles)

print('Total epiosdes: ', len(episodes) )

lista_separada = [episodes]
if len(episodes) > 10:
    i = len(episodes) // 10
    lista_separada = np.array_split(episodes, i+1)

for episodes in lista_separada:
    ids = []
    for epi in episodes:
        ids.append(epi['id'])

    ids = ','.join(ids)
    print('IDS' + ids)

    episodes = api.get_many_episodes(ids)

    #print(episodes)

    for epi in episodes:
        ep_audio = epi['audio']
        ep_id = epi['id']
        ep_title = epi['title']
        ep_duration = epi['audio_length_sec']
        ep_image = epi['image']
        ep_description = epi['description']
        # saved_imag = save_image(ep_image, ep_id, 'episode')
        epi = PodcastEpisode(title=ep_title, duration = ep_duration,
            URI = ep_audio, id_listenotes=ep_id, podcast=pod, image=ep_image, description=ep_description)
        epi.save()
        print('Episodio almacenado: ' + ep_title)
