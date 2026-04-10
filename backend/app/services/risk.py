import math


class AdaptiveRiskEngine:
    def __init__(self, max_notional: float, max_daily_loss: float) -> None:
        self.max_notional = max_notional
        self.max_daily_loss = max_daily_loss

    def calculate_risk_score(
        self,
        quantity: float,
        price: float,
        rsi: float,
        volatility: float,
    ) -> float:
        notional = quantity * price
        exposure_component = min(1.0, notional / self.max_notional)
        rsi_component = abs(rsi - 50.0) / 50.0
        volatility_component = min(1.0, volatility)
        weighted = 0.5 * exposure_component + 0.3 * volatility_component + 0.2 * rsi_component
        return round(weighted, 4)

    def should_block(self, risk_score: float) -> bool:
        dynamic_threshold = 0.75 - 0.1 * math.sin(risk_score * math.pi)
        return risk_score > dynamic_threshold
