from abc import ABC, abstractmethod
from typing import Any, Callable

from src.main.api.models.base_model import BaseModel

class Requester(ABC):
    def __init__(self, request_spec: dict[str, Any], response_spec: Callable):
        self.headers = request_spec.get('headers')
        self.base_url = request_spec.get('base_url')
        self.response_spec = response_spec

    @abstractmethod
    def post(self, model: BaseModel):
        pass
