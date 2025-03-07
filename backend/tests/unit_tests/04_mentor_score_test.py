import requests
from fixtures.mentor_fixture import mentor_signatures
from core.config import TestConfig

config = TestConfig()
baseurl = config.BACKEND_BASEURL

def test_score_increment(mentor_signatures):
    ids = []
    for mentor in mentor_signatures[0:2]: # два ментора
        response = requests.post(
            baseurl + "/mentors/sign-up",
            json=mentor
        )
        assert response.status_code == 201

        ids.append(response.json().get("id"))


    id1, id2 = ids
    # Начисляем скоры

    # У первого будет 50
    for _ in range(10):
        response = requests.post(
            baseurl + f"/mentors/{id1}/score",
            json={"score":5}
        )
        print(response.json())
        assert response.status_code == 200

    # У второго 100
    for _ in range(20):
        response = requests.post(
            baseurl + f"/mentors/{id2}/score",
            json={"score":5}
        )
        assert response.status_code == 200



    response1 = requests.get(baseurl + f"/mentors/{id1}")
    assert response1.status_code == 200

    print(response1.json())
    assert response1.json().get("score") == 50

    response2 = requests.get(baseurl + f"/mentors/{id2}")
    assert response2.status_code == 200
    assert response2.json().get("score") == 100