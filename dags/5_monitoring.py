from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, classification_report
import smtplib

# Ścieżki do plików
MODEL_PATH = "/opt/airflow/models/xgboost_model.pkl"
DATA_PATH = "/opt/airflow/data/test_data.csv"

# Próg
THRESHOLD = 0.8 

# Funkcje
def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

def validate_model():
    # Wczytaj model i dane
    model = load_model()
    data = pd.read_csv(DATA_PATH)
    X = data.drop("Delay", axis=1)
    y = data["Delay"]

    # Przewidywania i metryki
    y_pred = model.predict(X)
    acc = accuracy_score(y, y_pred)
    report = classification_report(y, y_pred)

    print(f"Accuracy: {acc}")
    print("Report:")
    print(report)

    # Sprawdź próg jakości
    if acc < THRESHOLD:
        send_alert(acc, report)

def send_alert(acc, report):
    # Wysyłanie maila z ostrzeżeniem
    sender = "airflowAdmin@airflow.com"
    recipient = "s24431@pjwstk.edu.pl"
    subject = "Model Alert: Quality Threshold Breached"
    body = f"""
    Model Performance Alert:
    - Model: Your Model Name
    - Accuracy: {acc}
    - Threshold: {THRESHOLD}
    - Report:
    {report}
    """
    try:
        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.starttls()
            server.login(sender, "password")
            server.sendmail(sender, recipient, f"Subject: {subject}\n\n{body}")
    except Exception as e:
        print(f"Failed to send alert: {e}")

# Definicja DAG-a
with DAG(
    "validate_model_on_new_data",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    validate_task = PythonOperator(
        task_id="validate_model",
        python_callable=validate_model,
    )

validate_task
