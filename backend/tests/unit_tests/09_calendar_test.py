import requests
from core.config import TestConfig

config = TestConfig()
baseurl = config.BACKEND_BASEURL

def test_make_normal_calendar_file():
    response = requests.post(
        baseurl + "/calendar",
        json={"date": "2020-12-23"}
    )
    assert response.status_code == 200


def test_make_invalid_calendar():
    response = requests.post(
        baseurl + "/calendar",
        json={"date": 10} # invalid date
    )
    assert response.status_code == 422


def test_make_invalid_calendar_wrong_format():
    response = requests.post(
        baseurl + "/calendar",
        json={"date": "13123-43-111111"}
    )
    assert response.status_code == 422