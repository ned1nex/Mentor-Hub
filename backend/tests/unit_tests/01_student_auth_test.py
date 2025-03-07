import requests
import json
import pytest
from fixtures.student_fixture import student_data

from core.config import TestConfig

config = TestConfig()
baseurl = config.BACKEND_BASEURL


def test_student_sign_up(student_data):
    """Тест регистрации студента"""
    response = requests.post(
        baseurl + "/students/sign-up",
        data=json.dumps(student_data),
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 201
    response_json = response.json()
    assert "token" in response_json


def test_student_sign_in(student_data):
    """Тест аутентификации студента"""
    # Регистрируем студента, чтобы он присутствовал в базе
    requests.post(
        baseurl + "/students/sign-up",
        data=json.dumps(student_data),
        headers={"Content-Type": "application/json"}
    )
    # Пытаемся войти
    sign_in_data = {
        "email": student_data["email"],
        "password": student_data["password"]
    }
    response = requests.post(
        baseurl + "/students/sign-in",
        data=json.dumps(sign_in_data),
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "token" in response_json


def test_student_sign_in_invalid_password(student_data):
    """Тест входа с неправильным паролем"""
    # Регистрируем студента, чтобы он присутствовал в базе
    requests.post(
        baseurl + "/students/sign-up",
        data=json.dumps(student_data),
        headers={"Content-Type": "application/json"}
    )
    sign_in_data = {
        "email": student_data["email"],
        "password": "wrongpassword"
    }
    response = requests.post(
        baseurl + "/students/sign-in",
        data=json.dumps(sign_in_data),
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 403
    assert response.json().get("error") == "not authenticated"
    

def test_student_get_profile(student_data):
    """Тест получения профиля студента"""
    # Регистрируем студента
    sign_up_response = requests.post(
        baseurl + "/students/sign-up",
        data=json.dumps(student_data),
        headers={"Content-Type": "application/json"}
    )
    assert sign_up_response.status_code == 201

    # Аутентификация
    sign_in_data = {
        "email": student_data["email"],
        "password": student_data["password"]
    }
    sign_in_response = requests.post(
        baseurl + "/students/sign-in",
        data=json.dumps(sign_in_data),
        headers={"Content-Type": "application/json"}
    )
    assert sign_in_response.status_code == 200
    access_token = sign_in_response.json()["token"]

    # Получаем профиль
    profile_response = requests.get(
        baseurl + "/students",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    assert profile_response.status_code == 200
    assert profile_response.json().get("email") == student_data["email"]


def test_student_patch_profile(student_data):
    """Тест обновления профиля студента"""
    # Регистрируем студента и получаем его id
    sign_up_response = requests.post(
        baseurl + "/students/sign-up",
        data=json.dumps(student_data),
        headers={"Content-Type": "application/json"}
    )
    assert sign_up_response.status_code == 201
    student_id = sign_up_response.json().get("id")

    # Аутентификация
    sign_in_data = {
        "email": student_data["email"],
        "password": student_data["password"]
    }
    sign_in_response = requests.post(
        baseurl + "/students/sign-in",
        data=json.dumps(sign_in_data),
        headers={"Content-Type": "application/json"}
    )
    assert sign_in_response.status_code == 200
    access_token = sign_in_response.json().get("access_token")

    # Обновляем профиль
    update_data = {"name": "Updated Name"}
    patch_response = requests.patch(
        baseurl + f"/students/{student_id}",
        data=json.dumps(update_data),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    assert patch_response.status_code == 200
    assert patch_response.json().get("name") == "Updated Name"
