# src/data/ingestion.py

import pandas as pd
from typing import List, Union, IO
from src.config import DATA_PATH

# Columnas mínimas que debe tener tu CSV
REQUIRED_COLUMNS = ["date", "sales", "store_id"]

def load_sales_data(
    source: Union[str, IO] = None
) -> pd.DataFrame:
    """
    Lee un CSV de ventas desde:
      - un path (str), o
      - un file-like (IO), p.ej. UploadFile.file de FastAPI.

    Si source es None, usa DATA_PATH de config.
    """
    csv_source = source if source is not None else DATA_PATH
    try:
        df = pd.read_csv(csv_source)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo en {csv_source}")
    except Exception as e:
        raise RuntimeError(f"Error al leer CSV: {e}")

def validate_sales_data(df: pd.DataFrame, required_cols: List[str] = REQUIRED_COLUMNS) -> None:
    """
    Verifica que el DataFrame contenga las columnas esperadas.
    Lanza ValueError si falta alguna.
    """
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {missing}")

def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Manejo básico de datos faltantes y transformación de tipos:
      - Convierte 'date' a datetime
      - Elimina filas sin fecha o sin ventas
    """
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "sales"])
    return df

def load_and_prepare_data(
    source: Union[str, IO] = None
) -> pd.DataFrame:
    """
    Pipeline completo: cargar (path o file-like), validar y limpiar datos.
    """
    df = load_sales_data(source)
    validate_sales_data(df)
    df = clean_sales_data(df)
    return df

if __name__ == "__main__":
    # Prueba rápida desde disco
    df = load_and_prepare_data()
    print(df.head())
    print(f"Total registros: {len(df)}")
