from airflow import models
from datetime import datetime, timedelta
from airflow.contrib.operators.dataflow_operator import DataFlowPythonOperator

#Default arguments for the DAG
default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2023, 12, 3),
    'retries': 0,
    'retry_delay': timedelta(seconds=50),
	'dataflow_default_options': {
        'project': 'project-id',
        'region': 'composer-region', 
		'runner': 'DataflowRunner'
    }
}

#Define the DAG
with models.DAG('food_orders_dag',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:
    
    #DataFlowPythonOperator to execute the Beam pipeline
    t1 = DataFlowPythonOperator(
        task_id='beamtask',
        #Path to the Beam pipeline file
        py_file='gs://composer-bucket/beam.py',
        #Input file for the pipeline
        options={'input' : 'gs://your-bucket/food_daily.csv'}
    )
