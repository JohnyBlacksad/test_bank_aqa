from http import Response
from typing import Optional, Protocol

from main.api.models.base_model import BaseModel


class CredEndpoint(Protocol):
    def post(self, model: Optional[BaseModel]) -> BaseModel | Response: ...
    def get(self, user_id: int) -> BaseModel | Response: ...
    def delete(self, user_id: int) -> BaseModel | Response: ...
