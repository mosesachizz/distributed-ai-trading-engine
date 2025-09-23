"""
Script to train the LSTM model for trade signal prediction using synthetic market data.
"""

import numpy as np
import tensorflow as tf
from src.core.models import build_trading_model
from src.utils.logger import setup_logger

def generate_synthetic_market_data(samples: int = 10000, time_steps: int = 50) -> tuple:
    """Generate synthetic market data with realistic patterns for LSTM.
    
    Args:
        samples (int): Number of data points to generate.
        time_steps (int): Number of time steps for LSTM input.
    
    Returns:
        tuple: (X, y) where X is feature array (samples, time_steps, features) and y is labels.
    """
    logger = setup_logger(__name__)
    logger.info("Generating synthetic market data...")
    
    # Initialize arrays
    X = np.zeros((samples, time_steps, 5))  # Features: price, volume, volatility, SMA, RSI
    y = np.zeros(samples)  # Labels: 0 (sell), 1 (buy)
    
    # Simulate price series with random walk and momentum
    prices = [100.0]  # Starting price
    for _ in range(samples + time_steps - 1):
        prices.append(prices[-1] * (1 + np.random.normal(0, 0.01)))
    
    # Calculate features
    for i in range(samples):
        for t in range(time_steps):
            idx = i + t
            price = prices[idx]
            volume = np.random.randint(500, 5000)
            volatility = np.std(prices[max(0, idx-20):idx+1]) / np.mean(prices[max(0, idx-20):idx+1])
            
            # Calculate SMA (20 periods)
            sma = np.mean(prices[max(0, idx-20):idx+1]) if idx >= 20 else price
            
            # Calculate RSI (14 periods)
            if idx >= 14:
                deltas = np.diff(prices[max(0, idx-14):idx+1])
                gains = np.where(deltas > 0, deltas, 0)
                losses = np.where(deltas < 0, -deltas, 0)
                avg_gain = np.mean(gains)
                avg_loss = np.mean(losses) + 1e-10
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
            else:
                rsi = 50.0
            
            # Normalize features
            X[i, t] = [
                price / 1000.0,
                volume / 10000.0,
                volatility,
                sma / 1000.0,
                rsi / 100.0
            ]
        
        # Generate labels: Buy if RSI < 30 (oversold), Sell if RSI > 70 (overbought)
        rsi = X[i, -1, 4] * 100.0  # Denormalize RSI
        y[i] = 1 if rsi < 30 else 0 if rsi > 70 else np.random.randint(0, 2)
    
    logger.info("Generated %d synthetic data points with %d time steps", samples, time_steps)
    return X, y

def train_model():
    """Train and save the LSTM trading model."""
    logger = setup_logger(__name__)
    logger.info("Starting model training...")
    
    # Generate synthetic data
    X, y = generate_synthetic_market_data()
    
    # Split data
    train_size = int(0.8 * len(X))
    X_train, X_val = X[:train_size], X[train_size:]
    y_train, y_val = y[:train_size], y[train_size:]
    
    # Build and train model
    model = build_trading_model(input_shape=(50, 5))
    model.fit(
        X_train,
        y_train,
        epochs=20,
        batch_size=64,
        validation_data=(X_val, y_val),
        verbose=1
    )
    
    # Save model
    model.save("models/trading_model.h5")
    logger.info("Model training completed and saved to models/trading_model.h5")

if __name__ == "__main__":
    train_model()