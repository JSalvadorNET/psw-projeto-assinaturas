from sqlmodel import Field, SQLModel, create_engine, Relationship
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class Subscription(SQLModel, table=True):
    id: int = Field(primary_key=True)
    company: str
    site: Optional[str] = None # optional data
    date_assignature: date
    value: Decimal
    
class Payments(SQLModel, table=True):
    id: int = Field(primary_key=True)
    subscription_id: int = Field(foreign_key="subscription.id")
    subscription: Subscription = Relationship()
    date: date
