# Użyj oficjalnego obrazu Python jako bazowego
FROM python:3.9-slim

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki aplikacji do obrazu
COPY app /app

# Instaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Eksponuj port dla serwera FastAPI
EXPOSE 8000

#test
RUN python -c "import xgboost; print('xgboost imported successfully')"


# Uruchom aplikację
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
