import matplotlib.pyplot as plt
import requests
from datetime import datetime, timedelta

title = ''


def get_history(text: str):
    """Get currency rate history."""
    global title
    text = text.replace('/history', '')
    text = text.split()
    base = text[0].split('/')[0]
    to = text[0].split('/')[-1]
    title = text[0]

    end_at = datetime.now().date()
    period = timedelta(days=int(text[-2]))
    start_at = end_at - period

    url = f'https://api.exchangeratesapi.io/history?start_at={start_at}&end_at={end_at}&base={base}&symbols={to}'

    response = requests.get(url)
    result = response.json()
    try:
        return result['rates']
    except KeyError:
        return False


def draw(text: str):
    """Draw amd save the graph."""
    if get_history(text):
        global title
        data = get_history(text)
        days = list(data.keys())
        rates = [list(data.get(key).values()) for key in days]

        days = [date[5:] for date in data.keys()]
        days.sort()

        plt.plot(days, rates)

        plt.xlabel('date')
        plt.ylabel('rate')
        plt.title(title)

        plt.savefig('media/graph.png')
        plt.close()
        return True
    return False
