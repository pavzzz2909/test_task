import requests
import os


class ApiWeather:
    url = 'https://api.openweathermap.org/data/2.5/weather?'
    headers = {'accept': 'application/json',
               'Content-Type': 'application/json'}
    appid = os.environ.get('api_key_weather')

    def _get(self, endpoint):
        return requests.get(f'{self.url}{endpoint}&APPID={self.appid}&lang=ru&units=metric', headers=self.headers).json()

    def get_weather(self, city):
        url = f'q={city}'
        return self._get(endpoint=url)

