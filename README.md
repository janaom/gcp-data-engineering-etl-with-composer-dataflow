# <img width="40" alt="image" src="https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/60f8f158-3bdc-4b3d-94ae-27a12441e2a3"> GCP Data Engineering Project: Building and Orchestrating an ETL Pipeline for Online Food Delivery Industry with Apache Beam and Apache Airflow

This GCP Data Engineering project focuses on developing a robust ETL (Extract, Transform, Load) pipeline for the online food delivery industry. The pipeline is designed to handle batch transactional data and leverages various Google Cloud Platform (GCP) services:

- <img width="18" alt="image" src="https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/6b5ffddf-0f74-41cf-8303-22f675cabdda"> GCS is used to store and manage the transactional data
- <img width="18" alt="image" src="https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/4c57cf42-15d3-4ba3-bad6-65b7fb9c5094"> Composer, a managed Apache Airflow service, is utilized to orchestrate Dataflow jobs
- <img width="18" alt="image" src="https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/69ceceb2-73a4-4b8b-9eb1-1207e7b5c5e3"> Dataflow, based on Apache Beam, is responsible for data processing, transformation, and loading into BigQuery
- <img width="18" alt="image" src="https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/48de05df-2b34-4d82-b2c5-e81809e9322c"> BigQuery serves as a serverless data warehouse
- <img width="18" alt="image" src="https://seeklogo.com/images/G/google-looker-logo-B27BD25E4E-seeklogo.com.png"> Looker, a business intelligence and analytics platform, is employed to generate daily reports

These technologies work together to efficiently process, store, and generate reports on the daily transaction data.

![GCP-Diagram](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/f3a7ff86-92b3-46db-a156-e5ebbefc3bb9)


# <img width="30" alt="image" src="https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/6b5ffddf-0f74-41cf-8303-22f675cabdda"> GCS

Upload the provided CSV file to your designated Google Cloud Storage (GCS) bucket. This transactional data represents a sample of real-world cases from the online food delivery industry. It includes information such as customer ID, date, time, order ID, items ordered, transaction amount, payment mode, restaurant name, order status, customer ratings, and feedback. The data showcases various scenarios, including late delivery, stale food, and complicated ordering procedures, providing valuable insights into different aspects of the customer experience.

