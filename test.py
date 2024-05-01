import requests
id = 34
url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(id)

response = requests.get(url)
pokemon = response.json()
print (pokemon["stats"][1])