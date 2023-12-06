So we will use: GCS, Composer, Dataflow, BigQuery, Data Studio (not the same as Looker, need to try out)

# GCS 🪣

Upload csv file to your bucket

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/285dcfd6-f212-418b-b5bc-e56beb35fa52)




# Beam code ![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/efadef42-4d27-4223-888d-f2a55eb6d006)



Set the project: `gcloud config set project your-project-id`

Install Apache Beam: `pip install apache-beam[gcp]`

Test Beam code in the shell: `python beam.py --input gs://de-project-food-orders/food_daily.csv --temp_location gs://de-project-food-orders`

❗  Make sure that all your files and services are in the same location. E.g. both buckets should be in the same location or you will get the error message: 'Cannot read and write in different locations: source: US, destination: EU’


![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/ea3f1109-0672-4600-8d69-e5ea4e1c7484)


Results in BQ. To avoid any errors delete the dataset/tables/view before running the code in the next step. 

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/5a5d939a-8988-4ffe-a18f-aee0142ce75e)



# Cloud Composer/Airflow  ![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/e1d45e3d-67d7-4b81-b7b5-82829a082cfe)

Enable Cloud Composer API.

Enable Dataflow API.

## Composer 1 

If your code has `contrib` imports you can run it only in the Composer 1.

More [info](https://airflow.apache.org/docs/apache-airflow/1.10.5/_api/airflow/contrib/operators/dataflow_operator/index.html#airflow.contrib.operators.dataflow_operator.DataFlowPythonOperator) about DataFlowPythonOperator for the Composer 1.

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




