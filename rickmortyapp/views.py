from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests 
import sys


def index(request):
    
    url = 'https://integracion-rick-morty-api.herokuapp.com/api/episode/'
    response = requests.get(url)
    response = response.json()
    context = { 'results' : response['results'] }
    while True:
        if response['info']['next'] != '':
            response = requests.get(response['info']['next'])
            response = response.json()
            context['results'].extend(response['results'])
        else:
            break

    return render(request, 'episodes.html', context)

def episode(request, id):
    url = 'https://integracion-rick-morty-api.herokuapp.com/api/episode/' + str(id)
    episode = requests.get(url)
    episode = episode.json()

    if (len(episode['characters'])) != 0:
        characters_id = ''
        for i in episode['characters']:
            characters_id += str(i.split('/')[-1]) + ','
        characters_id = characters_id[:len(characters_id) - 1]
        
        url = 'https://integracion-rick-morty-api.herokuapp.com/api/character/' + characters_id
        characters = requests.get(url)
        characters = characters.json()
        if isinstance(characters, dict):
            characters = [characters]
    else:
        characters = ''

    context = { 'name': episode['name'], 'air_date': episode['air_date'], 'episode': episode['episode'],
    'characters': characters }
    
    return render(request, 'episode_detail.html', context)

def character(request, id):
    url = 'https://integracion-rick-morty-api.herokuapp.com/api/character/' + str(id)
    character = requests.get(url)
    character = character.json()
    
    if len(character['episode']) != 0:
        episodes_id = ''
        for i in character['episode']:
            episodes_id += str(i.split('/')[-1]) + ','
        episodes_id = episodes_id[:len(episodes_id) - 1]
        url = 'https://integracion-rick-morty-api.herokuapp.com/api/episode/' + episodes_id
        episodes = requests.get(url)
        episodes = episodes.json()
        if isinstance(episodes, dict):
            episodes = [episodes]
    else: 
        episodes = ''

    location_id = character['location']['url'].split('/')[-1]
    origin_id = character['origin']['url'].split('/')[-1]
    
    context = { 'name': character['name'], 'status': character['status'], 'species': character['species'],
    'type': character['type'], 'gender': character['gender'], 'episodes': episodes,
    'location': character['location']['name'], 'location_id': location_id,
    'origin': character['origin']['name'], 'origin_id': origin_id,
    'image': character['image'] }

    return render(request, 'character.html', context)


def location(request, id):
    url = 'https://integracion-rick-morty-api.herokuapp.com/api/location/' + str(id)
    location = requests.get(url)
    location = location.json()
    
    #residents 
    if len(location['residents']) != 0:
        residents_id = ''
        for i in location['residents']:
            residents_id += str(i.split('/')[-1]) + ','
        residents_id = residents_id[:len(residents_id) - 1]
        url = 'https://integracion-rick-morty-api.herokuapp.com/api/character/' + residents_id
        residents = requests.get(url)
        residents = residents.json()
        if isinstance(residents, dict):
            residents = [residents]
    else:
        residents = ''

    context = { 'name': location['name'], 'type': location['type'],
    'dimension': location['dimension'], 'residents': residents }
    return render(request, 'location.html', context)


def search(request):
    if request.method == 'GET': 
        search_query = request.GET.get('search_box', None)

    search_query = search_query.lower()
    results = {}

    url_character = 'https://integracion-rick-morty-api.herokuapp.com/api/character/?name=' + search_query
    filter_character = requests.get(url_character)
    filter_character = filter_character.json()
  
    if 'results' in filter_character.keys():
        results = {'character': filter_character['results']}

        while True:
            if filter_character['info']['next'] != '':
                filter_character = requests.get(filter_character['info']['next'])
                filter_character = filter_character.json()
                results['character'].extend(filter_character['results'])
            else:
                break
    
    url_location = 'https://integracion-rick-morty-api.herokuapp.com/api/location/?name=' + search_query
    filter_location = requests.get(url_location)
    filter_location = filter_location.json()
    if 'results' in filter_location.keys():
        results['location'] = filter_location['results']

        while True:
            if filter_location['info']['next'] != '':
                filter_location = requests.get(filter_location['info']['next'])
                filter_location = filter_location.json()

                results['location'].extend(filter_location['results'])
            else:
               break

    url_episode = 'https://integracion-rick-morty-api.herokuapp.com/api/episode/?name=' + search_query
    filter_episode = requests.get(url_episode)
    filter_episode = filter_episode.json()
    if 'results' in filter_episode.keys():
        results['episode'] = filter_episode['results']
        while True:
            if filter_episode['info']['next'] != '':
                filter_episode = requests.get(filter_episode['info']['next'])
                filter_episode = filter_episode.json()

                results['episode'].extend(filter_episode['results'])
            else:
                break
    
    return render(request, 'search.html', results)