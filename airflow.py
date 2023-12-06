from airflow import models
from datetime import datetime, timedelta
from airflow.contrib.operators.dataflow_operator import DataFlowPythonOperator

default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2023, 12, 3),
    'retries': 0,
    'retry_delay': timedelta(seconds=50),
	'dataflow_default_options': {
        'project': 'food-orders-407014',
        'region': 'us-central1', #composer region
		'runner': 'DataflowRunner'
    }
}

with models.DAG('food_orders_dag',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:
    
    t1 = DataFlowPythonOperator(
        task_id='beamtask',
        py_file='gs://us-central1-food-orders-dev-752d1f51-bucket/beam.py',
        options={'input' : 'gs://food-orders-us/food_daily.csv'}
    )
