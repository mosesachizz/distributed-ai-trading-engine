from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.schemas.trade import TradeRequest, TradeResponse
from app.services.container import get_trade_orchestrator
from app.services.trade import TradeOrchestrator

router = APIRouter(prefix="/trades", tags=["trades"])


@router.post("", response_model=TradeResponse)
async def create_trade(
    payload: TradeRequest,
    _: str = Depends(get_current_user),
    orchestrator: TradeOrchestrator = Depends(get_trade_orchestrator),
) -> TradeResponse:
    return await orchestrator.execute(payload)
