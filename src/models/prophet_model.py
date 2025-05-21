# src/models/prophet_model.py

import os
from pathlib import Path
from joblib import dump, load
from src.models.prophet_model import Prophet
import pandas as pd
from src.config import (
    PROPHET_SEASONALITY_MODE,
    PROPHET_DAILY_SEASONALITY,
    PROPHET_WEEKLY_SEASONALITY,
    PROPHET_YEARLY_SEASONALITY,
)

# Carpeta por defecto para guardar los modelos
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

def train_prophet(
    df: pd.DataFrame,
    model_path: str = MODEL_DIR / "prophet_model.joblib",
    **prophet_kwargs
) -> Prophet:
    """
    Entrena un modelo Prophet y lo guarda en disk.

    Parámetros:
    - df: DataFrame con índice datetime y columna 'sales'.
    - model_path: ruta donde se guardará el modelo.
    - prophet_kwargs: argumentos extra para Prophet().

    Retorna:
    - Instancia del modelo ajustado.
    """
    # Preparar datos para Prophet
    df_prophet = df.reset_index().rename(columns={"date": "ds", "sales": "y"})
    
    # Inicializar el modelo con parámetros de config + kwargs
    m = Prophet(
        seasonality_mode=PROPHET_SEASONALITY_MODE,
        daily_seasonality=PROPHET_DAILY_SEASONALITY,
        weekly_seasonality=PROPHET_WEEKLY_SEASONALITY,
        yearly_seasonality=PROPHET_YEARLY_SEASONALITY,
        **prophet_kwargs,
    )
    m.fit(df_prophet)
    
    # Guardar el modelo
    dump(m, model_path)
    return m

def predict_prophet(
    model: Prophet = None,
    periods: int = 52,
    freq: str = "W",
    model_path: str = MODEL_DIR / "prophet_model.joblib"
) -> pd.DataFrame:
    """
    Carga (si es necesario) y genera predicciones futuras.

    Parámetros:
    - model: instancia Prophet ya entrenada (opcional).
    - periods: número de pasos a predecir (e.g. 52 semanas).
    - freq: frecuencia (D, W, M, etc.).
    - model_path: ruta al .joblib con el modelo.

    Retorna:
    - DataFrame con columnas ['ds','yhat','yhat_lower','yhat_upper'].
    """
    # Si no se pasó el modelo, cargarlo de disk
    if model is None:
        model = load(model_path)
    
    # Generar periodos futuros
    future = model.make_future_dataframe(periods=periods, freq=freq)
    forecast = model.predict(future)
    
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]

def save_model(
    model: Prophet,
    model_path: str = MODEL_DIR / "prophet_model.joblib"
) -> None:
    """
    Guarda un modelo Prophet entrenado en la ruta especificada.
    """
    dump(model, model_path)

def load_model(
    model_path: str = MODEL_DIR / "prophet_model.joblib"
) -> Prophet:
    """
    Carga un modelo Prophet desde disco.
    """
    return load(model_path)
