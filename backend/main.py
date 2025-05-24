#!/usr/bin/env python3
# backend/main.py

import sys
from pathlib import Path

# 1) Inyecta backend/ en el PYTHONPATH para que “src” sea importable
BASE_DIR = Path(__file__).resolve().parent        # …/IAproyecto/backend
sys.path.insert(0, str(BASE_DIR))

# 2) Imports
from fastapi                 import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas                as pd
import joblib
import torch

# ahora las importaciones en tu código pueden usar src.* tal como en tus módulos existentes
from src.config               import FREQ
from src.models.LSTM_model    import LSTMModel
from src.models.prophet_model import _add_date_regressors

# 3) Crea la app y habilita CORS
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # en prod restringe a tu front-end
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4) Define rutas a tus artefactos
ARTIFACTS    = BASE_DIR / "models"
SCALER_PATH  = ARTIFACTS / "lstm_scaler.pkl"
LSTM_STATE   = ARTIFACTS / "lstm_quantile.pth"
PROPHET_PATH = ARTIFACTS / "prophet_model.joblib"
XGB_PATH     = ARTIFACTS / "xgb_residual_adv_fixed.joblib"

# 5) Carga el scaler y el modelo LSTM
lstm_scaler = joblib.load(SCALER_PATH)
lstm_model  = LSTMModel(
    input_size  = lstm_scaler.n_features_in_,
    hidden_size = 128,    # ajusta a tus hiperparámetros reales
    num_layers  = 2,
    dropout     = 0.2,
)
state_dict = torch.load(LSTM_STATE, map_location="cpu")
lstm_model.load_state_dict(state_dict)
lstm_model.eval()

# 6) Carga Prophet y XGBoost
prophet_model = joblib.load(PROPHET_PATH)
xgb_model     = joblib.load(XGB_PATH)

# 7) Endpoint para recibir CSV y devolver SOLO LSTM y ENSEMBLE
@app.post("/predict-csv")
async def predict_csv(file: UploadFile = File(...)):
    """
    - Espera un multipart/form-data con un CSV que tenga columnas:
        'fecha'         (YYYY-MM-DD)
        'ventas_previas'
        'otras_vars'
    - Devuelve JSON con las predicciones de:
        • lstm
        • ensemble (lstm + prophet + xgb_residual)
    """
    df = pd.read_csv(file.file)
    results = []

    for _, row in df.iterrows():
        fecha          = row["fecha"]
        ventas_previas = row["ventas_previas"]
        otras_vars     = row["otras_vars"]

        # — LSTM —
        arr    = lstm_scaler.transform([[ventas_previas, otras_vars]])
        tensor = torch.tensor(arr, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            p_lstm = lstm_model(tensor).item()

        # — Prophet + XGB residual (para el ensemble) —
        tmp    = pd.DataFrame({"ds": [fecha]})
        tmp    = _add_date_regressors(tmp)
        p_prop = prophet_model.predict(tmp)["yhat"].iloc[0]
        p_xgb  = xgb_model.predict(pd.DataFrame({"prophet": [p_prop]}))[0]

        # — Ensamble final —
        p_ens = p_lstm + p_prop + p_xgb

        results.append({
            "fecha":    fecha,
            "lstm":     p_lstm,
            "ensemble": p_ens
        })

    return {"predictions": results}