![image](https://github.com/janaom/gcp-data-engineering-project-food-orders-etl/assets/83917694/285dcfd6-f212-418b-b5bc-e56beb35fa52)




# <img width="40" alt="image" src="https://beam.apache.org/images/mascot/beam_mascot_500x500.png"> Beam code

📖

`beam.py` code is a data processing pipeline implemented using Apache Beam. It reads data from an input file, performs cleaning and filtering operations, and writes the results to two separate BigQuery tables based on specific conditions.

The pipeline consists of the following steps:

1. Command-line arguments are parsed to specify the input file.
2. The data is read from the input file and undergoes cleaning operations, such as removing trailing colons and special characters.
3. The cleaned data is split into two branches based on the status of the orders: delivered and undelivered.
4. The total count of records, delivered orders count, and undelivered orders count are computed and printed.
5. The cleaned and filtered data from the delivered orders branch is transformed into JSON format and written to a BigQuery table.
6. Similarly, the cleaned and filtered data from the undelivered orders branch is transformed into JSON format and written to another BigQuery table.
7. The pipeline is executed, and the success or failure status is printed.

👩‍💻

Set the project in the cloud shell: `gcloud config set project your-project-id`

Install Apache Beam in the cloud shell: `pip install apache-beam[gcp]`

Give the Beam code a test run in the shell and then check the results in BigQuery:  `python beam.py --input gs://your-bucket/food_daily.csv --temp_location gs://your-bucket`

❗  Make sure that all your files and services are in the same location. E.g. both buckets should be in the same location or you will get a similar error message: 'Cannot read and write in different locations: source: US, destination: EU’


![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/5f26e09a-3b98-4848-9413-097a49a84bd6)



![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/8d18241f-4ede-431e-b123-744ed9470f0c)

To avoid any confusion, it is recommended to delete the dataset before moving forward with actions that involve appending data in BigQuery.




# <img width="40" alt="image" src="https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/c1d5bfc6-94c3-44e4-b38e-4eaf5656a840"> Composer/Airflow

📖

The DAG monitors the GCS bucket for new files with the specified prefix using the GoogleCloudStoragePrefixSensor (for Airflow 1) or GCSObjectsWithPrefixExistenceSensor (for Airflow 2). When a new file is found, it executes the `list_files` function which uses the GoogleCloudStorageHook (for Airflow 1) and GCSHook (for Airflow 2) to move the file to a 'processed' subdirectory and delete the original file. Finally, it triggers the execution of a Dataflow pipeline using the DataFlowPythonOperator (for Airflow 1) or DataflowCreatePythonJobOperator/BeamRunPythonPipelineOperator (for Airflow 2) with the processed file as input.

This setup is ideal for recurring data processing workflows where files arrive in a GCS bucket at regular intervals (e.g., every 10 minutes) and need to be transformed using Dataflow and loaded into BigQuery. By using Apache Airflow and this DAG, you can automate and schedule the data processing workflow. The DAG ensures that the tasks are executed in the defined order and at the specified intervals.

Do note that the actual operator and hook names, and some of their parameters, will differ between Airflow 1 and Airflow 2. Be sure to use the correct names and parameters for your version of Airflow. For example, if your code contains `contrib` imports, it can only be run in Composer 1. 

For more information about Airflow operators, please refer to the official Apache Airflow documentation at https://airflow.apache.org/ or the Astronomer Registry at https://registry.astronomer.io/. Additionally, if you have any specific questions or need further guidance, you can interact with "Ask Astro" an LLM-powered chatbot, available at https://ask.astronomer.io.

👩‍💻

Enable Cloud Composer API, Dataflow API: `gcloud services enable composer.googleapis.com dataflow.googleapis.com`

## 🌠Composer 1 

[DataFlowPythonOperator](https://airflow.apache.org/docs/apache-airflow/1.10.5/_api/airflow/contrib/operators/dataflow_operator/index.html#airflow.contrib.operators.dataflow_operator.DataFlowPythonOperator) can be used to launch Dataflow jobs written in Python.

To proceed, create a Composer 1 environment.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/f5f7d40b-67fe-4206-9501-92b042c950f7)


 - Select n1-standard-1 (1 vCPU, 3.75 GB RAM)

 - Disk size: 30. The disk size in GB used for node VMs. Minimum is 30 GB. If unspecified, defaults to 100 GB. Cannot be updated. 

 - The Google Cloud Platform Service Account to be used by the node VMs. If a service account is not specified, the "default" Compute Engine service account is used. Cannot be updated.

Creating a Composer 1 environment typically takes around 15 minutes. If the creation process fails, you may want to consider trying a different zone.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/a9bb70e4-0cef-4290-ba6a-c81e587046f9)

The same `beam.py`, tested in the shell, can be used for both Composer 1 and Composer 2. 

Upload the `beam.py` code to the Composer bucket.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/4fe512ed-489a-4955-b289-89d72be61dcf)


Go to the object details, copy `gsutil URI` and paste it in the DAG file (`py_file`).


![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/593511d3-fde2-4704-8c3e-030037802419)

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/8601ea31-2c88-42d6-9441-bf5576b0e19e)

Upload `airflow.py` file to the dags folder.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/91ef65c4-37de-42b4-85be-85187a4db78c)

After a few minutes, the DAG will appear in the Airflow UI. For testing purposes, the DAG is initially scheduled to run every 10 minutes. However, you have the flexibility to modify the schedule according to your specific requirements. Wait for the scheduled run to occur automatically or manually trigger the DAG.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/52cfa6e7-e577-412c-963c-2861dc2eb4cf)

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/e671c5ef-ed4c-470d-b96a-636119e9b847)

To gain a better understanding of the process, review the logs of each individual task. 

### 🚀 gcs_sensor

Sensor checks existence of objects: food-orders-us, food_daily. Success criteria met. Sensor found the file in the bucket.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/378cd73f-d29c-43d4-9d3f-3e5cf3c754d9)

### 🚀 list_files

