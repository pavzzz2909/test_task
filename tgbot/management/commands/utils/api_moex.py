import requests


list_currencies = {'CNYRUB_TOM': 'Юань',
                   'EUR_RUB__TOM': 'Евро',
                   'USD000UTSTOM': 'Доллар'}


class ApiMoex:
    url = 'https://iss.moex.com/iss/'
    headers = {'accept': 'application/json',
               'Content-Type': 'application/json'}

    def _get(self, endpoint):
        return requests.get(f'{self.url}{endpoint}', headers=self.headers).json()

    def get_curses(self):
        return self._get(endpoint=('engines/currency/markets/selt/securities.json?'
                                   "iss.only=securities,marketdata&"
                                   "securities=CETS:USD000UTSTOM,CETS:EUR_RUB__TOM,CETS:CNYRUB_TOM,"
                                   "lang=ru&iss.meta=off&iss.json=extended&callback=angular.callbacks._gk&"
                                   "marketdata.columns=SECID,LAST"))[1]['marketdata']




