import requests as re
import wget
import json

class ScryfallHandler:

    def __init__(self) -> None:
        self.__base_url = 'https://api.scryfall.com'
        self.__base_data_path = 'data'

    def download_bulk_data(self, database = 'All'):
        
        options = [
            'Oracle',
            'UniqueArtwork',
            'Default',
            'All',
            'Rulings'
        ]
        
        response = re.get(f'{self.__base_url}/bulk-data')
        if response.status_code == 200:
            data = response.json()
            wget.download(
                data['data'][options.index(database)]['download_uri'], 
                f'{self.__base_data_path}/{database}.json'
            )
        else:
            print("Falha ao obter os dados", response.status_code)
            print("Resposta:", response.text)

    def download_all_commander_cards(self):
        response = re.get(f'{self.__base_url}/cards/search?q=st:commander')
        if response.status_code == 200:
            response = response.json()
            cards = response['data']
            while response['has_more']:
                response = re.get(response['next_page']).json()
                cards.extend(response['data'])
            with open(f'{self.__base_data_path}/commader.json', 'w') as f:
                json.dump(cards, f)
        else:
            print("Falha ao obter os dados", response.status_code)
            print("Resposta:", response.text)
