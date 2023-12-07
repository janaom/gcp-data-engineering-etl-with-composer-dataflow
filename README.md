So we will use: GCS, Composer, Dataflow, BigQuery, Data Studio (not the same as Looker, need to try out)

# GCS 🪣

Upload csv file to your bucket

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/285dcfd6-f212-418b-b5bc-e56beb35fa52)




# Beam code ![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/ccdad178-1609-41d7-9393-f47e065c9d29)

📖

This code is a data processing pipeline implemented using Apache Beam. It reads data from an input file, performs cleaning and filtering operations, and writes the results to two separate BigQuery tables based on specific conditions.

The pipeline consists of the following steps:

1. Command-line arguments are parsed to specify the input file.
2. The data is read from the input file and undergoes cleaning operations, such as removing trailing colons and special characters.
3. The cleaned data is split into two branches based on the status of the orders: delivered and undelivered.
4. The total count of records, delivered orders count, and undelivered orders count are computed and printed.
5. The cleaned and filtered data from the delivered orders branch is transformed into JSON format and written to a BigQuery table.
6. Similarly, the cleaned and filtered data from the undelivered orders branch is transformed into JSON format and written to another BigQuery table.
7. The pipeline is executed, and the success or failure status is printed.

👩‍💻

Set the project: `gcloud config set project your-project-id`

Install Apache Beam: `pip install apache-beam[gcp]`

Test Beam code in the shell:  `python beam.py --input gs://your-bucket/food_daily.csv --temp_location gs://your-bucket`

❗  Make sure that all your files and services are in the same location. E.g. both buckets should be in the same location or you will get the error message: 'Cannot read and write in different locations: source: US, destination: EU’


![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/5f26e09a-3b98-4848-9413-097a49a84bd6)



Check results in BQ.  

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/8d18241f-4ede-431e-b123-744ed9470f0c)




# Cloud Composer/Airflow ![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/41c83c58-4685-41df-a3d8-3aedb1f94b23)

📖

This code defines an Airflow DAG (Directed Acyclic Graph) named "food_orders_dag" that schedules the execution of a Beam pipeline on a daily basis. The DAG uses the DataFlowPythonOperator to execute the Beam pipeline defined in the file located at `gs://us-central1-food-orders-dev-752d1f51-bucket/beam.py`. The pipeline processes data from the input file `gs://food-orders-us/food_daily.csv`. The DAG is configured with default arguments, including the project and region information for Dataflow, and it does not catch up on missed runs.

👩‍💻

Enable Cloud Composer API, Dataflow API: `gcloud services enable composer.googleapis.com dataflow.googleapis.com`

## Composer 1 

If your code has `contrib` imports you can run it only in the Composer 1. More [info](https://airflow.apache.org/docs/apache-airflow/1.10.5/_api/airflow/contrib/operators/dataflow_operator/index.html#airflow.contrib.operators.dataflow_operator.DataFlowPythonOperator) about DataFlowPythonOperator.

Create a Composer environment

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/885a4d8f-e48c-4bc3-84c6-8a13f0cf8fb4)


 - Select n1-standard-1 (1 vCPU, 3.75 GB RAM)

 - Disk size: 30. The disk size in GB used for node VMs. Minimum is 30 GB. If unspecified, defaults to 100 GB. Cannot be updated. 

 - The Google Cloud Platform Service Account to be used by the node VMs. If a service account is not specified, the "default" Compute Engine service account is used. Cannot be updated. 

It took me around 15min to create Composer 1 environment. If it fails, try different zone.

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/31f6b7f2-8aee-4f5e-9471-1c31903b9ca9)


Upload Beam code to your Composer bucket

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/99e182d7-2259-4099-8e28-5a7a3f8bc785)


Then go to the object details and copy gsutil URI and paste it in the DAG file (`py_file`)


![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/9c598cf6-42d4-4792-81bc-dfdad86aebae)


Upload the Airflow code to the dags folder


![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/f0e3d1f2-1d82-4acd-9ae7-a8631a920f0b)


The DAG will appear in Airflow UI

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/766cae5f-3062-4509-8c91-35c79eebd62d)


You can trigger the DAG manually (click on Trigger DAG)

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/40bdaccf-20aa-49e7-b96b-a4ee3ee7a8d8)


Open Dataflow to see the progress. It takes around 6min to run Dataflow job

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/5dcffb86-c666-4197-a634-2d5c2912980b)

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/687313a1-497a-4d28-b112-89f628a73e03)

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/6124d148-7c3d-460b-89d7-362f19649999)


You can click on the Airflow task to see the logs

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/664a77bd-fc38-45cc-b258-99b82e51e11d)


You should get the same results in BQ. 

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/ddd5f7b5-d809-46dc-8632-871287e4e39a)


## Composer 2

Create a Composer 2 environment

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/349d0685-6174-4c35-8e2b-545e2f59488c)

❗ It's important to give `Cloud Composer v2 API Service Agent Extension` role to your Service Account.

Select Environment size: Small.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/5377ced5-2b83-4f44-bdd0-fc0d51203954)

The rest is the same, add Beam code to the Composer bucket, copy `gsutil URl` link and add it to the DAG.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/4e59c352-9123-4566-b156-d98cd91fff6a)

Upload `airflow2.py` code to `dags` folder

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/518c7f43-2dcc-47d8-9a32-0c94bba84786)

In Airflow 2 you will get a new fancy dashboard

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/74c39295-ad3c-4c8e-bbe1-06c51195cb2a)

Wait for the run or trigger your DAG, check logs for more info. You should see the same result in Dataflow and Bigquery.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/957e9244-f6a9-4944-90d7-4b85b9a194cc)

