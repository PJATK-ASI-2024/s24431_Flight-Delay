import pandas as pd
from pycaret.classification import *

# Funkcja wczytująca dane
def load_data(file_path):
    return pd.read_csv(file_path)

# Funkcja inicjalizująca środowisko PyCaret
def initialize_pycaret(data, target_column, session_id=42):
    exp_clf = setup(data=data, target=target_column, session_id=session_id, html=False)
    return exp_clf

# Funkcja porównująca modele
def compare_models_and_select(data, top_n=3):
    best_models = compare_models(n_select=top_n)
    print("\nNajlepsze modele:")
    for model in best_models:
        print(model)
    return best_models

# Funkcja wybierająca najlepszy model
def get_best_model(models):
    best_model = models[0]  # Najlepszy model
    print("\nNajlepszy model:")
    print(best_model)
    return best_model

# Funkcja tunująca model
def tune_selected_model(model):
    tuned_model = tune_model(model)
    print("\nModel po tuningu:")
    print(tuned_model)
    return tuned_model

# Funkcja oceniająca model
def evaluate_selected_model(model):
    evaluate_model(model)

# Główna funkcja
def main():
    # Ścieżka do danych
    file_path = "G:\\Asi\\s24431_FlightDelay\\data\\prepared_data.csv"

    # Wczytaj dane
    data = load_data(file_path)

    # Inicjalizacja PyCaret
    exp_clf = initialize_pycaret(data, target_column='Delay', session_id=42)

    # Porównanie modeli
    best_models = compare_models_and_select(data, top_n=3)

    # Wybranie najlepszego modelu
    final_best_model = get_best_model(best_models)

    # Tunowanie najlepszego modelu
    tuned_model = tune_selected_model(final_best_model)

    # Ocena modelu
    evaluate_selected_model(tuned_model)

# Uruchomienie głównej funkcji
if __name__ == "__main__":
    main()
