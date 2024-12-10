from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

# Ładowanie modelu
with open("xgboost_model.pkl", "rb") as f:
    model = pickle.load(f)

# Inicjalizacja aplikacji FastAPI
app = FastAPI()


# Klasa reprezentująca dane wejściowe
class PredictRequest(BaseModel):
    Airline: int
    AirportFrom: int
    AirportTo: int
    DayOfWeek: int
    Time: float
    Lenght: float


@app.post("/predict")
def predict(request: PredictRequest):
    # Pobieranie danych wejściowych
    features = np.array(
        [[request.Airline, request.AirportFrom, request.AirportTo, request.DayOfWeek, request.Time, request.Lenght]])

    # Predykcja za pomocą modelu
    prediction = model.predict(features)

    # Konwersja wyniku na natywny typ Pythona
    prediction_value = int(prediction[0])

    # Zwracanie wyniku w formacie JSON
    return {"prediction": prediction_value}
