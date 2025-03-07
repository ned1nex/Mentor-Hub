import requests
import random
from core.config import TestConfig

config = TestConfig()
baseurl = config.BACKEND_BASEURL

def generate_random_string(length: int = 5):
    return "".join([random.choice("ABCDEFGH") for _ in range(length)])


def test_make_admin():
    response = requests.post(
        baseurl + "/admin/sign-up",
        json={
            "email": generate_random_string(10) + "@gmail.com",
            "password": "nikitoska"
        }
    )
    assert response.status_code == 201
    admin_json = response.json()

    response = requests.get(
        baseurl + f"/get-role/{admin_json.get("id")}",
    )
    assert response.status_code == 200
    assert response.json().get("role") == "admin"


    response = requests.get(
        baseurl + f"/get-role",
        headers={"Authorization": f"Bearer {admin_json.get("token")}"}
    )
    assert response.status_code == 200
    assert response.json().get("role") == "admin"