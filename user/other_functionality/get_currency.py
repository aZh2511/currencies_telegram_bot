import requests


def get_currency():
    """Get currency rates data."""
    """Get a list of currencies."""

    url = 'https://api.exchangeratesapi.io/latest?base=USD'
    response = requests.get(url, 'HTTP/1.1')

    result = response.json()
    rates = result['rates']
    rates.pop('USD')

    return rates
