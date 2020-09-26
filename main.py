import time
import requests
import json

from bs4 import BeautifulSoup

import requests

URL = "https://www.tayara.tn/sc/immobilier/appartements/centre%20urbain%20nord"
FILENAME = "houses.json"
INTERVAL = 10  # s

WIREPUSHER_ID = '6mEZmpXwA'


def search():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = list(map(lambda x: x.find("a", recursive=False), soup.find_all(class_="card")))
    return results


def extract_url(a):
    return "https://www.tayara.tn" + a['href']


def get_old_houses():
    return json.load(open(FILENAME))


def save_houses(houses):
    return json.dump(houses, open(FILENAME, 'w'))


def notify(house):
    print("Notifying, " + house)
    params = {
        'id': WIREPUSHER_ID,
        'title': "Dar jdida aala tayara",
        'message': house
    }
    r = requests.get('https://wirepusher.com/send', params=params)
    print(f"Notified and got response code {r.status_code}, with response {r.text}")


def update(flag=None):
    print('Checking new listings..')
    houses = list(map(extract_url, search()))
    old_houses = get_old_houses()
    print(f'Found {len(old_houses)} old houses')
    difference = list(set(houses) - set(old_houses))
    print(f'Found {len(difference)} new houses!')
    if len(difference):
        print('Notifying with new house listings')
    if flag:
        for house in difference:
            notify(house)
    print('Saving new list')
    save_houses(houses)


def main():
    notify_flag = False
    while 1:
        update(notify_flag)
        time.sleep(INTERVAL)
        notify_flag = True


if __name__ == '__main__':
    main()
