from dataclasses import dataclass

from src.repositories import AbstractRepository


@dataclass
class ServiceMixin:
    repository: AbstractRepository
