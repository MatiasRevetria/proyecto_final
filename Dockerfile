# Imagen base oficial de Python
FROM python:3.12-slim


# Seteo el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copio el archivo de requerimientos y lo instalo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copio todo el proyecto (excepto lo que se ignore en .dockerignore)
COPY . .

# Expongo el puerto en que Django corre por defecto
EXPOSE 8000

# Comando para correr el servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

