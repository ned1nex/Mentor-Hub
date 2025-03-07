import requests
from fixtures.mentor_fixture import mentor_signatures
from fixtures.student_fixture import student_signatures
from core.config import TestConfig

config = TestConfig()
baseurl = config.BACKEND_BASEURL

def test_get_stats():
    response = requests.get(
        baseurl + "/stats"
    )
    print(response.json())
    assert response.status_code == 200


def test_get_stats_by_mentor(mentor_signatures, student_signatures):
    signature = mentor_signatures[0]

    response = requests.post(
        baseurl + "/mentors/sign-up",
        json=signature
    )
    mentor_id = response.json().get("id")

    # Пусть будет один какой-то ментор, его захотят 10 студентов, он ответит на 2, откажет 3, 5 проинорит

    request_ids = []
    # Регаемся и кидаем заявку
    for student in student_signatures:
        response = requests.post(
            baseurl + "/students/sign-up",
            json=student
        )
        student = response.json()
        assert response.status_code == 201
        student_id = response.json().get("id")

        # Создаём заявки
        response = requests.post(
            baseurl + "/request",
            json={
                "mentor_id": mentor_id,
                "student_id": student_id,
                "query": "babaika",
                "status": "PENDING",
                "date": "2002-10-12"
            }
        )
        print(response.json())
        assert response.status_code == 201

        request_ids.append(response.json().get("request_id"))


    accept_id, refuse_id, pending_id = request_ids[:2], request_ids[2:5], request_ids[5:]
    for accept in accept_id:
        print("ACCEPT", accept)
        response = requests.patch(
            baseurl + f"/request/{accept}",
            json={"status": "ACCEPTED"}
        )
        assert response.status_code == 200

    for refuse in refuse_id:
        print("REFUSE", refuse)
        response = requests.patch(
            baseurl + f"/request/{refuse}",
            json={"status": "REFUSED"}
        )
        assert response.status_code == 200
    

    for refuse in pending_id:
        print("PENDING", refuse)
        response = requests.patch(
            baseurl + f"/request/{refuse}",
            json={"status": "PENDING"}
        )
        assert response.status_code == 200
    

    response = requests.get(
        baseurl + f"/stats/{mentor_id}"
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json().get("total") == 10
    assert response.json().get("pending") == 5
    assert response.json().get("refused") == 3
    assert response.json().get("accepted") == 2