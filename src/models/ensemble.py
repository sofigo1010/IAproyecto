# src/models/ensemble.py

import pandas as pd
import numpy as np
from pathlib import Path
from joblib import dump, load
from xgboost import XGBRegressor

from src.models.prophet_model import load_model, _add_date_regressors
from src.config import FREQ, HORIZON_DAYS

MODEL_DIR = Path("models")
ENSEMBLE_PATH = MODEL_DIR / "xgb_residual_adv.joblib"
MODEL_DIR.mkdir(exist_ok=True)

LAGS    = [1, 7, 14]
WINDOWS = [7, 14, 28]


def _cyclic_encode(df, col, period):
    radians = 2 * np.pi * df[col] / period
    df[f"{col}_sin"] = np.sin(radians)
    df[f"{col}_cos"] = np.cos(radians)


def _make_features(df_fc: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(index=df_fc.index)
    # Componentes Prophet
    df["yhat"]     = df_fc["yhat"]
    df["trend"]    = df_fc["trend"]
    df["weekly"]   = df_fc["weekly"]
    df["monthly"]  = df_fc["monthly"]
    # Lags
    for lag in LAGS:
        df[f"lag_{lag}"] = df["yhat"].shift(lag)
    # Rolling
    for w in WINDOWS:
        df[f"roll_mean_{w}"] = df["yhat"].shift(1).rolling(w, min_periods=1).mean()
        df[f"roll_std_{w}"]  = df["yhat"].shift(1).rolling(w, min_periods=1).std()
    # Fecha
    df["dow"]   = df.index.dayofweek
    df["month"] = df.index.month
    # Cíclicas
    _cyclic_encode(df, "dow",   7)
    _cyclic_encode(df, "month", 12)
    # One-hot
    df = pd.get_dummies(df, columns=["dow","month"], prefix=["dow","mon"], drop_first=True)

    # Imputar en vez de eliminar
    df.fillna(method="bfill", inplace=True)
    df.fillna(method="ffill", inplace=True)
    return df


def train_ensemble(df_ts: pd.DataFrame) -> None:
    model = load_model()

    # Future frame + regresores de calendario
    future = model.make_future_dataframe(periods=HORIZON_DAYS, freq=FREQ)
    future = _add_date_regressors(future)

    # Forecast completo
    fc_all = model.predict(future).set_index("ds")

    # Crear features
    feats    = _make_features(fc_all)
    n_hist   = len(df_ts)
    feats_hist = feats.iloc[:n_hist]

    # Residual histórico
    resid = df_ts["sales"].values - feats_hist["yhat"].values

    # Entrenar XGBoost
    X_train = feats_hist.drop(columns=["yhat"])
    y_train = resid
    xgb = XGBRegressor(
        objective="reg:squarederror",
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
    )
    xgb.fit(X_train, y_train)
    dump(xgb, ENSEMBLE_PATH)


def predict_ensemble(df_ts: pd.DataFrame) -> pd.DataFrame:
    model = load_model()
    xgb   = load(ENSEMBLE_PATH)

    future = model.make_future_dataframe(periods=HORIZON_DAYS, freq=FREQ)
    future = _add_date_regressors(future)
    fc_all = model.predict(future).set_index("ds")

    feats    = _make_features(fc_all)
    n_hist   = len(df_ts)
    feats_fut = feats.iloc[n_hist:]

    # Residual predicho y forecast final
    resid_pred = xgb.predict(feats_fut.drop(columns=["yhat"]))
    yhat_base  = feats_fut["yhat"].values
    yhat_final = yhat_base + resid_pred

    out = fc_all.iloc[n_hist:][["yhat_lower","yhat_upper"]].copy()
    out["yhat"] = yhat_final
    return out.reset_index().rename(columns={"ds": "date"})


def fit_and_forecast(df_ts: pd.DataFrame) -> pd.DataFrame:
    """
    Ejecuta entrenamiento y predicción del ensemble.
    """
    train_ensemble(df_ts)
    return predict_ensemble(df_ts)
