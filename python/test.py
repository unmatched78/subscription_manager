from subscription_manager.storage_sqlalchemy import SQLAlchemyBackend
from subscription_manager.services import SubscriptionService
from subscription_manager.models import Plan, Client
from uuid import uuid4

def gen_id(): return str(uuid4())

# 1) Backend & plans
backend = SQLAlchemyBackend("postgresql+psycopg2://user:pass@localhost/db")
plans = {
    "free_trial": Plan("free_trial", "14-day Free Trial", 0,    14, "Trial"),
    "basic":      Plan("basic",      "Basic Plan",       999,  30, "Paid"),
    "pro":        Plan("pro",        "Pro Plan",        1999, 30, "Paid"),
}

# 2) Service
svc = SubscriptionService(backend, plans, id_generator=gen_id)

# 3) Use
client = svc.register_client("alice@example.com", phone="+250780000000")
trial  = svc.start_subscription(client, "free_trial")
print("Expires:", trial.end_date)
