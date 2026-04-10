import pathlib

import numpy as np
import tensorflow as tf


def build_model(sequence_length: int = 20) -> tf.keras.Model:
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(sequence_length, 3)),
            tf.keras.layers.LSTM(64, return_sequences=True),
            tf.keras.layers.LSTM(32),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model


def main() -> None:
    np.random.seed(42)
    tf.random.set_seed(42)
    x_train = np.random.random((2000, 20, 3)).astype(np.float32)
    y_train = np.random.randint(0, 2, size=(2000, 1)).astype(np.float32)

    model = build_model()
    model.fit(x_train, y_train, epochs=2, batch_size=32, verbose=1)

    output_path = pathlib.Path("models")
    output_path.mkdir(parents=True, exist_ok=True)
    model.save(output_path / "lstm_model.keras")


if __name__ == "__main__":
    main()
