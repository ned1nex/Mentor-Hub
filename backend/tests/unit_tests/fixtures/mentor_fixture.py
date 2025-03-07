import pytest
import random

def generate_random_string(length: int = 5):
    return "".join([random.choice("ABCDEFGH") for _ in range(length)])

@pytest.fixture
def mentor_signatures():
    mentors = [
        {
            "name": "abcde",
            "email": generate_random_string(10) + "@gmail.com",
            "telegram": "@" + generate_random_string(10),
            "expertise": generate_random_string(10),
            "bio": generate_random_string(10),
            "score": 0,
            "tags": [generate_random_string(10) for _ in range(10)],
            "password": generate_random_string(10)
        }
        for __ in range(10)
    ]
    return mentors
