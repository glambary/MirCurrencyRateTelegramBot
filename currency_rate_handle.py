from currency_rate_parse import get_currency_rate


def get_info() -> str:
    currency_rate, currency_rate_with_percent = get_currency_rate()

    old_currency = round(10000/currency_rate_with_percent, 2)

    return f"""Курс = {currency_rate}. Курс с комиссией Тинькофф банка = <b>{currency_rate_with_percent}</b>.
За {currency_rate_with_percent} российских рублей можно купить 1 белорусский рубль.
За 1 российский рубль можно купить {(old_currency/10000):.6f} (<b>{old_currency}</b>) белорусских рублей.
"""


def get_amount_of_money_to_buy(n: float) -> float:
    _, currency_rate_with_percent = get_currency_rate()

    return round(n * currency_rate_with_percent, 2)
