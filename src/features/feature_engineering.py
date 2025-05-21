# src/features/feature_engineering.py

import pandas as pd
import numpy as np
from typing import List, Optional


def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extrae características de calendario de un índice datetime:
      - dayofweek (0=lun … 6=dom)
      - month, quarter
      - is_weekend (1 si sab/dom)
    """
    df = df.copy()
    idx = pd.to_datetime(df.index)
    df["dayofweek"] = idx.dayofweek
    df["month"]      = idx.month
    df["quarter"]    = idx.quarter
    df["is_weekend"] = idx.dayofweek.isin([5, 6]).astype(int)
    return df


def add_lag_features(
    df: pd.DataFrame,
    lags: List[int]
) -> pd.DataFrame:
    """
    Crea columnas de ventas con retrasos (lag):
      - lag_1, lag_7, lag_14, etc.
    """
    df = df.copy()
    for lag in lags:
        df[f"lag_{lag}"] = df["sales"].shift(lag)
    return df


def add_rolling_features(
    df: pd.DataFrame,
    windows: List[int]
) -> pd.DataFrame:
    """
    Para cada ventana crea:
      - roll_mean_{w}: media móvil de tamaño w (shift(1) para evitar lookahead)
      - roll_std_{w}: desviación estándar de tamaño w
    """
    df = df.copy()
    for w in windows:
        df[f"roll_mean_{w}"] = df["sales"].shift(1).rolling(w).mean()
        df[f"roll_std_{w}"]  = df["sales"].shift(1).rolling(w).std()
    return df


def encode_store_id(
    df: pd.DataFrame,
    column: str = "store_id"
) -> pd.DataFrame:
    """
    One-hot-encode la columna de tienda si existe.
    """
    if column in df.columns:
        df = pd.get_dummies(df, columns=[column], prefix=column)
    return df


def create_features(
    df: pd.DataFrame,
    freq: Optional[str] = None,
    lags: List[int]    = [1, 7, 14],
    windows: List[int] = [7, 14, 28],
) -> pd.DataFrame:
    """
    Pipeline completo de generación de features:
      1) Asegura índice datetime y opcionalmente resamplea
      2) Extrae features de fecha
      3) Agrega lags y rolling stats
      4) Codifica store_id
      5) Elimina filas con NaNs generados
    """
    df_proc = df.copy()
    
    # 1) Resample si se indicó frecuencia
    if freq is not None:
        df_proc = df_proc.resample(freq).sum()
    
    # 2) Index como datetime
    df_proc.index = pd.to_datetime(df_proc.index)
    
    # 3) Date features
    df_proc = add_date_features(df_proc)
    
    # 4) Lag features
    df_proc = add_lag_features(df_proc, lags)
    
    # 5) Rolling features
    df_proc = add_rolling_features(df_proc, windows)
    
    # 6) Codificar tiendas
    df_proc = encode_store_id(df_proc)
    
    # 7) Eliminar filas incompletas (NaNs)
    df_proc = df_proc.dropna()

    return df_proc
