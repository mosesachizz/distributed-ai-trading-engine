"""
Core trading engine for executing trades with sub-50ms latency.
Integrates ML models for predictions and adaptive risk management.
"""

import time
import logging
from typing import Dict, Optional
import tensorflow as tf
import numpy as np
from .risk_manager import RiskManager
from .market_data import MarketData
from ..utils.logger import setup_logger
from ..utils.metrics import MetricsCollector

class TradeEngine:
    """High-frequency trading engine with ML-driven decision-making."""
    
    def __init__(self, model_path: str, risk_manager: RiskManager, market_data: MarketData):
        """Initialize the trading engine.
        
        Args:
            model_path (str): Path to pre-trained ML model.
            risk_manager (RiskManager): Instance of risk management module.
            market_data (MarketData): Instance of market data processor.
        """
        self.logger = setup_logger(__name__)
        self.model = tf.keras.models.load_model(model_path)
        self.risk_manager = risk_manager
        self.market_data = market_data
        self.metrics = MetricsCollector()
        self.logger.info("TradeEngine initialized with model: %s", model_path)

    def execute_trade(self, market_data: Dict) -> Optional[Dict]:
        """Execute a trade based on market data and ML predictions.
        
        Args:
            market_data (Dict): Real-time market data (price, volume, volatility, SMA, RSI).
        
        Returns:
            Optional[Dict]: Trade execution details or None if rejected.
        """
        start_time = time.time()
        try:
            # Preprocess market data for ML model
            features = self.market_data.preprocess(market_data)
            prediction = self.model.predict(np.array([features]), verbose=0)[0]
            
            # Apply risk checks
            if not self.risk_manager.evaluate_risk(prediction, market_data):
                self.logger.warning("Trade rejected due to risk thresholds: %s", market_data)
                self.metrics.record_trade_rejection()
                return None
            
            # Simulate trade execution
            trade = {
                "symbol": market_data["symbol"],
                "action": "buy" if prediction[0] > 0.5 else "sell",
                "quantity": self.risk_manager.calculate_position_size(market_data),
                "price": market_data["price"],
                "timestamp": time.time()
            }
            
            # Log latency and metrics
            latency = (time.time() - start_time) * 1000  # Convert to ms
            self.metrics.record_trade_latency(latency)
            self.metrics.record_trade_execution()
            self.logger.info("Trade executed: %s, Latency: %.2fms", trade, latency)
            return trade
        
        except Exception as e:
            self.logger.error("Trade execution failed: %s", str(e))
            self.metrics.record_error()
            return None

    def start(self):
        """Start the trading engine, subscribing to market data."""
        self.logger.info("Starting TradeEngine...")
        self.market_data.subscribe(self.execute_trade)