# Бизнес логика
from typing import List, Tuple
from uuid import UUID

from common.dependencies import (
    get_cache_service, 
    get_password_token_service,
    get_qdrant_service,
    get_vectorise_service
)
from .models import Mentor, MentorRegisterStatus, MentorRegister
from .repository import MentorRepository

import numpy as np

class MentorRepositoryService():
    def __init__(self, db, cache):
        self.mentor_repo = MentorRepository(db, cache)
        self.cache_service = get_cache_service(cache)
        self.token_service = get_password_token_service()


    def mentor_login(self, mentor_email: str, mentor_password: str) -> MentorRegisterStatus:
        """Проверка ментора на соответствие пароля"""

        mentor = self.mentor_repo.get_mentor_by_email(mentor_email)
        status = self.token_service.verify_password(mentor_password, mentor.password)

        # Если логин пройден - выдаём новый токен (старые удаляются)
        if status:
            token = self.token_service.generate_token(str(mentor.mentor_id))
            self.cache_service.set_id_with_handler(token=token, id=str(mentor.mentor_id), handler="mentor")

            # Всё ок - возвращаем токен
            return MentorRegisterStatus(
                status=True,
                message="ok",
                token=token,
                id=mentor.mentor_id
            )
        
        else:
            # Не вошёл в систему
            return MentorRegisterStatus(
                status=False,
                message="not authenticated",
                token=None,
                id=None
            )
        

    def get_mentor_by_id(self, mentor_id: UUID):
        return self.get_mentor_by_id(mentor_id)


class MentorQdrantService():
    def __init__(self) -> None:
        self.qdrant_service = get_qdrant_service()
        self.vectorize_service = get_vectorise_service()

        self.vector_weights = {
            "tags": 0.6,
            "expertise": 0.3,
            "bio": 0.1,
        }


    def add_qdrant_mentor(self, mentor_id: str, mentor: MentorRegister):
        """Добавление ментора в кудрант на основе взвешенного вектора"""
        
        combined_tags = " ".join(mentor.tags)
        bio = mentor.bio
        expertise = mentor.expertise

        tags_vector = self.vectorize_service.get_embedding(combined_tags, vector_size=384)
        bio_vector = self.vectorize_service.get_embedding(bio, vector_size=384)
        expertise_vector = self.vectorize_service.get_embedding(expertise, vector_size=384)

        # Нормализуем вектор и применяем веса в общем векторе
        weighted_normalized_vector = (
            np.array(tags_vector)      / np.linalg.norm(tags_vector)      * self.vector_weights["tags"] +
            np.array(bio_vector)       / np.linalg.norm(bio_vector)       * self.vector_weights["bio"] +
            np.array(expertise_vector) / np.linalg.norm(expertise_vector) * self.vector_weights["expertise"]
        ).tolist()
        
        # Добавляем в векторное хранилище
        success = self.qdrant_service.add_vector(
            vector=weighted_normalized_vector, 
            uuid_str=mentor_id, 
            metadata={
                "tags": combined_tags,
                "bio": bio,
                "expertise": expertise
            }
        )

        return success
    
    def get_qdrant_mentors(self, sentence: str, threshold: float = 0.3) -> List[Tuple]:
        # Возвращает список UUId менторов
        vector = self.vectorize_service.get_embedding(sentence, vector_size=384)

        similar_results = self.qdrant_service.find_similar_vectors(
            vector, 
            score_threshold=threshold
        )

        r: List[Tuple] = []
        for mentor in similar_results:
            r.append(
                (
                    mentor["uuid"],
                    mentor["score"],
                )
            )

        return r