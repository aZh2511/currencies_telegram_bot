import requests

response = requests.get('https://api.exchangeratesapi.io/latest?base=USD', 'HTTP/1.1')
result = response.json()
rates_d = result['rates']
rates = []

for currency in rates_d:
    print(f'{currency}: {rates_d.get(currency)}')
