import requests


# de https://www.listennotes.com/api/docs/
url = 'https://listen-api.listennotes.com/api/v2/search?q=star%20wars&sort_by_date=0&type=episode&offset=0&len_min=10&len_max=30&genre_ids=68%2C82&published_before=1580172454000&published_after=0&only_in=title%2Cdescription&language=English&safe_mode=1'
headers = {
  'X-ListenAPI-Key': '<SIGN UP FOR API KEY>',
}
response = requests.request('GET', url, headers=headers)
print(response.json())
