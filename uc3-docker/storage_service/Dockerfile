FROM python:3.9-slim

WORKDIR /app

COPY storage_service.py /app/

# Instalar Flask (y lo que necesites)
RUN pip install Flask

# Exponemos el puerto 5000 (donde corre Flask)
EXPOSE 5000

CMD ["python", "storage_service.py"]
