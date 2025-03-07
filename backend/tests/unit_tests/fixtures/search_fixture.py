import pytest
import random

def generate_random_string(n: int = 10):
    return "".join([random.choice("ABCDEFGH") for _ in range(n)])

@pytest.fixture
def mentor_search_fixtures():
    class Data:
        first_triple = (
            {
                "mentor_id": "001",
                "name": "Александр ML-Эксперт",
                "email": generate_random_string(10) + "@example.com",
                "telegram": "@alex_ml",
                "expertise": "Разработка моделей машинного обучения и нейросетей. Опыт работы в Яндекс и Google.",
                "bio": "Data Scientist с 8-летним опытом. Защитил диссертацию по применению ML в финтех индустрии. Люблю кофе и горы.",
                "score": 0,
                "tags": ["Machine Learning", "Python", "TensorFlow", "Neural Networks", "Computer Vision"]
            },
            "Ищу ментора по машинному обучению и компьютерному зрению",
            "Александр ML-Эксперт"
        )
        
        second_triple = (
            {
                "mentor_id": "002",
                "name": "Елена DevOps-Гуру",
                "email": generate_random_string(10) + "@example.com",
                "telegram": "@elena_devops",
                "expertise": "Построение масштабируемой инфраструктуры, CI/CD, контейнеризация в Kubernetes, опыт с AWS и Google Cloud.",
                "bio": "Более 7 лет опыта в инфраструктурной разработке. Увлекаюсь автоматизацией, люблю шахматы.",
                "score": 0,
                "tags": ["DevOps", "Kubernetes", "Docker", "Terraform", "AWS", "GCP", "CI/CD"]
            },
            "Хочу научиться строить микросервисы и настраивать облачную инфраструктуру в AWS",
            "Елена DevOps-Гуру"
        )
        
        third_triple = (
            {
                "mentor_id": "003",
                "name": "Сергей Фронтенд-Мастер",
                "email": generate_random_string(10) + "@example.com",
                "telegram": "@sergey_frontend",
                "expertise": "Разработка современных веб-приложений, SPA, PWA. Глубокий опыт работы с React, Vue и архитектурой фронтенда.",
                "bio": "Frontend developer с фокусом на пользовательский опыт и производительность. Люблю делиться знаниями и проводить код-ревью.",
                "score": 0,
                "tags": ["JavaScript", "TypeScript", "React", "Vue", "Frontend", "Web Development", "Performance"]
            },
            "Я только начал свой путь в IT, интересует веб-разработка, хочу научиться делать современные интерфейсы и анимации, думал о React или может Vue, еще интересно как делать красивые сайты, может что-то с дизайном связанное. Есть много идей для проектов, но не знаю с чего начать.",
            "Сергей Фронтенд-Мастер"
        )
        
        fourth_triple = (
            {
                "mentor_id": "004",
                "name": "Мария Алгоритмы-Про",
                "email": generate_random_string(10) + "@example.com",
                "telegram": "@maria_algorithms",
                "expertise": "Алгоритмы и структуры данных, оптимизация кода, подготовка к собеседованиям в FAANG компании.",
                "bio": "Выпускница МФТИ, работала в Amazon и Facebook. Подготовила более 200 студентов к собеседованиям. Автор курса 'LeetCode от А до Я'.",
                "score": 0,
                "tags": ["Algorithms", "Data Structures", "Problem Solving", "Competitive Programming", "Interview Prep"] 
            },
            "Хочу пройти собеседование в крупную технологическую компанию, нужна помощь с подготовкой",
            "Мария Алгоритмы-Про"
        )
        
        fifth_triple = (
            {
                "mentor_id": "005",
                "name": "Павел Fullstack-Разработчик",
                "email": generate_random_string(10) + "@example.com",
                "telegram": "@pavel_fullstack",
                "expertise": "Полный стек веб-разработки с акцентом на Java Spring и Angular. Разработка REST API, работа с базами данных.",
                "bio": "Более 10 лет опыта fullstack разработки. Разработал несколько высоконагруженных финансовых приложений. Люблю скалолазание и хорошую документацию :)",
                "score": 0,
                "tags": ["Java", "Spring", "Angular", "SQL", "REST API", "Microservices", "Fullstack"]
            },
            "Нужен ментор для создания корпоративного приложения с бэкендом на Java и фронтендом на Angular, с микросервисной архитектурой",
            "Павел Fullstack-Разработчик"
        )
        
    return Data()
