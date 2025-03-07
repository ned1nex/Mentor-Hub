import random
import requests
from typing import List

from fixtures.search_fixture import mentor_search_fixtures
from core.config import TestConfig

config = TestConfig()
baseurl = config.BACKEND_BASEURL

def generate_random_string(n = 10):
    return "".join([random.choice(list("ASHDCHSD")) for _ in range(10)])

def make_mentor(tags: List[str]):
    return {
        "name": "nikita",
        "email": generate_random_string(10) + "@yandex.ru",
        "telegram": "@" + generate_random_string(10),
        "password": "1231231231JJ",
        "expertise": "expert",
        "bio": "123123",
        "score": 0,
        "tags": tags
    }

def test_search_a_lot_of_same_words():
    """Обычный поиск по бд"""
    tags = [
        r.split()
        for r in [
            "У меня большой опыт в программировании на питоне. Обожаю фастапи и все с этим связанное.",
            "Я много программировал на джаваскрипте, это то что я очень люблю",
            "Я обожаю плюсы, это то что мне больше всего нравится.",
            "ПРОГРАММИРОВАТЬ ПРОГРАММИРОВАТЬ ПРОГРАММИРОВАТЬ ПРОГРАММИРОВАТЬ ПРОГРАММИРОВАТЬ ПРОГРАММИРОВАТЬ ПРОГРАММИРОВАТЬ",
        ]
    ]

    query = "Хочу прогать на джаваскрипте"
    response = requests.get(
        baseurl + "/mentors?query=" + query
    )
    print(response.json())
    sorted_response = sorted(response.json(), key=lambda x: x.get("score"), reverse=True)

    assert len(response.json()) != 0


def test_search_queries(mentor_search_fixtures):
    mentor_search_fixtures = [
        mentor_search_fixtures.first_triple,
        mentor_search_fixtures.second_triple,
        mentor_search_fixtures.third_triple,
        mentor_search_fixtures.fourth_triple,
        mentor_search_fixtures.fifth_triple,
    ]

    for mentor, query, awaited in mentor_search_fixtures:
        mentor["password"] = "123123123123"

        response = requests.post(
            baseurl + "/mentors/sign-up",
            json=mentor
        )
        assert response.status_code == 201

    
    for _, query, awaited in mentor_search_fixtures:
        response = requests.get(
            baseurl + "/mentors?query=" + query
        )
        assert response.status_code == 200
        sorted_response = sorted(response.json(), key=lambda x: x.get("score"), reverse=True)

        print(list(sorted_response)[0].get("mentor").get("name"))