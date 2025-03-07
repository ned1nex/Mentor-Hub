import requests
from fixtures.mentor_fixture import mentor_signatures
from fixtures.student_fixture import student_signatures
from core.config import TestConfig

config = TestConfig()
baseurl = config.BACKEND_BASEURL

def test_get_role_by_id(mentor_signatures, student_signatures):

    # Регистрируем менторов
    mentor_ids = []
    for fixture in mentor_signatures:
        response = requests.post(
            baseurl + "/mentors/sign-up",
            json=fixture
        )
        assert response.status_code == 201

        response_json = response.json()
        mentor_ids.append(response_json.get("id"))


    # Регистрируем студентов
    student_ids = []
    for fixture in student_signatures:
        response = requests.post(
            baseurl + "/students/sign-up",
            json=fixture
        )
        assert response.status_code == 201

        response_json = response.json()
        student_ids.append(response_json.get("id"))


    for student_id, mentor_id in zip(student_ids, mentor_ids):
        response = requests.get(
            baseurl + f"/get-role/{student_id}",
        )
        assert response.status_code == 200
        assert response.json().get("role") == "student"

        response = requests.get(
            baseurl + f"/get-role/{mentor_id}",
        )
        assert response.status_code == 200
        assert response.json().get("role") == "mentor"



def test_get_role_by_token(mentor_signatures, student_signatures):

    # Регистрируем менторов
    mentor_tokens = []
    for fixture in mentor_signatures:
        response = requests.post(
            baseurl + "/mentors/sign-up",
            json=fixture
        )
        assert response.status_code == 201

        response_json = response.json()
        mentor_tokens.append(response_json.get("token"))


    # Регистрируем студентов
    student_tokens = []
    for fixture in student_signatures:
        response = requests.post(
            baseurl + "/students/sign-up",
            json=fixture
        )
        assert response.status_code == 201

        response_json = response.json()
        student_tokens.append(response_json.get("token"))


    for student_token, mentor_token in zip(student_tokens, mentor_tokens):
        response = requests.get(
            baseurl + f"/get-role",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 200
        assert response.json().get("role") == "student"

        response = requests.get(
            baseurl + f"/get-role",
            headers={"Authorization": f"Bearer {mentor_token}"}
        )
        assert response.status_code == 200
        assert response.json().get("role") == "mentor"



def test_get_role_not_a_token(mentor_signatures, student_signatures):
    """Тест на ошибку валидации - не настоящий токен"""
    mentor_token = "abc" # Это не настоящий токен
    response = requests.get(
        baseurl + f"/get-role",
        headers={"Authorization": f"Bearer {mentor_token}"}
    )
    assert response.status_code == 401