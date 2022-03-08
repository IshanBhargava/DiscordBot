import requests

pubg_api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5OGQ4YWQwMC03ZjhkLTAxM2EtOTcwYS0xNTY1Y2U0ZmRiYWIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjQ2NTc5NDc4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii1iYjlmY2RjOS1hYjk5LTQ5MjItOTMxOC1kYmY3YmQ2NzBhOTkifQ.h95znR_UiPiBNMiA8Vtw53IzOSmQsAIsUOY9HCouVdQ'


def joke() -> str:
    url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single"
    response = requests.get(url)
    return response.json()["joke"]
