from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def process_data():
    # Pobierz dane
    df = pd.read_csv("/opt/airflow/dags/prepared_data.csv")
    # Usuń duplikaty
    df.drop_duplicates(inplace=True)
    # Uzupełnij braki
    df.fillna(df.median(numeric_only=True), inplace=True)
    # Zapisz dane
    df.to_csv('/opt/airflow/processed_data/processed_data.csv', index=False)

    # Wizualizacja
    sns.pairplot(df.select_dtypes(include=['float64', 'int64']))
    plt.savefig('/opt/airflow/visualizations/pairplot.png')

with DAG(
    dag_id='data_processing_dag',
    start_date=datetime(2024, 10, 1),
    schedule_interval=None
) as dag:
    process_data_task = PythonOperator(
        task_id='process_data',
        python_callable=process_data
    )