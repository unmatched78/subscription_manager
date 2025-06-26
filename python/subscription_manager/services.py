from datetime import datetime, timedelta
from typing import Dict, Callable
from .models import Client, Subscription, Plan
from .storage import StorageBackend
from .exceptions import TrialAlreadyUsed, PlanNotFound

class SubscriptionService:
    def __init__(
        self,
        storage: StorageBackend,
        plans: Dict[str, Plan],
        id_generator: Callable[[], str],
    ):
        self.storage = storage
        self.plans = plans
        self.id_generator = id_generator

    def register_client(self, email: str, phone: str = None, fingerprint: str = None) -> Client:
        existing = self.storage.get_client_by_email(email)
        if existing:
            return existing
        client = Client(
            id=self.id_generator(),
            email=email,
            phone=phone,
            fingerprint=fingerprint
        )
        self.storage.add_client(client)
        return client

    def start_subscription(self, client: Client, plan_key: str) -> Subscription:
        if plan_key not in self.plans:
            raise PlanNotFound(f"No such plan: {plan_key}")

        plan = self.plans[plan_key]

        if plan_key == "free_trial":
            subs = self.storage.get_subscriptions(client.id)
            if any(s.plan_key == "free_trial" for s in subs):
                raise TrialAlreadyUsed("Client has already used the free trial")

        now = datetime.utcnow()
        sub = Subscription(
            client_id=client.id,
            plan_key=plan_key,
            start_date=now,
            end_date=now + timedelta(days=plan.duration_days),
            active=True
        )
        self.storage.add_subscription(sub)
        return sub

    def renew_subscription(self, client: Client, plan_key: str) -> Subscription:
        sub = self.start_subscription(client, plan_key)
        return sub

    def cancel_subscription(self, client: Client, plan_key: str) -> None:
        # simplistic: mark active=False on all matching
        subs = self.storage.get_subscriptions(client.id)
        for s in subs:
            if s.plan_key == plan_key and s.active:
                s.active = False
        # you'd add update logic in storage if needed

    def is_active(self, client: Client, plan_key: str) -> bool:
        subs = self.storage.get_subscriptions(client.id)
        now = datetime.utcnow()
        return any(
            s.plan_key == plan_key and s.active and s.start_date <= now < s.end_date
            for s in subs
        )
