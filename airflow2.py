from airflow import DAG
from airflow.utils.dates import datetime, timedelta
from airflow.providers.google.cloud.operators.dataflow import DataflowCreatePythonJobOperator

default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2023, 12, 3),
    'retries': 0,
    'retry_delay': timedelta(seconds=50),
    'dataflow_default_options': {
        'project': 'food-orders-407014',
        'region': 'us-central1',  # Airflow region
        'runner': 'DataflowRunner'
    }
}

with DAG('food_orders_dag',
         default_args=default_args,
         schedule_interval=timedelta(days=1),
         catchup=False) as dag:
    
    t1 = DataflowCreatePythonJobOperator(
        task_id='beamtask',
        py_file='gs://us-central1-food-orders-dev-6da85f96-bucket/beam.py',
        options={
            'input': 'gs://food-orders-us/food_daily.csv'
        }
    )
