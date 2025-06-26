from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Client:
    id: str
    email: str
    phone: Optional[str] = None
    fingerprint: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Plan:
    key: str
    name: str
    price_cents: int
    duration_days: int
    category: str

@dataclass
class Subscription:
    client_id: str
    plan_key: str
    start_date: datetime
    end_date: datetime
    active: bool = True
