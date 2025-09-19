"""
REST API for trade execution using FastAPI with JWT authentication.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Dict
from jose import JWTError, jwt
from ..core.trade_engine import TradeEngine
from ..utils.logger import setup_logger
from ..utils.auth import verify_token

app = FastAPI(title="Distributed AI Trading Engine API")
logger = setup_logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TradeRequest(BaseModel):
    """Pydantic model for trade request payload."""
    symbol: str
    price: float
    volume: float
    volatility: float
    sma: float
    rsi: float

@app.post("/trade")
async def execute_trade(request: TradeRequest, token: str = Depends(oauth2_scheme)) -> Dict:
    """Execute a trade via HTTP request.
    
    Args:
        request (TradeRequest): Trade request payload.
        token (str): JWT token for authentication.
    
    Returns:
        Dict: Trade execution details.
    """
    try:
        verify_token(token)  # Authenticate user
        trade_engine = app.state.trade_engine
        market_data = request.dict()
        result = trade_engine.execute_trade(market_data)
        if result is None:
            raise HTTPException(status_code=400, detail="Trade rejected by risk manager")
        return result
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error("Trade API error: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
async def startup_event():
    """Initialize trade engine on API startup."""
    from ..core.risk_manager import RiskManager
    from ..core.market_data import MarketData
    app.state.trade_engine = TradeEngine(
        model_path="models/trading_model.h5",
        risk_manager=RiskManager(),
        market_data=MarketData()
    )
    logger.info("Trade API initialized")