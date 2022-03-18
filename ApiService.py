import requests


def joke() -> str:
    url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single"
    response = requests.get(url)
    return response.json()["joke"]
