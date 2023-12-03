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

## Composer 1

If your code has `contrib` imports you can run it only in the Composer 1.

More [info](https://airflow.apache.org/docs/apache-airflow/1.10.5/_api/airflow/contrib/operators/dataflow_operator/index.html#airflow.contrib.operators.dataflow_operator.DataFlowPythonOperator) about DataFlowPythonOperator for the Composer 1.

Create a Composer environment

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/031c2d67-4a57-4139-a408-c8a51a02ed52)


 - Select n1-standard-1 (1 vCPU, 3.75 GB RAM)

 - Disk size: 30. The disk size in GB used for node VMs. Minimum is 30 GB. If unspecified, defaults to 100 GB. Cannot be updated. 

 - The Google Cloud Platform Service Account to be used by the node VMs. If a service account is not specified, the "default" Compute Engine service account is used. Cannot be updated. 

It took me around 15min to create Composer 1 environment. 

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/3e5897e4-602f-4da0-8517-10d4bc487c3b)
