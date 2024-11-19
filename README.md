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

# Aktualizacje
## Projekt - 2 - prototypowanie
Dodano folder Notebooks wraz z podfolderami. W podfolderach znajdują się pliki z 2 zadania projektowego.  

Struktura plików zadania 2:  
Notebooks -> Task2 -> EDA i Pycaret_Best_Model  

W src/s24431.py stworzono skrypt będący implementacją najlepszego modelu.  
Podczas pracy stworzono pliki z raportem sweetviz, prepared_data.csv, label_mappings.json - plik z danymi klucz - wartość danych przed przekształceniem,
oraz skrypty EDA.py i Pycaret.py. Pliki znajdują się w Notebooks/EDA oraz Notebooks/Pycaret_Best_Model, dane po przygotowaniu zostały umieszczone w folderze data.    
Dodano osobny plik z dokumentacją, zakutalizowano README.md.

## Projekt – 3 – Airflow  
Dodano folder airflow wraz z nim podfolder dags z dagami, dodano plik label_mappings.json z mapowaniem zmiennych. Stworzono docker-compose.yaml.  
Zaktualizowano Dokumentacje i readme.md

[Link-dataset]: https://www.kaggle.com/datasets/jimschacko/airlines-dataset-to-predict-a-delay
