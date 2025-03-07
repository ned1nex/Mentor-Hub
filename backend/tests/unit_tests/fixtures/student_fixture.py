import pytest
import random

def generate_random_string(length: int = 5):
    return "".join([random.choice("ABCDEFGH") for _ in range(length)])

@pytest.fixture
def student_signatures():
    mentors = [
        {
            "name": "abcde",
            "email": generate_random_string(10) + "@gmail.com",
            "telegram": "@nizier193",
            "expertise": generate_random_string(10),
            "bio": generate_random_string(10),
            "score": random.randint(0, 1000),
            "tags": [generate_random_string(10) for _ in range(10)],
            "password": generate_random_string(10)
        }
        for __ in range(10)
    ]
    return mentors

def generate_random_email():
    return f"student{random.randint(1000, 9999)}@example.com"

@pytest.fixture
def student_data():
    """
    Фикстура возвращает данные для регистрации студента.
    Каждый запуск теста будет использовать уникальный email.
    """
    return {
        "email": generate_random_email(),
        "name": "Test Student",
        "password": "password123",
        "telegram": "Lol"
    }
