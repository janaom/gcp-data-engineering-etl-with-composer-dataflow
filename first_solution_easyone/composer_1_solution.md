

This code defines an Airflow DAG (Directed Acyclic Graph) named "food_orders_dag" that schedules the execution of a Beam pipeline on a daily basis. The DAG uses the DataFlowPythonOperator to execute the Beam pipeline defined in the file located at gs://composer-bucket/beam.py. The pipeline processes data from the input file gs://your-bucket/food_daily.csv. The DAG is configured with default arguments, including the project and region information for Dataflow, and it does not catch up on missed runs.


## Composer 1 

If your code has `contrib` imports you can run it only in the Composer 1. More [info](https://airflow.apache.org/docs/apache-airflow/1.10.5/_api/airflow/contrib/operators/dataflow_operator/index.html#airflow.contrib.operators.dataflow_operator.DataFlowPythonOperator) about DataFlowPythonOperator.

Create a Composer environment.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/f5f7d40b-67fe-4206-9501-92b042c950f7)


 - Select n1-standard-1 (1 vCPU, 3.75 GB RAM)

 - Disk size: 30. The disk size in GB used for node VMs. Minimum is 30 GB. If unspecified, defaults to 100 GB. Cannot be updated. 

 - The Google Cloud Platform Service Account to be used by the node VMs. If a service account is not specified, the "default" Compute Engine service account is used. Cannot be updated. 

It took me around 15min to create Composer 1 environment. If it fails, try different zone.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/a9bb70e4-0cef-4290-ba6a-c81e587046f9)


Upload Beam code to your Composer bucket.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/4fe512ed-489a-4955-b289-89d72be61dcf)


Then go to the object details and copy gsutil URI and paste it in the DAG file (`py_file`).


![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/593511d3-fde2-4704-8c3e-030037802419)


![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/f7ee71f2-e788-4850-9ef3-ee8a388ae9b6)


Upload the Airflow code to the dags folder.


![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/d8279e8f-5899-4444-93a6-e4e18ff7c3a3)



The DAG will appear in Airflow UI.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/82aec353-b6bd-44a5-b06a-4e0a3c28a97a)


Wait for the run to complete or trigger the DAG manually (click on Trigger DAG).

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/6d8420b5-d650-4ccc-98b3-0a08bb144887)


Open Dataflow to see the progress. It takes around 6min to run Dataflow job.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/c34f4121-79e3-4669-870f-17c029f43610)

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/b7f6f19b-e2d2-4c21-8ee0-8e5c8f4a7176)

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/ae2745b8-f9ef-480b-871d-3c5db7b2e8d5)

The run completed.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/b9525886-1beb-40e9-850c-5c9daaefe50a)


You can click on the Airflow task to see the logs.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/4ae7d22f-51a5-4b4a-8489-fc3946c58bcc)



You should get the same results in BQ.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/a0a12fc2-9d07-42c6-9b7b-b0a27eb462e1)
