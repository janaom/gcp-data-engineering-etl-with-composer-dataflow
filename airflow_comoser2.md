## Composer 2

Create a Composer 2 environment.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/349d0685-6174-4c35-8e2b-545e2f59488c)

❗ It's important to give `Cloud Composer v2 API Service Agent Extension` role to your Service Account.

Select Environment size: Small.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/5377ced5-2b83-4f44-bdd0-fc0d51203954)

The rest is the same, add Beam code to the Composer bucket, copy `gsutil URl` link and add it to the DAG.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/4e59c352-9123-4566-b156-d98cd91fff6a)

Upload `airflow2.py` code to `dags` folder.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/518c7f43-2dcc-47d8-9a32-0c94bba84786)

In Airflow 2 you will get a new fancy dashboard.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/74c39295-ad3c-4c8e-bbe1-06c51195cb2a)

Wait for the run or trigger your DAG, check logs for more info. You should see the same result in Dataflow and Bigquery.

![image](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow/assets/83917694/957e9244-f6a9-4944-90d7-4b85b9a194cc)
