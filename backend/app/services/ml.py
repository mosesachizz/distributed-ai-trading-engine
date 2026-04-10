from __future__ import annotations

import numpy as np


class LSTMPredictor:
    """Wrapper around an LSTM-like model inference interface.

    This implementation keeps inference lightweight and deterministic
    for local development while preserving the expected shape contract.
    """

    def __init__(self, model_path: str) -> None:
        self.model_path = model_path

    def predict_edge(self, price: float, rsi: float, volatility: float) -> float:
        features = np.array([price / 1000.0, rsi / 100.0, volatility], dtype=np.float32)
        pseudo_signal = float(np.dot(features, np.array([0.5, 0.3, 0.2], dtype=np.float32)))
        return round(max(0.0, min(1.0, pseudo_signal)), 4)
