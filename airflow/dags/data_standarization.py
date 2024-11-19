from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import json
from sklearn.preprocessing import LabelEncoder

# Configuration
JSON_KEYFILE_PATH = '/opt/airflow/dags/flightdelay.json'
SHEET_NAME = 'Zbior_Modelowy'
PROCESSED_SHEET_NAME = 'Przetworzone_Dane'
LABEL_MAPPINGS_FILE = '/opt/airflow/dags/label_mappings.json'


def connect_to_google_sheets(sheet_name, json_keyfile_path):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    return sheet


def fetch_data_from_gsheets(**kwargs):
    sheet = connect_to_google_sheets(SHEET_NAME, JSON_KEYFILE_PATH)
    data = pd.DataFrame(sheet.get_all_records())
    kwargs['ti'].xcom_push(key='raw_data', value=data.to_json())


def clean_data(**kwargs):
    raw_data_json = kwargs['ti'].xcom_pull(key='raw_data')
    data = pd.read_json(raw_data_json)

    # Remove duplicates
    data.drop_duplicates(inplace=True)

    # Check for missing values
    missing_values = data.isnull().sum()
    if missing_values.any():
        data.fillna('Unknown', inplace=True)

    kwargs['ti'].xcom_push(key='cleaned_data', value=data.to_json())


def standardize_data(**kwargs):
    cleaned_data_json = kwargs['ti'].xcom_pull(key='cleaned_data')
    data = pd.read_json(cleaned_data_json)

    # Encode categorical variables
    label_mappings = {}
    for column in data.select_dtypes(include=['object']).columns:
        encoder = LabelEncoder()
        data[column] = encoder.fit_transform(data[column])
        label_mappings[column] = {str(k): int(v) for k, v in zip(encoder.classes_, encoder.transform(encoder.classes_))}

    # Save label mappings, converting all int64 to int
    label_mappings = {key: {k: int(v) for k, v in value.items()} for key, value in label_mappings.items()}
    with open(LABEL_MAPPINGS_FILE, 'w') as f:
        json.dump(label_mappings, f, indent=4)

    kwargs['ti'].xcom_push(key='standardized_data', value=data.to_json())


def save_to_gsheets(**kwargs):
    standardized_data_json = kwargs['ti'].xcom_pull(key='standardized_data')
    data = pd.read_json(standardized_data_json)

    sheet = connect_to_google_sheets(PROCESSED_SHEET_NAME, JSON_KEYFILE_PATH)
    sheet.clear()
    sheet.update([data.columns.values.tolist()] + data.values.tolist())


with DAG(
    'data_processing_v2_dag',
    default_args={'owner': 'airflow', 'retries': 1},
    description='DAG to clean and standardize data from Google Sheets',
    schedule_interval='@daily',
    start_date=datetime(2023, 11, 1),
    catchup=False,
) as dag:

    fetch_task = PythonOperator(
        task_id='fetch_data_from_gsheets',
        python_callable=fetch_data_from_gsheets
    )

    clean_task = PythonOperator(
        task_id='clean_data',
        python_callable=clean_data
    )

    standardize_task = PythonOperator(
        task_id='standardize_data',
        python_callable=standardize_data
    )

    save_task = PythonOperator(
        task_id='save_to_gsheets',
        python_callable=save_to_gsheets
    )

    fetch_task >> clean_task >> standardize_task >> save_task
