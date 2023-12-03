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

