So we will use: GCS, Composer, Dataflow, BigQuery, Data Studio (not the same as Looker, need to try out)

# GCS

Upload csv file to your bucket

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/d4a9ee6d-a590-4a44-bf82-79497d4d0361)




# Beam code

Set the project: `gcloud config set project your-project-id`

Install Apache Beam: `pip install apache-beam[gcp]`

Run Beam code: `python beam.py --input gs://de-project-food-orders/food_daily.csv --temp_location gs://de-project-food-orders`


![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/6130ae85-b30a-4dc0-ac98-599294250bcb)

Results in BQ

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/9eb31561-5502-463e-8213-3a825b1434e2)


# Cloud Composer/Airflow 

Enable Cloud Composer API.
Enable Dataflow API.

## Composer 1

If your code has `contrib` imports you can run it only in the Composer 1.

More [info](https://airflow.apache.org/docs/apache-airflow/1.10.5/_api/airflow/contrib/operators/dataflow_operator/index.html#airflow.contrib.operators.dataflow_operator.DataFlowPythonOperator) about DataFlowPythonOperator for the Composer 1.

Create a Composer environment

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/031c2d67-4a57-4139-a408-c8a51a02ed52)


 - Select n1-standard-1 (1 vCPU, 3.75 GB RAM)

 - Disk size: 30. The disk size in GB used for node VMs. Minimum is 30 GB. If unspecified, defaults to 100 GB. Cannot be updated. 

 - The Google Cloud Platform Service Account to be used by the node VMs. If a service account is not specified, the "default" Compute Engine service account is used. Cannot be updated. 

It took me around 15min to create Composer 1 environment. 

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/177f66db-9af2-439b-a12a-8278b66500a3)

Upload Beam code to your Composer bucket

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/cad8071f-ae4f-45ed-9fa6-96e153b4aa98)

Then go to the object details and copy gsutil URI and paste it in the DAG file (py_file)

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/dc1f7432-b812-4551-b188-a76e13258066)

Upload the Airflow code to the dags folder

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/c67d352b-87a5-452e-99e0-46087570859b)

The DAG will appear in Airflow UI

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/86cb3dfb-0dc4-4731-8d9b-87bad82a7530)

You can trigger the DAG manually (click on Trigger DAG)

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/2565b3f2-7a34-410d-8426-7f1863370a06)



