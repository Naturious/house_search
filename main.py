import time
import requests
import json
from pprint import pprint

from bs4 import BeautifulSoup
import cssutils

URL = "https://www.tayara.tn/sc/immobilier/appartements/centre%20urbain%20nord"
FILENAME = "houses.json"


def search():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all(class_="card__preview")
    return results


def extract_url(a):
    return cssutils.parseStyle(a['style'])['background-image'].replace('url(', '').replace(')', '')


def get_old_houses():
    return json.load(open(FILENAME))


def save_houses(houses):
    return json.dump(houses, open(FILENAME, 'w'))


def notify(house):
    print(house)


def update():
    print('Checking new listings..')
    houses = list(map(extract_url, search()))
    old_houses = get_old_houses()
    print(f'Found {len(old_houses)} old houses')
    difference = list(set(houses) - set(old_houses))
    print(f'Found {len(difference)} new houses!')
    if len(difference):
        print('Notifying with new house listings')
    for house in difference:
        notify(house)
    print('Saving new list')
    save_houses(houses)


def main():
    while 1:
        time.sleep(10)
        update()

if __name__ == '__main__':
    main()
