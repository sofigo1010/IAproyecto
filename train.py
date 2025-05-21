#!/usr/bin/env python3
"""
train.py – Script principal para entrenar y predecir con Prophet
"""

import os
from src.data.ingestion import load_and_prepare_data
from src.data.preprocessing import preprocess_sales_data
from src.models.prophet_model import train_prophet, predict_prophet

def main():
    # 1. Carga y limpieza inicial (desde DATA_PATH o frontend)
    df_raw = load_and_prepare_data()

    # 2. Preprocesamiento (resample semanal)
    df_ts = preprocess_sales_data(df_raw, freq='W')

    # 3. Entrenamiento del modelo Prophet
    print("Entrenando modelo Prophet...")
    model = train_prophet(df_ts)
    print("Modelo entrenado y guardado en models/prophet_model.joblib")

    # 4. Generar pronóstico de 12 semanas
    print("Generando pronóstico de 12 semanas...")
    forecast = predict_prophet(model=model, periods=12, freq='W')
    
    # 5. Guardar pronóstico en CSV
    os.makedirs("models", exist_ok=True)
    forecast_csv = "models/forecast.csv"
    forecast.to_csv(forecast_csv, index=False)
    print(f"Pronóstico guardado en {forecast_csv}")

    # 6. Mostrar últimas líneas del pronóstico
    print(forecast.tail())

if __name__ == "__main__":
    main()
