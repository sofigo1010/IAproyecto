# src/data/preprocessing.py

import pandas as pd
import numpy as np

def preprocess_sales_data(
    df: pd.DataFrame,
    freq: str = "W"
) -> pd.DataFrame:
    """
    - Convierte 'date' a índice datetime y ordena.
    - Resamplea a freq (p.ej. 'D', 'W', 'M') sumando ventas.
    - Rellena valores faltantes por interpolación lineal.
    - Atenúa outliers usando IQR (clip).
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date").sort_index()

    # Resample
    df_resampled = df.resample(freq).sum()

    # Interpolación de sales faltantes
    df_resampled["sales"] = df_resampled["sales"].interpolate(method="linear")

    # Caps de outliers (IQR)
    q1 = df_resampled["sales"].quantile(0.25)
    q3 = df_resampled["sales"].quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    df_resampled["sales"] = df_resampled["sales"].clip(lower, upper)

    return df_resampled
