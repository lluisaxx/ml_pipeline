"""
Pruebas básicas del dataset SDSS — requeridas por Jenkins
Ejecutar: python -m pytest tests/ -v
"""
import pandas as pd
import pytest
import os

DATA_PATH = os.environ.get("DATA_PATH", "sdss_sample.csv")
REQUIRED_COLS = ["u", "g", "r", "i", "z", "redshift", "class"]


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(DATA_PATH)


def test_archivo_existe():
    assert os.path.exists(DATA_PATH), f"No se encontró el archivo: {DATA_PATH}"


def test_columnas_requeridas(df):
    for col in REQUIRED_COLS:
        assert col in df.columns, f"Columna faltante: {col}"


def test_sin_nulos(df):
    nulls = df[REQUIRED_COLS].isnull().sum().sum()
    assert nulls == 0, f"Se encontraron {nulls} valores nulos"


def test_clases_validas(df):
    valid = {"Galaxy", "QSO", "Star"}
    found = set(df["class"].unique())
    assert found.issubset(valid), f"Clases inesperadas: {found - valid}"


def test_redshift_positivo(df):
    neg = (df["redshift"] < 0).sum()
    assert neg == 0, f"{neg} valores de redshift son negativos"


def test_magnitudes_rango(df):
    for col in ["u", "g", "r", "i", "z"]:
        assert df[col].between(0, 35).all(), f"Valores fuera de rango en columna {col}"


def test_minimo_filas(df):
    assert len(df) >= 100, f"Dataset muy pequeño: {len(df)} filas"
