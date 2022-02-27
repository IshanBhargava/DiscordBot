import requests


def chucknorrisjokes() -> str:
    url = "https://api.chucknorris.io/jokes/random"
    response = requests.get(url)
    return response.json()["value"]


def joke() -> str:
    url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist,explicit&type=single"
    response = requests.get(url)
    return response.json()["joke"]
