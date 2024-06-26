import requests as re
import wget
import json
import pandas as pd
import streamlit as st

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

    def commander_cards(self, option = 'data_frame'):
        '''
            options: data_frame | download
        '''
        query = (
            "is:legendary (type:creature OR (type:planeswalker "
            "AND oracle_text:'This card can be your commander' and legal:commander ))"
        )
        response = re.get(f'{self.__base_url}/cards/search?q={query}')
        if response.status_code == 200:
            response = response.json()
            cards = response['data']
            total_cards = response['total_cards']
            progress = 0
            my_bar = st.progress(0, text="Buscando os dados. Por favor Aguarde")
            while response['has_more']:
                response = re.get(response['next_page']).json()
                cards.extend(response['data'])
                status = len(cards)
                progress = status / total_cards
                my_bar.progress(progress,
                                text=f"Buscando os dados. Por favor Aguarde. Status: {progress*100:.2f}%")
            my_bar.empty()
            if option == 'data_frame':
                return pd.json_normalize(cards)

            if option == 'download':
                with open(f'{self.__base_data_path}/commader.json', 'w') as f:
                    json.dump(cards, f)
        else:
            print("Falha ao obter os dados", response.status_code)
            print("Resposta:", response.text)
