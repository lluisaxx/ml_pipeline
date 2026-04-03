# Imagen base liviana con Python 3.11
FROM python:3.11-slim

# Metadatos
LABEL maintainer="USB Inteligencia Computacional"
LABEL description="Pipeline ML reproducible — Dataset SDSS"

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar dependencias primero (aprovecha caché de Docker)
COPY requirements.txt .

# Instalar dependencias sin caché para mantener imagen pequeña
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Crear carpeta de salida
RUN mkdir -p outputs

# Variable de entorno para que matplotlib no necesite display
ENV MPLBACKEND=Agg

# Ejecutar el pipeline al iniciar el contenedor
CMD ["python", "main.py", "--data", "sdss_sample.csv"]
