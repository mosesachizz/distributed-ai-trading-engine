"""
Market data processing module for the trading engine.
Handles data ingestion, preprocessing, and subscription for real-time updates.
"""

import logging
from typing import Dict, Callable, List
import numpy as np
from ..utils.logger import setup_logger

class MarketData:
    """Processes market data for ML model input and trade execution."""
    
    def __init__(self):
        """Initialize the market data processor."""
        self.logger = setup_logger(__name__)
        self.subscribers = []
        self.price_history = []  # Store recent prices for technical indicators
        self.max_history = 50  # Window for moving averages and RSI

    def preprocess(self, market_data: Dict) -> List[float]:
        """Preprocess market data for ML model input.
        
        Args:
            market_data (Dict): Raw market data with price, volume, volatility.
        
        Returns:
            List[float]: Preprocessed features (price, volume, volatility, SMA, RSI).
        """
        try:
            # Extract raw features
            price = market_data.get("price", 0.0)
            volume = market_data.get("volume", 0.0)
            volatility = market_data.get("volatility", 0.0)
            
            # Update price history for technical indicators
            self.price_history.append(price)
            if len(self.price_history) > self.max_history:
                self.price_history.pop(0)
            
            # Calculate Simple Moving Average (SMA) over 20 periods
            sma = np.mean(self.price_history[-20:]) if len(self.price_history) >= 20 else price
            
            # Calculate Relative Strength Index (RSI) over 14 periods
            rsi = self._calculate_rsi() if len(self.price_history) >= 14 else 50.0
            
            # Normalize features for ML model
            features = [
                price / 1000.0,  # Normalize price
                volume / 10000.0,  # Normalize volume
                volatility,
                sma / 1000.0,  # Normalize SMA
                rsi / 100.0  # Normalize RSI
            ]
            self.logger.debug("Preprocessed features: %s", features)
            return features
        except KeyError as e:
            self.logger.error("Invalid market data for preprocessing: %s", str(e))
            return [0.0] * 5  # Fallback: 5 features

    def _calculate_rsi(self) -> float:
        """Calculate RSI over the last 14 periods.
        
        Returns:
            float: RSI value (0-100).
        """
        prices = np.array(self.price_history[-14:])
        if len(prices) < 14:
            return 50.0
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses) + 1e-10  # Avoid division by zero
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def subscribe(self, callback: Callable):
        """Subscribe a callback to receive processed market data.
        
        Args:
            callback (Callable): Function to process market data.
        """
        self.subscribers.append(callback)
        self.logger.info("Subscribed callback to market data: %s", callback.__name__)

    def process(self, market_data: Dict):
        """Process incoming market data and notify subscribers.
        
        Args:
            market_data (Dict): Raw market data.
        """
        try:
            for subscriber in self.subscribers:
                subscriber(market_data)
        except Exception as e:
            self.logger.error("Error processing market data: %s", str(e))