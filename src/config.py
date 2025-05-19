# src/config.py

import os
from dotenv import load_dotenv

# Carga variables de .env
load_dotenv()

# — Rutas de datos ——————————————————————————————
DATA_PATH = os.getenv("DATA_PATH")

# — Parámetros de Prophet ————————————————————————
PROPHET_SEASONALITY_MODE = os.getenv("PROPHET_SEASONALITY_MODE", "additive")
PROPHET_DAILY_SEASONALITY = os.getenv("PROPHET_DAILY_SEASONALITY", "false").lower() == "true"
PROPHET_WEEKLY_SEASONALITY = os.getenv("PROPHET_WEEKLY_SEASONALITY", "true").lower() == "true"
PROPHET_YEARLY_SEASONALITY = os.getenv("PROPHET_YEARLY_SEASONALITY", "true").lower() == "true"

# — Parámetros de LSTM ——————————————————————————
LSTM_EPOCHS = int(os.getenv("LSTM_EPOCHS", 50))
LSTM_BATCH_SIZE = int(os.getenv("LSTM_BATCH_SIZE", 32))
LSTM_UNITS = int(os.getenv("LSTM_UNITS", 64))

def print_config():
    """Imprime en consola los valores cargados, útil para verificar."""
    from pprint import pprint
    pprint({
        "DATA_PATH": DATA_PATH,
        "PROPHET_SEASONALITY_MODE": PROPHET_SEASONALITY_MODE,
        "PROPHET_DAILY_SEASONALITY": PROPHET_DAILY_SEASONALITY,
        "PROPHET_WEEKLY_SEASONALITY": PROPHET_WEEKLY_SEASONALITY,
        "PROPHET_YEARLY_SEASONALITY": PROPHET_YEARLY_SEASONALITY,
        "LSTM_EPOCHS": LSTM_EPOCHS,
        "LSTM_BATCH_SIZE": LSTM_BATCH_SIZE,
        "LSTM_UNITS": LSTM_UNITS,
    })
