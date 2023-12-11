
#project-id:dataset_id.table_id
delivered_table_spec = 'project-id:dataset_food_orders.delivered_orders'
#project-id:dataset_id.table_id
other_table_spec = 'project-id:dataset_food_orders.other_status_orders'

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import argparse
from google.cloud import bigquery

#Command-line argument parser
parser = argparse.ArgumentParser()

parser.add_argument('--input',
                      dest='input',
                      required=True,
                      help='Input file to process.')
                      
path_args, pipeline_args = parser.parse_known_args()

inputs_pattern = path_args.input

#Pipeline options
options = PipelineOptions(pipeline_args)
p = beam.Pipeline(options = options)

#Transformation functions
def remove_last_colon(row):
    #Remove the trailing colon from the fifth column of the row		
    cols = row.split(',')		
    item = str(cols[4])			
    
    if item.endswith(':'):
        cols[4] = item[:-1]		

    return ','.join(cols)		
	
def remove_special_characters(row): 
    #Remove special characters from each column of the row 
    import re
    cols = row.split(',')			
    ret = ''
    for col in cols:
        clean_col = re.sub(r'[?%&]','', col)
        ret = ret + clean_col + ','			
    ret = ret[:-1]						
    return ret

def print_row(row):
    print (row)

#Data processing pipeline
cleaned_data = (
	p
	| beam.io.ReadFromText(inputs_pattern, skip_header_lines=1)
	| beam.Map(remove_last_colon)
	| beam.Map(lambda row: row.lower())
	| beam.Map(remove_special_characters)
	| beam.Map(lambda row: row+',1')		
)


delivered_orders = (
	cleaned_data
	| 'delivered filter' >> beam.Filter(lambda row: row.split(',')[8].lower() == 'delivered')

)

other_orders = (
    cleaned_data
    | 'Undelivered Filter' >> beam.Filter(lambda row: row.split(',')[8].lower() != 'delivered')
)

(cleaned_data
 | 'count total' >> beam.combiners.Count.Globally() 		
 | 'total map' >> beam.Map(lambda x: 'Total Count:' +str(x))	
 | 'print total' >> beam.Map(print_row)

)

(delivered_orders
 | 'count delivered' >> beam.combiners.Count.Globally()
 | 'delivered map' >> beam.Map(lambda x: 'Delivered count:'+str(x))
 | 'print delivered count' >> beam.Map(print_row)
 )


(other_orders
 | 'count others' >> beam.combiners.Count.Globally()
 | 'other map' >> beam.Map(lambda x: 'Others count:'+str(x))
 | 'print undelivered' >> beam.Map(print_row)
 )

#BigQuery 
client = bigquery.Client()

dataset_id = "food-orders-407014.dataset_food_orders"

try:
	client.get_dataset(dataset_id)
	
except:
	dataset = bigquery.Dataset(dataset_id)  #

	dataset.location = "US"
	dataset.description = "dataset for food orders"

	dataset_ref = client.create_dataset(dataset_id, exists_ok=True)
	
def to_json(csv_str):
    #Convert a CSV string to a JSON object
    fields = csv_str.split(',')
    
    json_str = {"customer_id":fields[0],
                 "date": fields[1],
                 "timestamp": fields[2],
                 "order_id": fields[3],
                 "items": fields[4],
                 "amount": fields[5],
                 "mode": fields[6],
                 "restaurant": fields[7],
                 "status": fields[8],
                 "ratings": fields[9],
                 "feedback": fields[10],
                 "new_col": fields[11]
                 }

    return json_str
	
table_schema = 'customer_id:STRING,date:STRING,timestamp:STRING,order_id:STRING,items:STRING,amount:STRING,mode:STRING,restaurant:STRING,status:STRING,ratings:STRING,feedback:STRING,new_col:STRING'

(delivered_orders
	| 'delivered to json' >> beam.Map(to_json)
	| 'write delivered' >> beam.io.WriteToBigQuery(
	delivered_table_spec,
	schema=table_schema,
	create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
	write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
	additional_bq_parameters={'timePartitioning': {'type': 'DAY'}}
	)
)

(other_orders
	| 'others to json' >> beam.Map(to_json)
	| 'write other_orders' >> beam.io.WriteToBigQuery(
	other_table_spec,
	schema=table_schema,
	create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
	write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
	additional_bq_parameters={'timePartitioning': {'type': 'DAY'}}
	)
)
#Running the pipeline
from apache_beam.runners.runner import PipelineState
ret = p.run()
if ret.state == PipelineState.DONE:
    print('Success!!!')
else:
    print('Error Running beam pipeline')
