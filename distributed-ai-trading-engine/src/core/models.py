"""
Machine learning model definitions for the trading engine.
"""

import tensorflow as tf
from tensorflow.keras import layers, models

def build_trading_model(input_shape: tuple = (50, 5)) -> models.Model:
    """Build an LSTM model for trade signal prediction.
    
    Args:
        input_shape (tuple): Shape of input data (time_steps, features).
    
    Returns:
        models.Model: Compiled TensorFlow LSTM model.
    """
    model = models.Sequential([
        layers.Input(shape=input_shape),
        layers.LSTM(64, return_sequences=True),
        layers.Dropout(0.3),
        layers.LSTM(32),
        layers.Dropout(0.3),
        layers.Dense(16, activation="relu"),
        layers.Dense(1, activation="sigmoid")  # Binary prediction (buy/sell)
    ])
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )
    return model