from airflow import DAG
from airflow.utils.dates import datetime, timedelta
from airflow.providers.google.cloud.operators.dataflow import DataflowCreatePythonJobOperator

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
with DAG('food_orders_dag',
         default_args=default_args,
         schedule_interval=timedelta(days=1),
         catchup=False) as dag:
             
      #DataflowCreatePythonJobOperator to create and execute the Beam job
    t1 = DataflowCreatePythonJobOperator(
        task_id='beamtask',
         #Path to the Beam job file
        py_file='gs://composer-bucket/beam.py',
        options={
            #Input file for the job
            'input': 'gs://your-bucket/food_daily.csv'
        }
    )
