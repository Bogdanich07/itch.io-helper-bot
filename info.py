import requests
from bs4 import BeautifulSoup


def check_username(user_name):
    url = f"http://{user_name}.itch.io"
    response = requests.get(url)
    return response.status_code != 404


def get_post_date(game_url):
    response = requests.get(game_url)
    soup = BeautifulSoup(response.text, "html.parser")

    abbr_tag = soup.find("div", class_="post_date").find("abbr")
    title = abbr_tag["title"]

    return title


def get_links(user_name):
    games = []
    response = requests.get(f"https://{user_name}.itch.io/")
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup.find_all("div", class_="game_title"):
        games.append(tag.find("a")["href"])

    return games


def get_titles(user_name):
    games = []
    response = requests.get(f"https://{user_name}.itch.io/")
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup.find_all("div", class_="game_title"):
        games.append(tag.a.get_text())

    return games
