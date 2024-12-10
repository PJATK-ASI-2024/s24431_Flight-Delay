# Przewidywanie opoźnień lotów
## Cel projektu
 Celem jest stworzenie modelu, który będzie przewidywać prawdopodobieństwo opóźnienia lotu na podstawie różnych cech, takich jak: linia lotnicza, lotnisko początkowe, lotnisko docelowe, godzina odlotu, dzień odlotu.
## Problem projektu
 Możliwość lepszego planowania lotów.
## Źródło danych
- [Link-dataset] – około 539383 linii danych.
    
Kolumny:  
- Airline  
- Flight  
- Airport From  
- Airport To  
- DayOfWeek  
- Time  
## Cele projektu
 - Zbudowanie modelu będącego w dokładny sposób przewidywać możliwe opóźnienia lotów.  
 - Analiza i eksploracja danych.  
 - Trenowanie oraz walidowanie modelu.  
 - Dokształcanie modelu.  
 -  Publikacja oraz prezentacja.  

# Uruchomienie

Uruchomienie docker:  
docker pull bartoszkunc/flight_pred_app:latest  
docker run -p 5000:5000 bartoszkunc/flight_pred_app:latest   
w przeglądrace: http://localhost:5000/docs  

Postman:  
New -> http  
Zmiana pakietu na POST  
adres: http://127.0.0.1:5000/predict  
raw JSON ustawiony w zakładce body np.:  
{  
    "Airline": 2,  
    "AirportFrom": 8,  
    "AirportTo": 197,  
    "DayOfWeek":2,  
    "Time": 30,  
    "Lenght": 202  
}  
Output:  
{  
    "prediction": 0  
}  


[Link-dataset]: https://www.kaggle.com/datasets/jimschacko/airlines-dataset-to-predict-a-delay
