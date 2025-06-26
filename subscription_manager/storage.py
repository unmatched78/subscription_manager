from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Client, Subscription

class StorageBackend(ABC):
    @abstractmethod
    def get_client_by_email(self, email: str) -> Optional[Client]:
        ...

    @abstractmethod
    def add_client(self, client: Client) -> None:
        ...

    @abstractmethod
    def get_subscriptions(self, client_id: str) -> List[Subscription]:
        ...

    @abstractmethod
    def add_subscription(self, subscription: Subscription) -> None:
        ...
