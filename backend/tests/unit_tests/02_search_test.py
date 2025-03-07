import random
import requests
from core.config import TestConfig

config = TestConfig()
baseurl = config.BACKEND_BASEURL

def generate_random_string(n = 10):
    return "".join([random.choice(list("ASHDCHSD")) for _ in range(10)])

def test_search():
    """Обычный поиск по бд"""
    tags = [
        ["python", "fastapi", "pydantic"],
        ["java", "minecraft", "banans"],
        ["программирование", "олимпиады", "C++"]
    ]

    for tag in tags:
        response = requests.post(
            baseurl + "/mentors/sign-up",
            json={
                "name": "nikita",
                "email": generate_random_string(10) + "@yandex.ru",
                "telegram": "@" + generate_random_string(10),
                "password": "1231231231JJ",
                "expertise": "expert",
                "bio": "123123",
                "score": 0,
                "tags": tag
            }
        )
        assert response.status_code == 201


    response = requests.get(
        baseurl + "/mentors?query=" + "олимпиады"
    )
    assert response.status_code == 200
    assert len(response.json()) != 0



def test_search_empty_query():
    """Тест на ошибки валидации, пустая строка в query"""
    tags = [
        ["python", "fastapi", "pydantic"],
        ["java", "minecraft", "banans"],
        ["программирование", "олимпиады", "C++"]
    ]

    for tag in tags:
        response = requests.post(
            baseurl + "/mentors/sign-up",
            json={
                "name": "nikita",
                "email": generate_random_string(10) + "@yandex.ru",
                "telegram": "@" + generate_random_string(10),
                "password": "1231231231JJ",
                "expertise": "expert",
                "bio": "123123",
                "score": 0,
                "tags": tag
            }
        )
        assert response.status_code == 201

    response = requests.get(
        baseurl + "/mentors?query=" + ""
    )
    assert response.status_code == 422