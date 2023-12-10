from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.apache.beam.operators.beam import BeamRunPythonPipelineOperator
from airflow.providers.google.cloud.operators.dataflow import DataflowConfiguration
from airflow.providers.google.cloud.sensors.gcs import GCSObjectsWithPrefixExistenceSensor
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.operators.python import PythonOperator
from google.cloud.storage import Client

#Default arguments for the DAG
default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2023, 12, 3),
    'retries': 0,
    'retry_delay': timedelta(seconds=50),
}

def list_files(bucket_name, prefix, processed_prefix='processed/'):
    gcs_hook = GCSHook()
    files = gcs_hook.list(bucket_name, prefix=prefix)
    if files:
        # Move the file to the 'processed' subdirectory
        source_object = files[0]
        file_name = source_object.split('/')[-1]  # Get the file name
        destination_object = processed_prefix.rstrip('/') + '/' + file_name

        # Get the source blob
        storage_client = Client()
        bucket = storage_client.bucket(bucket_name)
        source_blob = bucket.blob(source_object)

        # Define the destination blob and create it with the same content as the source blob
        destination_blob = bucket.blob(destination_object)
        destination_blob.upload_from_string(source_blob.download_as_text())

        # Delete the source blob
        source_blob.delete()

        return destination_object
    else:
        return None

# Define the DAG
with DAG('food_orders_dag',
         default_args=default_args,
         schedule_interval='@daily',  #Runs daily
         catchup=False,
         max_active_runs=1) as dag:  #Limit to one active run at a time

    gcs_sensor = GCSObjectsWithPrefixExistenceSensor(
        task_id='gcs_sensor',
        bucket='food-orders-us',
        prefix='food_daily',
        mode='poke',
        poke_interval=60,  #Check every 60 seconds
        timeout=300  #Stop after 5 minutes if no file is found
    )

    list_files_task = PythonOperator(
        task_id='list_files',
        python_callable=list_files,
        op_kwargs={'bucket_name': 'food-orders-us', 'prefix': 'food_daily'},
        do_xcom_push=True,  #This will push the return value of list_files to XCom
    )

    beamtask = BeamRunPythonPipelineOperator(
        task_id='beam_task',
        runner='DataflowRunner',
        py_file='gs://us-central1-food-orders-dev-afb73621-bucket/beam2.py',
        pipeline_options={
            "input": 'gs://food-orders-us/{{ task_instance.xcom_pull("list_files") }}',
            #add other pipeline options as needed
        },
        py_options=[],
        py_interpreter="python3",
        py_system_site_packages=False,
        dataflow_config=DataflowConfiguration(
            job_name='food_orders_processing_job',
            project_id='food-orders-407014',
            location='us-central1',
        ),
    )

    gcs_sensor >> list_files_task >> beamtask
