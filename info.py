from bs4 import BeautifulSoup
import requests
import json


def check_username(user_name):
    url = f"http://{user_name}.itch.io"
    response = requests.get(url)
    return response.status_code != 404


def get_last_update(game_url):
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


def get_devlog(game_url):
    response = requests.get(game_url)
    soup = BeautifulSoup(response.text, "html.parser")
    a_tag = soup.find("section", class_="game_devlog").find("a")
    link = a_tag["href"]

    return link


class UpdateInfo:
    def __init__(self, update_url):
        self.response = requests.get(update_url)
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def get_likes_count(self):
        likes_count_element = self.soup.find("div", class_="like_button_drop")[
            "data-init"
        ]
        likes_count = json.loads(likes_count_element)

        return str(likes_count["likes_count"])

    def get_header(self):
        h1_tag = self.soup.find("section", class_="post_header").find("h1")
        header = h1_tag.get_text()

        return header

    def get_description(self):
        strings = []
        for tag in self.soup.find_all(
            "section",
            class_="object_text_widget_widget base_widget user_formatted post_body",
        ):
            strings.append(tag.get_text())

        return strings
