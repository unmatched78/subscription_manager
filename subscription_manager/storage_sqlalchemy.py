from typing import List, Optional
from sqlalchemy import Column, String, Integer, DateTime, Boolean, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from datetime import datetime

from .models import Client as ClientDC, Subscription as SubscriptionDC
from .storage import StorageBackend

Base = declarative_base()

class ClientORM(Base):
    __tablename__ = "clients"
    id          = Column(String, primary_key=True)
    email       = Column(String, unique=True, nullable=False, index=True)
    phone       = Column(String, nullable=True)
    fingerprint = Column(String, nullable=True)
    created_at  = Column(DateTime, default=datetime.utcnow)
    subscriptions = relationship("SubscriptionORM", back_populates="client")

class SubscriptionORM(Base):
    __tablename__ = "subscriptions"
    id         = Column(Integer, primary_key=True, autoincrement=True)
    client_id  = Column(String, ForeignKey("clients.id"), nullable=False)
    plan_key   = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date   = Column(DateTime, nullable=False)
    active     = Column(Boolean, default=True)
    client     = relationship("ClientORM", back_populates="subscriptions")

class SQLAlchemyBackend(StorageBackend):
    def __init__(self, database_url: str):
        engine = create_engine(database_url, future=True)
        Base.metadata.create_all(engine)
        self.SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

    def _session(self) -> Session:
        return self.SessionLocal()

    def get_client_by_email(self, email: str) -> Optional[ClientDC]:
        with self._session() as sess:
            orm = sess.query(ClientORM).filter_by(email=email).one_or_none()
            if orm is None:
                return None
            return ClientDC(
                id=orm.id,
                email=orm.email,
                phone=orm.phone,
                fingerprint=orm.fingerprint,
                created_at=orm.created_at
            )

    def add_client(self, client: ClientDC) -> None:
        with self._session() as sess:
            orm = ClientORM(
                id=client.id,
                email=client.email,
                phone=client.phone,
                fingerprint=client.fingerprint,
                created_at=client.created_at
            )
            sess.add(orm)
            sess.commit()

    def get_subscriptions(self, client_id: str) -> List[SubscriptionDC]:
        with self._session() as sess:
            orms = sess.query(SubscriptionORM).filter_by(client_id=client_id).all()
            return [
                SubscriptionDC(
                    client_id=o.client_id,
                    plan_key=o.plan_key,
                    start_date=o.start_date,
                    end_date=o.end_date,
                    active=o.active
                )
                for o in orms
            ]

    def add_subscription(self, subscription: SubscriptionDC) -> None:
        with self._session() as sess:
            orm = SubscriptionORM(
                client_id=subscription.client_id,
                plan_key=subscription.plan_key,
                start_date=subscription.start_date,
                end_date=subscription.end_date,
                active=subscription.active
            )
            sess.add(orm)
            sess.commit()
