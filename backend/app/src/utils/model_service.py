import os
import requests
import numpy as np
from typing import List, Optional

from core.config import config

class VectorService:
    def __init__(self):
        self.ollama_host = config.OLLAMA_HOST
        self.ollama_port = config.OLLAMA_PORT
        self.ollama_url = f"http://{self.ollama_host}:{self.ollama_port}"
        self.model_name = "all-minilm:latest"  # Имя модели Ollama
        
        # Проверяем доступность Ollama при инициализации
        self.check_ollama_availability()
    
    def check_ollama_availability(self) -> bool:
        """Проверяет, доступен ли сервис Ollama."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                available_models = [m.get("name") for m in models]
                
                # Проверяем наличие требуемой модели
                if self.model_name not in available_models:
                    print(f"Модель {self.model_name} не найдена. Доступные модели: {available_models}")
                    print(f"Пытаемся загрузить модель {self.model_name}...")
                    self.pull_model()
                return True
            return False
        except Exception as e:
            print(f"Ошибка при проверке доступности Ollama: {e}")
            return False
    
    def pull_model(self) -> bool:
        """Загружает модель, если она отсутствует."""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/pull",
                json={"name": self.model_name}
            )
            if response.status_code == 200:
                print(f"Модель {self.model_name} успешно загружена")
                return True
            else:
                print(f"Ошибка загрузки модели: {response.text}")
                return False
        except Exception as e:
            print(f"Ошибка при загрузке модели: {e}")
            return False
    
    def get_embedding(self, text: str, vector_size: Optional[int] = None) -> List[float]:
        try:
            response = requests.post(
                f"{self.ollama_url}/api/embeddings",
                json={
                    "model": self.model_name,
                    "prompt": text
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                embedding = data.get("embedding", [])
                
                # Если указана требуемая размерность вектора
                if vector_size and len(embedding) != vector_size:
                    embedding = np.array(embedding)
                    if len(embedding) > vector_size:
                        embedding = embedding[:vector_size]
                    else:
                        embedding = np.pad(embedding, (0, vector_size - len(embedding)))
                    embedding = embedding.tolist()
                
                return embedding
            else:
                print(f"Ошибка API Ollama: {response.status_code}, {response.text}")
                # Возвращаем нулевой вектор в случае ошибки
                return [0.0] * (vector_size or 384)
        except Exception as e:
            print(f"Ошибка при получении эмбеддинга: {e}")
            # Возвращаем нулевой вектор в случае исключения
            return [0.0] * (vector_size or 384)
