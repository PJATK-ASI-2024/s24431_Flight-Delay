# Przewidywanie opoźnień lotów
## Cel projektu
 Celem jest stworzenie modelu, który będzie przewidywać prawdopodobieństwo opóźnienia lotu na podstawie różnych cech, takich jak: linia lotnicza, lotnisko początkowe, lotnisko docelowe, godzina odlotu, dzień odlotu.
## Problem projektu
 Możliwość lepszego planowania lotów w celu poprawy satysfakcji klientów lotniska.
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


## Model  
Po przeanalizowaniu datasetu poprzez narzędzie Pycaret najlepszym modelem okazał się xgboost a co za tym idzie został on użyty.  

## Jak pobrać?
Aby pobrać trzeba uruchomić terminal i wpisać następującą komendę:  
git clone https://github.com/PJATK-ASI-2024/s24431_Flight-Delay.git

## Jak uruchomić?
Potrzebny będzie docker a następnie po uruchomieniu:  
Przejście do katalogu z pobranymi plikami.  
Uruchomienie następujej komendy:  
docker-compose up  


[Link-dataset]: https://www.kaggle.com/datasets/jimschacko/airlines-dataset-to-predict-a-delay
