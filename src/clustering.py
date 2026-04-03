import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


def train_kmeans(X_scaled, n_clusters: int = 3, random_state: int = 42) -> KMeans:
    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    model.fit(X_scaled)
    print(f"[INFO] KMeans entrenado con {n_clusters} clusters")
    return model


def evaluate_clustering(model, X_scaled, true_labels, output_dir: str):
    cluster_labels = model.labels_
    unique_clusters, counts = np.unique(cluster_labels, return_counts=True)
    dist = {int(k): int(v) for k, v in zip(unique_clusters, counts)}
    print(f"[CLUSTERING] Distribución de clusters: {dist}")

    # Guardar métricas básicas
    metrics = {
        "n_clusters": int(model.n_clusters),
        "inertia": round(float(model.inertia_), 4),
        "cluster_distribution": dist,
    }
    with open(f"{output_dir}/clustering_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # Reducción PCA a 2D para visualización
    pca = PCA(n_components=2, random_state=42)
    X_2d = pca.fit_transform(X_scaled)

    class_to_int = {c: i for i, c in enumerate(np.unique(true_labels))}
    true_int = np.array([class_to_int[c] for c in true_labels])

    cmap_clusters = plt.colormaps["Set1"].resampled(3)
    cmap_classes = plt.colormaps["tab10"].resampled(len(class_to_int))

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Clusters KMeans
    sc1 = axes[0].scatter(
        X_2d[:, 0], X_2d[:, 1],
        c=cluster_labels, cmap=cmap_clusters, s=10, alpha=0.6
    )
    axes[0].set_title("Clusters obtenidos (KMeans)")
    axes[0].set_xlabel("PC1")
    axes[0].set_ylabel("PC2")
    plt.colorbar(sc1, ax=axes[0], label="Cluster")

    # Clases reales
    sc2 = axes[1].scatter(
        X_2d[:, 0], X_2d[:, 1],
        c=true_int, cmap=cmap_classes, s=10, alpha=0.6
    )
    axes[1].set_title("Clases reales")
    axes[1].set_xlabel("PC1")
    axes[1].set_ylabel("PC2")
    legend_labels = list(class_to_int.keys())
    handles = [
        plt.Line2D([0], [0], marker="o", color="w",
                   markerfacecolor=cmap_classes(i), markersize=8)
        for i in range(len(legend_labels))
    ]
    axes[1].legend(handles, legend_labels, title="Clase")

    plt.suptitle("Clustering KMeans vs Clases Reales (PCA 2D)", fontsize=13)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/clustering_plot.png", dpi=150)
    plt.close()
    print(f"[INFO] Métricas y gráfica de clustering guardadas en {output_dir}/")
    return dist
