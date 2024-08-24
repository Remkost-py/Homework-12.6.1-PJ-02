import json
import requests
from config import keys

class ConvertionException(Exception):
    pass


class ValueCovector:
    @staticmethod
    def convert(quote: str, baze: str, amount: float):


        if quote == baze:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты: {baze}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Неудалось обработать валюту: {quote}\nДоступные валюты вы можете посмотреть с помощью команды: /values')

        try:
            baze_ticker = keys[baze]
        except KeyError:
            raise ConvertionException(f'Неудалось обработать валюту: {baze}\nДоступные валюты вы можете посмотреть с помощью команды: /values')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Неудалось обработать количество: {amount}\nПомощь /help')

        quote_ticker, baze_ticker = keys[quote], keys[baze]
        url = f'https://v6.exchangerate-api.com/v6/46ee335c3aa83bab543eb1e6/latest/{quote_ticker}'
        response = requests.get(url)
        data = response.json()
        value = data.get('conversion_rates')
        total_baze = value.get(baze_ticker) * int(amount)

        return total_baze