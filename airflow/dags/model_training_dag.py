from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle

def train_model():
    # Pobieranie danych
    df = pd.read_csv('/opt/airflow/processed_data/processed_data.csv')
    X = df.drop('Delay', axis=1)
    y = df['Delay']

    # Podziel dane
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Trenuj model
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train)

    # Ewaluacja
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    # Zapisz model
    with open('/opt/airflow/models/xgboost_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    # Zapisz raport
    with open('/opt/airflow/reports/evaluation_report.txt', 'w') as f:
        f.write(f'Accuracy: {accuracy}\n')
        f.write(f'Report:\n{report}')

with DAG(
    dag_id='model_training_dag',
    start_date=datetime(2024, 10, 1),
    schedule_interval=None
) as dag:
    train_model_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model
    )
