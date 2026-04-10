from app.services.risk import AdaptiveRiskEngine


def test_risk_score_in_range() -> None:
    engine = AdaptiveRiskEngine(max_notional=1_000_000, max_daily_loss=50_000)
    score = engine.calculate_risk_score(quantity=10, price=100, rsi=55, volatility=0.2)
    assert 0 <= score <= 1


def test_high_risk_blocks() -> None:
    engine = AdaptiveRiskEngine(max_notional=1_000_000, max_daily_loss=50_000)
    assert engine.should_block(0.95)
