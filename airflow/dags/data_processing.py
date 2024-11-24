from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from sklearn.model_selection import train_test_split
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Konfiguracja Google Sheets
JSON_KEYFILE_PATH = '/opt/airflow/dags/flightdelay.json'
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Funkcja do autoryzacji Google Sheets
def authorize_google_sheets():
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEYFILE_PATH, SCOPES)
    client = gspread.authorize(creds)
    return client

# Funkcja: Pobranie danych
def fetch_data(**kwargs):
    file_path = '/opt/airflow/dags/dataset.csv'  # Ścieżka do pliku CSV
    data = pd.read_csv(file_path)
    kwargs['ti'].xcom_push(key='raw_data', value=data.to_json())

# Funkcja: Podział danych
def split_data(**kwargs):
    raw_data = pd.read_json(kwargs['ti'].xcom_pull(key='raw_data'))
    train, test = train_test_split(raw_data, test_size=0.3, random_state=42)
    kwargs['ti'].xcom_push(key='train_data', value=train.to_json())
    kwargs['ti'].xcom_push(key='test_data', value=test.to_json())

# Funkcja: Zapis do Google Sheets
def upload_to_google_sheets(sheet_name, data_json):
    client = authorize_google_sheets()
    try:
        # Otwórz arkusz i pobierz zakładkę
        sheet = client.open(sheet_name).sheet1
        data = pd.read_json(data_json)

        # Dodanie nazw kolumn jako pierwszy wiersz
        data_with_headers = [data.columns.tolist()] + data.values.tolist()

        # Czyszczenie istniejących danych
        sheet.clear()

        # Zapis danych do arkusza
        sheet.update('A1', data_with_headers)
        print(f"Dane zapisane do arkusza: {sheet_name}")
    except Exception as e:
        print(f"Błąd podczas zapisu do Google Sheets: {e}")
        raise

def save_data_to_gsheets(**kwargs):
    train_data = kwargs['ti'].xcom_pull(key='train_data')
    test_data = kwargs['ti'].xcom_pull(key='test_data')

    # Nazwy arkuszy
    model_sheet_name = "Zbior_Modelowy"
    training_sheet_name = "Zbior_Douczeniowy"

    # Zapis danych do arkuszy
    upload_to_google_sheets(sheet_name=model_sheet_name, data_json=train_data)
    upload_to_google_sheets(sheet_name=training_sheet_name, data_json=test_data)

# Definicja DAG-a
with DAG(
    'data_processing_dag',
    default_args={
        'owner': 'airflow',
        'retries': 1,
    },
    description='DAG pobierający dane, dzielący je i zapisujący do Google Sheets',
    schedule_interval='@daily',
    start_date=datetime(2023, 11, 1),
    catchup=False,
) as dag:

    fetch_task = PythonOperator(
        task_id='fetch_data',
        python_callable=fetch_data
    )

    split_task = PythonOperator(
        task_id='split_data',
        python_callable=split_data
    )

    save_task = PythonOperator(
        task_id='save_data_to_gsheets',
        python_callable=save_data_to_gsheets
    )

    fetch_task >> split_task >> save_task
