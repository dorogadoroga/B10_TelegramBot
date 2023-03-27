import requests
import json
from config import currency


class APIException(Exception):
    pass


class ConvertTest:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'Не удалось конвертировать валюту "{base}"')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'Не удалось конвертировать валюту "{quote}"')

        if base == quote:
            raise APIException('Вы ввели одинаковые валюты')

        try:
            amount = float(amount)
            if amount < 0:
                raise APIException(f'Количество переводимой валюты должно быть положительным числом')
        except ValueError:
            raise APIException(f'Не удалось обработать параметр "{amount}"')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        exch_rate = json.loads(r.content)
        result = round(float(amount) * float(exch_rate[quote_ticker]), 2)

        return result
