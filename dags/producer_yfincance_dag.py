from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from producer.main_producer import main

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='producer_yahoo_data_pipeline',
    default_args=default_args,
    description='Fetch financial data from Yahoo and push to Kafka',
    schedule_interval='*/5 * * * *', 
    start_date=datetime(2025, 5, 1),  
    catchup=False,  
    tags=['kafka', 'yahoo', 'finance']
) as dag:

    run_producer = PythonOperator(
        task_id='run_producer_task',
        python_callable=main,
        op_kwargs={
            'params': {
                'api_name': 'yahoo',
                'use_symbols_test': True,
                'broker': 'kafka:9092',
                'topic': 'market_data',
                'period': '1mo',
                'interval': '1d',
                'batch_size': 50
            }
        }
    )

    run_producer
