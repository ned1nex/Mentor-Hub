from typing import Dict, List, Optional
import requests
from requests import Response

from core.config import config

class APIService():
    def __init__(self) -> None:
        self.baseurl = config.BACKEND_BASEURL.rstrip("/")


    def get_search_result(self, query) -> List[Dict]:
        response = requests.get(
            self.baseurl + "/mentors",
            params={"query": query}
        )
        if response.status_code != 200:
            return []

        return response.json()
    

    def make_mentor(self, mentor: Dict) -> Optional[Dict]:
        response = requests.post(
            self.baseurl + "/mentors/sign-up",
            json=mentor
        )
        if response.status_code != 201:
            return None

        mentor_json = response.json()
        return mentor_json
    