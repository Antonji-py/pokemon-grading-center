import requests
import json
import os
from bs4 import BeautifulSoup


def download_all_sets():
    all_sets = []

    url = "https://www.pokellector.com/sets"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "lxml")

    set_buttons = soup.find_all("a", {"class": "button"})
    for button in set_buttons:
        set_name = button["title"].replace(" Set", "")
        set_url = "https://www.pokellector.com" + button["href"]

        expansion = {
            "name": set_name,
            "url": set_url
        }
        all_sets.append(expansion)

    return all_sets


def get_all_sets(database_path):
    with open(f"{database_path}/sets.json") as json_file:
        sets = json.load(json_file)

        return sets


def get_set(expansion, database_path):
    for _set in get_all_sets(database_path):
        if _set["name"] == expansion:
            return _set


def download_set_images(database_path, expansion):
    url = expansion["url"]

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    if os.path.isdir(f'{database_path}/stock_images/{expansion["name"]}'):
        print(f"{expansion['name']} directory exists")
    else:
        print(f"Making {expansion['name']} directory")
        os.mkdir(f'{database_path}/stock_images/{expansion["name"]}')

        cards = soup.find_all("div", {"class": "card"})
        for div in cards:
            card_name = div.find("a")["title"]
            card_img_url = div.find("img")["data-src"].replace(".thumb", "")

            with open(f"{database_path}/{expansion['name']}/{card_name}.jpg".replace("?", "").replace("*", "").replace(":", ""), "wb+") as file:
                response = requests.get(card_img_url)
                file.write(response.content)

        print(f"Successfully downloaded images from {expansion['name']} set")
        
        
def download_cmc_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    
    cards = soup.find_all("div", {"class": "d-flex mb-4 col-12 col-sm-6 col-md-4 col-lg-3"})
    for card in cards:
        card_img = card.find("img")["data-echo"]
        card_img_url = f"https:{card_img}"
        card_name = card.find("h2", {"class": "card-title h3"}).text.strip()

        with open(f"Aquapolis/{card_name}.jpg", "wb+") as file:
            response = requests.get(card_img_url)
            file.write(response.content)
