"""
Pipeline principal de Machine Learning — Dataset SDSS
Ejecutar: python main.py [--data ruta/al/csv]
"""
import argparse
import json
import os
import sys

from src.preprocessing import (
    load_data,
    get_classification_data,
    get_regression_data,
    get_clustering_data,
)
from src.classification import train_knn, evaluate_classification
from src.regression import train_linear_regression, evaluate_regression
from src.clustering import train_kmeans, evaluate_clustering

OUTPUT_DIR = "outputs"


def main(data_path: str = "sdss_sample.csv"):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=" * 55)
    print("  PIPELINE ML — SDSS Astronómico")
    print("=" * 55)

    # ── Carga de datos ──────────────────────────────────────
    df = load_data(data_path)

    # ── 1. Clasificación ────────────────────────────────────
    print("\n[1/3] CLASIFICACIÓN (KNN k=5)")
    X_train_c, X_test_c, y_train_c, y_test_c, le, _ = get_classification_data(df)
    knn = train_knn(X_train_c, y_train_c, k=5)
    acc, cm = evaluate_classification(knn, X_test_c, y_test_c, le, OUTPUT_DIR)

    # ── 2. Regresión ────────────────────────────────────────
    print("\n[2/3] REGRESIÓN LINEAL (redshift)")
    X_train_r, X_test_r, y_train_r, y_test_r, _ = get_regression_data(df)
    lr = train_linear_regression(X_train_r, y_train_r)
    mse, r2 = evaluate_regression(lr, X_test_r, y_test_r, OUTPUT_DIR)

    # ── 3. Clustering ───────────────────────────────────────
    print("\n[3/3] CLUSTERING (KMeans k=3)")
    X_scaled, true_labels = get_clustering_data(df)
    kmeans = train_kmeans(X_scaled, n_clusters=3)
    dist = evaluate_clustering(kmeans, X_scaled, true_labels, OUTPUT_DIR)

    # ── Resumen general ─────────────────────────────────────
    summary = {
        "clasificacion": {"accuracy": round(acc, 4)},
        "regresion": {"MSE": round(mse, 6), "R2": round(r2, 6)},
        "clustering": {"inertia": round(float(kmeans.inertia_), 4), "distribucion": dist},
    }
    with open(f"{OUTPUT_DIR}/summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 55)
    print("  RESUMEN FINAL")
    print("=" * 55)
    print(f"  Clasificación  — Accuracy : {acc:.4f}")
    print(f"  Regresión      — MSE      : {mse:.4f}  |  R²: {r2:.4f}")
    print(f"  Clustering     — Inercia  : {kmeans.inertia_:.2f}")
    print(f"\n  Resultados guardados en: {OUTPUT_DIR}/")
    print("=" * 55)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline ML SDSS")
    parser.add_argument(
        "--data",
        default="sdss_sample.csv",
        help="Ruta al archivo CSV del dataset",
    )
    args = parser.parse_args()
    main(args.data)
