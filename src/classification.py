import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


def train_knn(X_train, y_train, k: int = 5) -> KNeighborsClassifier:
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train, y_train)
    print(f"[INFO] KNN entrenado con k={k}")
    return model


def evaluate_classification(model, X_test, y_test, label_encoder, output_dir: str):
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    class_names = label_encoder.classes_

    print(f"[CLASIFICACIÓN] Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred, target_names=class_names))

    # Guardar métricas en JSON
    metrics = {
        "accuracy": round(acc, 4),
        "confusion_matrix": cm.tolist(),
        "classes": list(class_names),
    }
    with open(f"{output_dir}/classification_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # Guardar matriz de confusión como imagen
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names,
        ax=ax,
    )
    ax.set_title(f"Matriz de Confusión — KNN (k=5)\nAccuracy: {acc:.4f}")
    ax.set_ylabel("Real")
    ax.set_xlabel("Predicho")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/confusion_matrix.png", dpi=150)
    plt.close()
    print(f"[INFO] Métricas y gráfica de clasificación guardadas en {output_dir}/")
    return acc, cm
