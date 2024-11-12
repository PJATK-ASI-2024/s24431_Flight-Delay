import pandas as pd
from pycaret.classification import *
import pytest

# Wczytaj przygotowane dane
data = pd.read_csv("G:\\Asi\\s24431_FlightDelay\\data\prepared_data.csv")

# Inicjalizacja środowiska PyCaret
# Ustawienie 'Delay' jako zmiennej docelowej i automatyczne wstępne przetwarzanie danych
exp_clf = setup(data=data, target='Delay', session_id=42, html=False)

# Porównanie modeli - automatyczny wybór najlepszych modeli
best_model = compare_models(n_select=3)

# Wyświetlenie najlepszych modeli
print("\nNajlepsze modele:")
for model in best_model:
    print(model)

# Wybranie najlepszego modelu do dalszych analiz i tuningu
final_best_model = best_model[0]  # Najlepszy model z listy
print("\nNajlepszy model:")
print(final_best_model)

# Tunowanie najlepszego modelu
tuned_model = tune_model(final_best_model)
print("\nModel po tuningu:")
print(tuned_model)

# Ocena wydajności na zbiorze testowym
evaluate_model(tuned_model)

