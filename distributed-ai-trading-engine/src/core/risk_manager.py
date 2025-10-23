"""
Adaptive risk management module for the trading engine.
Ensures trades adhere to risk thresholds and market conditions.
"""

import logging
from typing import Dict
from ..utils.logger import setup_logger

class RiskManager:
    """Manages risk for trading decisions based on adaptive thresholds."""
    
    def __init__(self, max_position: float = 10000.0, volatility_threshold: float = 0.05):
        """Initialize the risk manager.
        
        Args:
            max_position (float): Maximum position size per trade.
            volatility_threshold (float): Maximum allowable market volatility.
        """
        self.logger = setup_logger(__name__)
        self.max_position = max_position
        self.volatility_threshold = volatility_threshold
        self.logger.info("RiskManager initialized with max_position: %.2f", max_position)

    def evaluate_risk(self, prediction: list, market_data: Dict) -> bool:
        """Evaluate if a trade meets risk criteria.
        
        Args:
            prediction (list): ML model prediction.
            market_data (Dict): Current market data (volatility, RSI).
        
        Returns:
            bool: True if trade is within risk limits, False otherwise.
        """
        try:
            volatility = market_data.get("volatility", 0.0)
            rsi = market_data.get("rsi", 50.0)
            if volatility > self.volatility_threshold:
                self.logger.warning("High volatility detected: %.2f", volatility)
                return False
            
            # Avoid trades in overbought (RSI > 70) or oversold (RSI < 30) conditions
            if rsi > 70 or rsi < 30:
                self.logger.warning("Extreme RSI detected: %.2f", rsi)
                return False
            
            confidence = max(prediction[0], 1 - prediction[0])
            if confidence < 0.6:  # Require at least 60% confidence
                self.logger.warning("Low prediction confidence: %.2f", confidence)
                return False
            
            return True
        
        except KeyError as e:
            self.logger.error("Invalid market data: %s", str(e))
            return False

    def calculate_position_size(self, market_data: Dict) -> float:
        """Calculate position size based on market conditions and risk limits.
        
        Args:
            market_data (Dict): Current market data.
        
        Returns:
            float: Position size for the trade.
        """
        volatility = market_data.get("volatility", 0.01)
        risk_factor = 1.0 - min(volatility, self.volatility_threshold)
        position_size = self.max_position * risk_factor
        self.logger.debug("Calculated position size: %.2f", position_size)
        return position_size