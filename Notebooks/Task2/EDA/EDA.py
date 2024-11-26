import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sweetviz as sv
import json
from sklearn.preprocessing import LabelEncoder


# Wczytywanie danych
def load_data(file_path):
    return pd.read_csv(file_path)


# Przegląd danych
def data_overview(data):
    print("Podstawowe informacje o danych:")
    print(data.info())
    print("\nPodstawowe statystyki opisowe:")
    print(data.describe())


# Wizualizacja histogramów zmiennych numerycznych
def plot_numerical_histograms(data):
    num_columns = data.select_dtypes(include=['float64', 'int64']).columns
    data[num_columns].hist(bins=20, figsize=(15, 10))
    plt.suptitle("Histogramy zmiennych numerycznych")
    plt.show()


# Wizualizacja rozkładów zmiennych kategorycznych
def plot_categorical_distributions(data):
    cat_columns = data.select_dtypes(include=['object', 'category']).columns
    for col in cat_columns:
        plt.figure(figsize=(10, 5))
        sns.countplot(data=data, x=col)
        plt.title(f'Rozkład zmiennej kategorycznej: {col}')
        plt.xticks(rotation=45)
        plt.show()


# Analiza brakujących wartości
def analyze_missing_values(data):
    missing_values = data.isnull().sum()
    missing_values = missing_values[missing_values > 0]
    print("\nBrakujące wartości w kolumnach:")
    print(missing_values)
    plt.figure(figsize=(10, 6))
    sns.heatmap(data.isnull(), cbar=False, cmap='viridis')
    plt.title("Wizualizacja brakujących wartości w danych")
    plt.show()


# Wizualizacja macierzy korelacji
def plot_correlation_matrix(data):
    numerical_data = data.select_dtypes(include=['float64', 'int64'])
    correlation_matrix = numerical_data.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", square=True)
    plt.title("Macierz korelacji zmiennych numerycznych")
    plt.show()


# Generowanie raportu Sweetviz
def generate_sweetviz_report(data, output_path):
    report = sv.analyze(data)
    report.show_html(output_path)
    print(f"Raport Sweetviz wygenerowany i zapisany jako '{output_path}'")


# Usuwanie zbędnych kolumn
def drop_irrelevant_columns(data, columns_to_drop):
    return data.drop(columns=[col for col in columns_to_drop if col in data.columns])


# Redukcja liczby kategorii
def reduce_categories(data, column, threshold=100):
    counts = data[column].value_counts()
    other_categories = counts[counts < threshold].index
    data[column] = data[column].replace(other_categories, 'Other')


# Kodowanie zmiennych kategorycznych
def encode_categorical_columns(data, columns):
    label_mappings = {}
    for col in columns:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        label_mappings[col] = {str(k): int(v) for k, v in zip(le.classes_, le.transform(le.classes_))}
    return data, label_mappings


# Zapis danych i mapowań
def save_data_and_mappings(data, data_file, mappings, mappings_file):
    data.to_csv(data_file, index=False)
    print(f"Przygotowane dane zostały zapisane jako '{data_file}'")
    with open(mappings_file, 'w') as f:
        json.dump(mappings, f, indent=4)
    print(f"Mapowania etykiet zostały zapisane jako '{mappings_file}'")


# Główna funkcja
def main():
    # Ścieżka do pliku z danymi
    file_path = "G:\\Asi\\s24431_FlightDelay\\data\\dataset.csv"

    # Wczytanie danych
    data = load_data(file_path)

    # Przegląd danych
    data_overview(data)

    # Wizualizacje
    plot_numerical_histograms(data)
    plot_categorical_distributions(data)

    # Analiza brakujących wartości
    analyze_missing_values(data)

    # Wizualizacja korelacji
    plot_correlation_matrix(data)

    # Analiza Sweetviz
    generate_sweetviz_report(data, 'sweetviz_report.html')

    # Przygotowanie danych
    irrelevant_columns = ['id', 'Flight']
    data = drop_irrelevant_columns(data, irrelevant_columns)
    reduce_categories(data, 'Airline', threshold=100)
    reduce_categories(data, 'AirportFrom', threshold=100)
    reduce_categories(data, 'AirportTo', threshold=100)

    label_encodable_columns = ['Airline', 'AirportFrom', 'AirportTo', 'DayOfWeek']
    data, label_mappings = encode_categorical_columns(data, label_encodable_columns)

    # Zapis danych i mapowań
    save_data_and_mappings(data, 'prepared_data.csv', label_mappings, 'label_mappings.json')


# Wywołanie głównej funkcji
if __name__ == "__main__":
    main()
