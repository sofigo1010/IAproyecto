import pandas as pd
from typing import IO, Union
from src.config import DATA_PATH

# Ahora solo validamos que existan estas columnas
REQUIRED_COLUMNS = ["Order Date", "Sales"]

def load_sales_data(source: Union[str, IO] = None) -> pd.DataFrame:
    """
    Lee el CSV (Superstore), renombra columnas a date/sales,
    agrupa ventas diarias y, si existe Profit, también agrupa profit.
    """
    path = source or DATA_PATH
    df = pd.read_csv(path)
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas en el CSV: {missing}")

    # Renombrar las que sí existen
    df = df.rename(columns={
        "Order Date": "date",
        "Sales": "sales",
        **({"Profit": "profit"} if "Profit" in df.columns else {})
    })

    # Fecha → datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Drop solo date y sales (profit si no existe no se menciona)
    df = df.dropna(subset=["date", "sales"])

    # Si existe profit, dropna ahí también
    if "profit" in df.columns:
        df = df.dropna(subset=["profit"])

    # Agrupar por día
    agg_dict = {"sales": "sum"}
    if "profit" in df.columns:
        agg_dict["profit"] = "sum"
    df_daily = df.groupby("date", as_index=False).agg(agg_dict)
    return df_daily

def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    return df

def load_and_prepare_data(source: Union[str, IO] = None) -> pd.DataFrame:
    df = load_sales_data(source)
    return clean_sales_data(df)
