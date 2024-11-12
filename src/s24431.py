import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error, f1_score, roc_auc_score, classification_report
from xgboost import XGBClassifier

# Wczytanie przygotowanych danych
data = pd.read_csv("G:\\Asi\\s24431_FlightDelay\\data\prepared_data.csv")
X = data.drop('Delay', axis=1)
y = data['Delay']

# Podział na zbiór treningowy i walidacyjny (70/30)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=42)

# Inicjalizacja modelu XGBoost z podstawowymi parametrami
model = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')

# Trening modelu na zbiorze treningowym
model.fit(X_train, y_train)

# Predykcja na zbiorze walidacyjnym
y_pred = model.predict(X_val)
# Prawdopodobieństwo dla klasy 1
y_pred_proba = model.predict_proba(X_val)[:, 1]

# Obliczenie podstawowych metryk jakości
accuracy = accuracy_score(y_val, y_pred)
f1 = f1_score(y_val, y_pred)
auc = roc_auc_score(y_val, y_pred_proba)
mae = mean_absolute_error(y_val, y_pred)

# Wyświetlenie wyników
print("Podstawowe metryki jakości modelu na zbiorze walidacyjnym:")
print(f"Dokładność (Accuracy): {accuracy:.4f}")
print(f"F1-Score: {f1:.4f}")
print(f"AUC: {auc:.4f}")
print(f"Średni błąd bezwzględny (MAE): {mae:.4f}")

# Dodatkowy raport klasyfikacji
print("\nRaport klasyfikacji:")
print(classification_report(y_val, y_pred))
