import requests

from bs4 import BeautifulSoup
from requests import RequestException, Response
from cachetools import cached, TTLCache
from datetime import datetime, timedelta

from config import RATE_IN_ERROR, HEADERS, URL


ERROR_MESSAGE = 'Функция "get_currency_rate" отработала некорректно'

cache = TTLCache(
    maxsize=10,
    ttl=timedelta(hours=2),
    timer=datetime.now
)


def get_response(url: str) -> Response | None:
    error_message = ERROR_MESSAGE + " - ошибка получения response."

    try:
        response = requests.get(url, headers=HEADERS)
    except (Exception, RequestException) as err:
        print(error_message + "Ошибка:", err)
        return

    if not 200 <= response.status_code < 300:
        print(error_message + "Статус код:", response.status_code)
        return

    return response


def get_parser(url: str) -> BeautifulSoup | None:
    response = get_response(url)

    if response is None:
        return

    parser = BeautifulSoup(response.text, features='html.parser')
    return parser


@cached(cache)
def get_currency_rate(
        currency_name: str = 'Белорусский рубль',
        n_percent: float = 1.02
) -> tuple:
    print('Currency_rate запрошен с сайта')
    parser = get_parser(URL)
    if parser is None:
        return RATE_IN_ERROR

    data = parser.select("tr td p")
    for indx, value in enumerate(data):
        if currency_name in value.text:
            rate = data[indx + 1].text.strip().replace(',', '.')
            break
    else:
        print(ERROR_MESSAGE, '- for. Не найдены интересующие значения')
        return RATE_IN_ERROR

    return (
        round(float(rate), 2),
        round(float(rate) * n_percent, 2)
    )