Object food_daily.csv in bucket food-orders-us copied to object processed/food_daily.csv in bucket food-orders-us. Blob food_daily.csv deleted.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/f1689521-8ce8-4444-b2f1-83677a6d1ac9)

Folder created.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/9451caf3-61db-4612-915f-0e3938bef965)

### 🚀 beamtask

The Dataflow job has just started.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/03784888-c23d-43ae-9b15-f3383dd984fe)


Check the completed tasks in Dataflow.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/922be238-59f7-413e-9415-f6cda9b772f5)

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/cef67aea-f2ce-4d7a-8047-5a46cc237758)

Open BigQuery to see the results.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/eebb4d73-6332-4a90-8798-e81cc5b2f628)

In practice, files often come with timestamps. As a test, I have uploaded a new file to the bucket to verify if the solution is functioning correctly.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/6a16b07e-7bc3-4522-9fb6-ff94347ffa63)


The solution performed as expected. The new file was successfully copied to the 'processed' folder, and the same process was repeated. The resulting transformed data will be appended to the existing tables in BigQuery.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/a4d449d0-35ec-42dc-b6b6-c08e91934b95)

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/12d734e3-d0ae-44ff-9bd6-f1e8b27859e1)

The values can be accessed and retrieved from XComs.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/1e26c216-0a18-475d-98eb-367883d7469a)



## 🌠Composer 2

Let's move to Composer 2. Create a Composer 2 environment. 

The DAGs feature two operators: [DataflowCreatePythonJobOperator](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/operators/dataflow/index.html#airflow.providers.google.cloud.operators.dataflow.DataflowCreatePythonJobOperator) and [BeamRunPythonPipelineOperator](https://airflow.apache.org/docs/apache-airflow-providers-apache-beam/stable/operators.html#python-pipelines-with-dataflowrunner). While the former is deprecated and no longer actively maintained, it is still available and functional. Although it is recommended to use the Beam operator for improved functionality and ongoing support, you can still try the deprecated operator.


![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/9d918734-cd98-49eb-a973-586d6178d341)


❗ It's important to give `Cloud Composer v2 API Service Agent Extension` role to your Service Account.

Select Environment size: Small.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/64581910-e4e2-4196-8812-4478a5af0739)



The rest is the same, upload CSV file to the bucket, add Beam code to the Composer bucket, copy `gsutil URl` link and add it to the DAG.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/a7198bbd-db3c-49b3-b8d8-dd7b6e50d690)


![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/22293adc-98b2-42ba-932e-e565867b7862)


![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/c4c5018d-7eb3-448e-875c-7c975c1200a9)



![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/f28d8fa7-84f1-4e0a-8184-575aeb9e2ece)




Upload `airflow2.py` code to the dags folder (with DataflowCreatePythonJobOperator or BeamRunPythonPipelineOperator).


Wait for the DAG to appear in the Airflow UI.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/2867c0f1-922e-48c8-a657-7563a9afbdcb)

Operators will be visible in the Graph section.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow-TEST/assets/83917694/1e6cc0bb-28a2-497c-be2d-a73a27a99d9b)


![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow-TEST/assets/83917694/42c60726-f7da-4e0c-8d88-161a69e4fc69)



Since it is scheduled to run '@daily' this time, I manually triggered it.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/4b889475-d7ab-4c62-81eb-97f153b2bb91)

Open Dataflow to check if the job is currently running.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/4fe108f0-ddce-458e-83fa-159a4860f186)

As expected, the Dataflow job will create 2 tables in BigQuery. 👏🎉


❗ Make sure to delete Composer from your setup as it can be a costly service. It's worth mentioning that Google Cloud provides an advantageous [Free Trial](https://cloud.google.com/free/docs/free-cloud-features#free-trial) option. As a new customer, you will receive $300 in free credits, allowing you to thoroughly explore and assess the capabilities of Google Cloud without incurring any additional expenses.

# <img width="30" alt="image" src="https://seeklogo.com/images/G/google-looker-logo-B27BD25E4E-seeklogo.com.png"> Looker

Connect to your Looker account: https://lookerstudio.google.com. Select BQ connection.
Create your own daily report, use delivered/other_status_orders tables. Here is my example

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/ebca078f-f231-4f86-9938-c0cf026c0c97)
