#!/usr/bin/env python3
# src/evaluate.py

import os
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from joblib import load as joblib_load

from src.config import FREQ, HORIZON_DAYS
from src.data.ingestion import load_and_prepare_data
from src.data.preprocessing import preprocess_sales_data
from src.models.prophet_model import load_model, predict_prophet, _add_date_regressors
from src.models.ensemble import _make_features

def smape(y_true, y_pred):
    denom = np.abs(y_true) + np.abs(y_pred)
    return 100 * np.mean(2 * np.abs(y_true - y_pred) / denom)

def main():
    # 1) Carga y preprocesado
    df_raw = load_and_prepare_data()
    df_ts  = preprocess_sales_data(df_raw, freq=FREQ)

    # 2) Modelos
    prophet   = load_model()
    xgb_model = joblib_load(os.path.join("models", "xgb_residual_adv.joblib"))

    # 3) Forecast in-sample de Prophet para yhat
    fc_hist   = predict_prophet(prophet, periods=0, freq=FREQ).set_index("ds")["yhat"]

    # 4) Índice de test: últimos HORIZON_DAYS de df_ts
    idx    = df_ts.index[-HORIZON_DAYS:]
    y_true = df_ts["sales"].loc[idx].values

    # 5) Predicción Prophet en-sample
    y_p = fc_hist.loc[idx].values

    # 6) Generar “future_dataframe” con regresores para todo el histórico
    future = prophet.make_future_dataframe(periods=0, freq=FREQ)
    future = _add_date_regressors(future)

    # 7) Predecir para obtener trend/week/month + yhat
    fc_full = prophet.predict(future).set_index("ds")

    # 8) Crear features del residual usando el mismo pipeline de ensemble
    feats_full = _make_features(fc_full)

    # 9) Extraer solo el periodo de test
    feats_test = feats_full.loc[idx]
    print("[DEBUG eval] Features residual shape:", feats_test.shape)
    print("[DEBUG eval] Primeras filas residual-features:\n", feats_test.head())

    # 10) Predecir residual y ensamblar ensemble
    resid_pred = xgb_model.predict(feats_test.drop(columns=["yhat"]))
    y_e        = y_p + resid_pred

    # 11) Métricas comparativas
    def metrics(y_pred, label):
        mae  = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mape = np.mean(np.abs((y_true - y_pred) / y_true.clip(1e-3))) * 100
        smp  = smape(y_true, y_pred)
        r2   = r2_score(y_true, y_pred)
        print(f"\n--- Métricas {label} ---")
        print(f"MAE:   {mae:.2f}")
        print(f"RMSE:  {rmse:.2f}")
        print(f"MAPE:  {mape:.2f}%")
        print(f"sMAPE: {smp:.2f}%")
        print(f"R²:    {r2:.3f}")

    metrics(y_p, "Prophet (in-sample)")
    metrics(y_e, "Ensemble (residual)")

    # 12) Diagnóstico residuals
    residuals = y_true - y_e
    print("\n[DEBUG eval] Residuals ensemble:")
    print(" media:", residuals.mean())
    print(" mediana:", np.median(residuals))
    print(" std:", residuals.std())
    print(" autocorr lag1:", pd.Series(residuals).autocorr())

    # 13) Error por ciclo (dow, month)
    df_err = pd.DataFrame({
        "err": np.abs(residuals) / y_true.clip(1e-3),
        "dow": idx.dayofweek,
        "month": idx.month
    })
    print("\n[DEBUG eval] MAPE por día de semana:\n", df_err.groupby("dow")["err"].mean())
    print("\n[DEBUG eval] MAPE por mes:\n", df_err.groupby("month")["err"].mean())

    # 14) Guardar métricas comparativas
    os.makedirs("models", exist_ok=True)
    pd.DataFrame({
        "metric": ["MAE","RMSE","MAPE","sMAPE","R2"],
        "Prophet": [
            mean_absolute_error(y_true,y_p),
            np.sqrt(mean_squared_error(y_true,y_p)),
            np.mean(np.abs((y_true-y_p)/y_true.clip(1e-3)))*100,
            smape(y_true,y_p),
            r2_score(y_true,y_p),
        ],
        "Ensemble": [
            mean_absolute_error(y_true,y_e),
            np.sqrt(mean_squared_error(y_true,y_e)),
            np.mean(np.abs((y_true-y_e)/y_true.clip(1e-3)))*100,
            smape(y_true,y_e),
            r2_score(y_true,y_e),
        ]
    }).to_csv("models/metrics_comparativo.csv", index=False)
    print("\n✅ Métricas comparativas guardadas en models/metrics_comparativo.csv")


if __name__ == "__main__":
    main()
