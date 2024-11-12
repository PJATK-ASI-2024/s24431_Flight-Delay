import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sweetviz as sv
import json
from sklearn.preprocessing import LabelEncoder

# Wczytanie danych
data = pd.read_csv("G:\\Asi\\s24431_FlightDelay\\data\\dataset.csv")

# Przegląd danych
print("Podstawowe informacje o danych:")
print(data.info())
print("\nPodstawowe statystyki opisowe:")
print(data.describe())

# Sprawdzenie rozkładów zmiennych numerycznych
num_columns = data.select_dtypes(include=['float64', 'int64']).columns
data[num_columns].hist(bins=20, figsize=(15, 10))
plt.suptitle("Histogramy zmiennych numerycznych")
plt.show()

# Sprawdzenie rozkładów zmiennych kategorycznych
cat_columns = data.select_dtypes(include=['object', 'category']).columns
for col in cat_columns:
    plt.figure(figsize=(10, 5))
    sns.countplot(data=data, x=col)
    plt.title(f'Rozkład zmiennej kategorycznej: {col}')
    plt.xticks(rotation=45)
    plt.show()

# Analiza brakujących wartości
missing_values = data.isnull().sum()
missing_values = missing_values[missing_values > 0]
print("\nBrakujące wartości w kolumnach:")
print(missing_values)

# Wizualizacja brakujących wartości
plt.figure(figsize=(10, 6))
sns.heatmap(data.isnull(), cbar=False, cmap='viridis')
plt.title("Wizualizacja brakujących wartości w danych")
plt.show()

# Wizualizacje - macierz korelacji
numerical_data = data.select_dtypes(include=['float64', 'int64'])
correlation_matrix = numerical_data.corr()

plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", square=True)
plt.title("Macierz korelacji zmiennych numerycznych")
plt.show()

# Analiza danych za pomocą Sweetviz
report = sv.analyze(data)
report.show_html('sweetviz_report.html')
print("Raport Sweetviz wygenerowany i zapisany jako 'sweetviz_report.html'")

# Przygotowanie danych do modelowania
# Przygotowanie miejsca na słowniki mapowań
label_mappings = {}

#Usunięcie kolumny 'id' i innych zbędnych
irrelevant_columns = ['id', 'Flight']
data = data.drop(columns=[col for col in irrelevant_columns if col in data.columns])

#Redukcja liczby unikalnych kategorii dla zmiennych o dużej liczbie wartości
def reduce_categories(df, column, threshold=100):
    counts = df[column].value_counts()
    other_categories = counts[counts < threshold].index
    df[column] = df[column].replace(other_categories, 'Other')

# Redukcja liczby kategorii w kolumnach
reduce_categories(data, 'Airline', threshold=100)
reduce_categories(data, 'AirportFrom', threshold=100)
reduce_categories(data, 'AirportTo', threshold=100)

#Kodowanie zmiennych kategorycznych i zapis mapowań
label_encodable_columns = ['Airline', 'AirportFrom', 'AirportTo', 'DayOfWeek']
for col in label_encodable_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    # Zapisz mapowanie etykiet do słownika, konwertując wartości na int
    label_mappings[col] = {str(k): int(v) for k, v in zip(le.classes_, le.transform(le.classes_))}

# Zapisz przetworzone dane
data.to_csv('prepared_data.csv', index=False)
print("Przygotowane dane zostały zapisane jako 'prepared_data.csv'")

# Zapisz mapowania do pliku JSON
with open('label_mappings.json', 'w') as f:
    json.dump(label_mappings, f, indent=4)
print("Mapowania etykiet zostały zapisane jako 'label_mappings.json'")
