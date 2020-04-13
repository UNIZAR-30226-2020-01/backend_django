from musica.models import *
from utils.podcasts.podcasts import Podcasts_api
import urllib.request
import sys

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
podcast, episodes = api.get_by_name('El hormiguero')
pod_tit = podcast['title']
pod_rss = podcast['rss']
genres = podcast['genre_ids']
pod_id = podcast['id']
pod_imag = podcast['image']
pod_canal = podcast['publisher']
saved_imag = save_image(pod_imag, pod_id, 'podcast')
pod = Podcast(title=pod_tit, RSS=pod_rss, id_listenotes=pod_id,
    image=saved_imag, canal=pod_canal)

pod.save()

for gen in genres:
    # Esto ha sido error de inserción. Hay varios generos iguales(mismo id)
    found = Genre.objects.filter(id_listenotes=gen)[0]
    pod.genre.add(found)

pod.save()
print('Podcast almacenado')

print('-'*20)
#Si tiene mas de 10 episodios, a chupar que es una prueba xd
print("Episodios: " + str(len(episodes)))
if len(episodes) > 10:
    episodes = episodes[:10]

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
    saved_imag = save_image(ep_image, ep_id, 'episode')
    epi = PodcastEpisode(title=ep_title, duration = ep_duration,
        URI = ep_audio, id_listenotes=ep_id, podcast=pod, image=saved_imag)
    epi.save()
    print('Episodio almacenado: ' + ep_title)
# print(podcast)
# print(episode)
