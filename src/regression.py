import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def train_linear_regression(X_train, y_train) -> LinearRegression:
    model = LinearRegression()
    model.fit(X_train, y_train)
    print("[INFO] Regresión lineal entrenada")
    return model


def evaluate_regression(model, X_test, y_test, output_dir: str):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"[REGRESIÓN] MSE: {mse:.4f}  |  R²: {r2:.4f}")

    # Guardar métricas
    metrics = {"MSE": round(mse, 6), "R2": round(r2, 6)}
    with open(f"{output_dir}/regression_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # Gráfica predicho vs real
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(y_test, y_pred, alpha=0.4, s=15, color="steelblue", label="Predicciones")
    lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
    ax.plot(lims, lims, "r--", linewidth=1.5, label="Perfecta predicción")
    ax.set_xlabel("Redshift real")
    ax.set_ylabel("Redshift predicho")
    ax.set_title(f"Regresión Lineal — Redshift\nMSE: {mse:.4f}  R²: {r2:.4f}")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{output_dir}/regression_plot.png", dpi=150)
    plt.close()
    print(f"[INFO] Métricas y gráfica de regresión guardadas en {output_dir}/")
    return mse, r2
