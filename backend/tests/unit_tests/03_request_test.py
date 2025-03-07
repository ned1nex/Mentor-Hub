import requests
import random
from uuid import uuid4
from typing import List, Dict

from fixtures.mentor_fixture import mentor_signatures
from fixtures.student_fixture import student_signatures

from core.config import TestConfig

config = TestConfig()
baseurl = config.BACKEND_BASEURL

def generate_random_string(n = 10):
    return "".join([random.choice(list("ASHDCHSD")) for _ in range(10)])


def test_create_normal_request(mentor_signatures, student_signatures):
    """Создание обычной заявки"""
    mentors_ids = []
    for mentor in mentor_signatures:
        response = requests.post(
            baseurl + "/mentors/sign-up",
            json=mentor
        )
        assert response.status_code == 201
        mentors_ids.append(response.json().get('id'))

    student_ids = []
    for student in student_signatures:
        response = requests.post(
            baseurl + "/students/sign-up",
            json=student
        )
        assert response.status_code == 201  
        student_ids.append(response.json().get('id'))


    ids = []
    for student, mentor in zip(student_ids, mentors_ids):
        response = requests.post(
            baseurl + "/request",
            json={
                "student_id": student,
                "mentor_id": mentor,
                "query": "some query",
                "status": "PENDING",
                "date": "2025-12-23"
            }
        )
        assert response.status_code == 201
        ids.append(response.json().get("request_id"))


    for id in ids:
        response = requests.get(baseurl + f"/request/{id}")
        print(id, response.json())
        assert response.status_code == 200


def test_create_broken_request(mentor_signatures, student_signatures):
    broken_requests: List[Dict] = [
        {
            "student_id": str(uuid4()),
            "mentor_id": str(uuid4()),
            "query": "some query",
            "status": "NONEXISTENT", # Такого статуса не существует
            "date": "2025-12-23"
        },
        {
            "student_id": str(uuid4()),
            "mentor_id": str(uuid4()),
            "query": "some query",
            "status": "PENDING",
            "date": "2025-13-23" # Тринадцатый месяц в году
        },
        {
            "student_id": str(uuid4()),
            "mentor_id": str(uuid4()),
            "query": 123, # Query - int 
            "status": "PENDING",
            "date": "2025-12-23"
        },
        {
            "student_id": str(uuid4()) + "1", # Это не UUID
            "mentor_id": str(uuid4()),
            "query": "123123123",
            "status": "PENDING",
            "date": "2025-12-23"
        },
        {
            "student_id": str(uuid4()),
            "query": "123123123", # Нет mentor_id
            "status": "PENDING",
            "date": "2025-12-23"
        }
    ] 
    for broken_request in broken_requests:
        response = requests.post(
            baseurl + "/request",
            json=broken_request
        )
        assert response.status_code == 422



def test_patch_request_normal(mentor_signatures, student_signatures):
    """Тест на изменение реквеста"""
    mentors_ids = []
    for mentor in mentor_signatures:
        response = requests.post(
            baseurl + "/mentors/sign-up",
            json=mentor
        )
        assert response.status_code == 201

        mentors_ids.append(response.json().get('id'))

    student_ids = []
    for student in student_signatures:
        response = requests.post(
            baseurl + "/students/sign-up",
            json=student
        )
        assert response.status_code == 201  
        student_ids.append(response.json().get('id'))


    ids = []
    for student, mentor in zip(student_ids, mentors_ids):
        response = requests.post(
            baseurl + "/request",
            json={
                "student_id": student,
                "mentor_id": mentor,
                "query": "some query",
                "status": "PENDING",
                "date": "2025-12-23"
            }
        )
        print("request id: ", response.json().get("request_id"))
        assert response.status_code == 201
        ids.append(response.json().get("request_id"))


    patch_model = {
        "query": "some another query",
        "status": "ACCEPTED",
        "date": "2020-09-03"
    }
    for id in ids:
        response = requests.patch(
            baseurl + f"/request/{id}",
            json=patch_model
        )
        print("patching: ", id)
        print(response.json())
        assert response.status_code == 200

        response = requests.get(
            baseurl + f"/request/{id}"
        )
        assert response.status_code == 200

        answer = response.json()
        assert answer.get("query") == "some another query"
        assert answer.get("status") == "ACCEPTED"
        assert "2020-09-03" in answer.get("date")