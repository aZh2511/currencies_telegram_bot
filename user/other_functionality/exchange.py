import requests


def get_exchange(text: str):
    """Get exchange history."""
    text = text.replace('/exchange ', '')
    text = text.split()

    if '$' in text[0]:
        base = 'USD'
        to = text[-1]
        amount = int(text[0].replace('$', ''))

    else:
        base = text[1]
        to = text[-1]
        amount = int(text[0])

    url = f'https://api.exchangeratesapi.io/latest?base={base}&symbols={to}'
    response = requests.get(url, 'HTTP1.1')
    try:
        result = response.json()['rates']
    except KeyError:
        return 'Unavailable operation!'
    currency = result.get(to)

    return round(currency*amount, 2)
