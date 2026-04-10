from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Side(str, Enum):
    buy = "buy"
    sell = "sell"


class TradeRequest(BaseModel):
    symbol: str = Field(min_length=2, max_length=10)
    side: Side
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)


class TradeResponse(BaseModel):
    accepted: bool
    order_id: str
    model_score: float
    risk_score: float
    created_at: datetime
