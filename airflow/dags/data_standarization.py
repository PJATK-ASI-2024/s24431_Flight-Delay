from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import json
from sklearn.preprocessing import LabelEncoder

# Configuration
JSON_KEYFILE_PATH = '/opt/airflow/dags/flightdelay.json'
SHEETS = {
    'Zbior_Modelowy': 'Dane_Modelowe_Przetworzone',
    'Zbior_Douczeniowy': 'Dane_Douczeniowe_Przetworzone'
}
LABEL_MAPPINGS_FILE = '/opt/airflow/dags/label_mappings.json'


def connect_to_google_sheets(sheet_name, json_keyfile_path):
    """Łączy się z Google Sheets i zwraca arkusz."""
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    return sheet


def fetch_and_clean_data(sheet_name, **kwargs):
    """Pobiera dane z Google Sheets i usuwa duplikaty oraz brakujące wartości."""
    sheet = connect_to_google_sheets(sheet_name, JSON_KEYFILE_PATH)
    data = pd.DataFrame(sheet.get_all_records())

    # Usunięcie duplikatów
    data.drop_duplicates(inplace=True)

    # Sprawdzenie brakujących wartości i uzupełnienie ich "Unknown"
    if data.isnull().sum().any():
        data.fillna('Unknown', inplace=True)

    kwargs['ti'].xcom_push(key=f'cleaned_data_{sheet_name}', value=data.to_json())


def standardize_data(sheet_name, **kwargs):
    """Standaryzuje dane: koduje zmienne kategoryczne i zapisuje mapowanie."""
    cleaned_data_json = kwargs['ti'].xcom_pull(key=f'cleaned_data_{sheet_name}')
    data = pd.read_json(cleaned_data_json)

    # Kodowanie zmiennych kategorycznych
    label_mappings = {}
    for column in data.select_dtypes(include=['object']).columns:
        encoder = LabelEncoder()
        data[column] = encoder.fit_transform(data[column])
        label_mappings[column] = {str(k): int(v) for k, v in zip(encoder.classes_, encoder.transform(encoder.classes_))}

    # Zapis mapowania etykiet do pliku
    label_mappings = {key: {k: int(v) for k, v in value.items()} for key, value in label_mappings.items()}
    with open(LABEL_MAPPINGS_FILE, 'w') as f:
        json.dump(label_mappings, f, indent=4)

    kwargs['ti'].xcom_push(key=f'standardized_data_{sheet_name}', value=data.to_json())


def save_to_google_sheets(source_sheet_name, target_sheet_name, **kwargs):
    """Zapisuje przetworzone dane do nowego arkusza Google Sheets."""
    standardized_data_json = kwargs['ti'].xcom_pull(key=f'standardized_data_{source_sheet_name}')
    data = pd.read_json(standardized_data_json)

    sheet = connect_to_google_sheets(target_sheet_name, JSON_KEYFILE_PATH)
    sheet.clear()
    sheet.update([data.columns.values.tolist()] + data.values.tolist())


# Definicja DAG-a
with DAG(
    'data_processing_v2_dag',
    default_args={'owner': 'airflow', 'retries': 1},
    description='DAG do czyszczenia i standaryzacji danych z Google Sheets',
    schedule_interval='@daily',
    start_date=datetime(2023, 11, 1),
    catchup=False,
) as dag:

    tasks = []
    for source_sheet, processed_sheet in SHEETS.items():
        fetch_task = PythonOperator(
            task_id=f'fetch_and_clean_{source_sheet}',
            python_callable=fetch_and_clean_data,
            op_kwargs={'sheet_name': source_sheet}
        )

        standardize_task = PythonOperator(
            task_id=f'standardize_{source_sheet}',
            python_callable=standardize_data,
            op_kwargs={'sheet_name': source_sheet}
        )

        save_task = PythonOperator(
            task_id=f'save_to_{processed_sheet}',
            python_callable=save_to_google_sheets,
            op_kwargs={
                'source_sheet_name': source_sheet,
                'target_sheet_name': processed_sheet
            }
        )

        fetch_task >> standardize_task >> save_task
        tasks.append(fetch_task)
