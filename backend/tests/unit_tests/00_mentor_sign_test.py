# 00_mentor_sign_test

from typing import List
from uuid import uuid4
import requests
from fixtures.mentor_fixture import mentor_signatures

from core.config import TestConfig

config = TestConfig()
baseurl = config.BACKEND_BASEURL

def test_ping():
    response = requests.get(
        baseurl + "/ping"
    )
    assert response.status_code == 200


def test_mentor_sign_up(mentor_signatures):
    """Тест на корректную регистрацию с нормальными данными"""
    tokens: List[str] = []
    for fixture in mentor_signatures:
        response = requests.post(
            baseurl + "/mentors/sign-up",
            json=fixture
        )

        assert response.status_code == 201
        
        response_json = response.json()
        tokens.append(response_json.get("token"))


def test_mentor_sign_in(mentor_signatures):
    """Тест на корректный логин с нормальными данными"""
    for fixture in mentor_signatures:
        response = requests.post(
            baseurl + "/mentors/sign-up",
            json=fixture
        )
        assert response.status_code == 201

        pswd = fixture.get("password")
        email = fixture.get("email")

        response = requests.post(
            baseurl + "/mentors/sign-in",
            json={
                "password": pswd,
                "email": email
            }
        )

        assert response.status_code == 200


def test_get_mentor_by_id(mentor_signatures):
    """Тест на корректное получение по id"""
    for fixture in mentor_signatures:
        response = requests.post(
            baseurl + "/mentors/sign-up",
            json=fixture
        )
        assert response.status_code == 201

        response_json = response.json()

        id = response_json.get("id")
        response = requests.get(
            baseurl + f"/mentors/{id}"
        )

        fixture.pop("password")
        answer = response.json()
        answer.pop("mentor_id")

        assert response.status_code == 200
        assert fixture == answer


def test_get_mentor_by_id_no_mentor(mentor_signatures):
    """Тест на получение ментора, к-ого не существует"""
    id = str(uuid4())

    response = requests.get(
        baseurl + f"/mentors/{id}"
    )
    assert response.status_code == 404


def test_sign_up_broken_mentor(mentor_signatures):
    """Тест на ошибки валидации"""
    fixture = mentor_signatures[0]

    fixture["name"] = 1 # name - integer

    response = requests.post(
        baseurl + "/mentors/sign-up",
        json=fixture
    )
    assert response.status_code == 422
