# Pipeline ML — Dataset SDSS Astronómico
**Universidad de San Buenaventura · Inteligencia Computacional**

Pipeline de Machine Learning reproducible que implementa clasificación, regresión y clustering sobre datos del Sloan Digital Sky Survey (SDSS).

---

## Estructura del proyecto

```
ml_pipeline/
├── main.py                  # Script principal del pipeline
├── requirements.txt         # Dependencias Python
├── Dockerfile               # Imagen Docker reproducible
├── Jenkinsfile              # Pipeline CI/CD automatizado
├── sdss_sample.csv          # Dataset astronómico
├── src/
│   ├── preprocessing.py     # Carga y preparación de datos
│   ├── classification.py    # KNN (k=5)
│   ├── regression.py        # Regresión lineal (redshift)
│   └── clustering.py        # KMeans (3 clusters)
├── tests/
│   └── test_dataset.py      # Pruebas básicas del dataset
└── outputs/                 # Métricas y gráficas generadas
```

---

## Modelos implementados

| Tarea | Modelo | Variables entrada | Variable objetivo |
|---|---|---|---|
| Clasificación | KNN (k=5) | u, g, r, i, z, redshift | class |
| Regresión | Regresión Lineal | u, g, r, i, z | redshift |
| Clustering | KMeans (k=3) | u, g, r, i, z | — |

---

## Ejecución local

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar el pipeline
python main.py --data sdss_sample.csv

# 3. Correr pruebas
pytest tests/ -v
```

Los resultados se guardan automáticamente en `outputs/`.

---

## Ejecución con Docker

```bash
# Construir la imagen
docker build -t sdss-ml-pipeline .

# Ejecutar el pipeline (los outputs quedan en la carpeta local)
docker run --rm -v $(pwd)/outputs:/app/outputs sdss-ml-pipeline
```

---

## Archivos generados en outputs/

| Archivo | Descripción |
|---|---|
| `classification_metrics.json` | Accuracy y matriz de confusión |
| `confusion_matrix.png` | Heatmap de la matriz de confusión |
| `regression_metrics.json` | MSE y coeficiente R² |
| `regression_plot.png` | Gráfica predicho vs real |
| `clustering_metrics.json` | Inercia y distribución de clusters |
| `clustering_plot.png` | Comparación clusters vs clases reales (PCA) |
| `summary.json` | Resumen consolidado de todas las métricas |
| `pipeline.log` | Log completo de ejecución |

---

## Pipeline Jenkins

El `Jenkinsfile` define estas etapas automáticas:

1. **Checkout** — Clona el repositorio
2. **Instalar dependencias** — Crea virtualenv e instala paquetes
3. **Pruebas del dataset** — Valida el CSV con pytest (JUnit XML)
4. **Ejecutar pipeline ML** — Corre `main.py` y guarda log
5. **Build Docker** — Construye la imagen
6. **Run en Docker** — Ejecuta el pipeline dentro del contenedor
7. **Almacenar artefactos** — Archiva métricas, gráficas y logs

---

## Interpretación de métricas

- **Accuracy**: proporción de objetos clasificados correctamente (Galaxy / QSO / Star).
- **Matriz de confusión**: muestra errores por clase; la diagonal es lo que el modelo acertó.
- **MSE**: error cuadrático medio del redshift predicho; cuanto más bajo, mejor.
- **R²**: qué tan bien explica el modelo la varianza del redshift (1.0 = perfecto).
- **Inercia (KMeans)**: suma de distancias al centroide; indica cohesión de los clusters.
