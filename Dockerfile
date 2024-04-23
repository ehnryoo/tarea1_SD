FROM python:3.9-slim

# Instalamos las dependencias del sistema operativo
RUN apt-get update && \
    apt-get install -y redis-server && \
    rm -rf /var/lib/apt/lists/*

# Definimos el directorio de trabajo
WORKDIR /app

# Copiamos el archivo requirements.txt y instalamos las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código fuente
COPY . .

# Comando para ejecutar el servidor
CMD ["python", "cache_server.py"]
