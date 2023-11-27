# Import necessary modules
# DAG File: The DAG file responsible for orchestrating the data pipeline and executing the SoQL query.
from airflow import DAG
import os
from datetime import datetime, timedelta
from web.operators.Eviction_operator import WebToGCSHKOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.operators.dummy import DummyOperator

# Define your default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),  # Set the initial execution date
    "email_on_failure": True,  # Send email on task failure
    "email_on_retry": False,  # Do not send email on task retries
    "retries": 2,  # Number of retries for each task
    "retry_delay": timedelta(minutes=1),  # Delay between retries
}

# Retrieve environment variables
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
DATASET = "Main_food"
OBJECT = "Food_recipe"

# Create your DAG with a unique identifier ('data_fetch_dag')
with DAG(dag_id="Load-Eviction-Data-From-Web-To-GCS-To-BQ",
     default_args=default_args,  # Use the default arguments defined above
     schedule_interval="0 6 2 * *",  # Schedule the DAG to run at a specific time 6:00am every month
     ) as dag:

    # Create a starting dummy operator
    start = DummyOperator(task_id='start')

    # Fetch and store data from an API into Google Cloud Storage
    download_to_gcs = WebToGCSHKOperator(
        task_id='download_to_gcs',
        gcs_bucket_name='Main_food',  # Specify the Google Cloud Storage bucket name
        gcs_object_name='Food-Data.csv',  # Specify the GCS object name
        api_endpoint='',  # API endpoint URL
        api_headers={
            "X-App-Token": '',  # API token header
            "X-App-Secret": 'f4fa8a14706e47558346b15411ca4a9c',  # API secret header
        },
        api_params={
            "$limit": 2000,  # API parameters
        },
    )

    # Push data from Google Cloud Storage to BigQuery
    upload_to_bigquery = GCSToBigQueryOperator(
        task_id='upload_to_bigquery',
        source_objects=['Food_recipe.csv'],  # Source object(s) in GCS
        destination_project_dataset_table=f"{DATASET}.{OBJECT}_table",  # Destination BigQuery table
        schema_fields=[],  # Define schema fields if needed
        skip_leading_rows=1,  # Skip leading rows in CSV
        source_format='CSV',  # Source file format
        field_delimiter=',',  # Delimiter used in CSV
        create_disposition='CREATE_IF_NEEDED',  # Create the table if it doesn't exist
        write_disposition='WRITE_TRUNCATE',  # Overwrite existing data in the table
        autodetect=True,  # Automatically detect schema
        bucket="Main_food",  # Specify the GCS bucket
    )

    # Create an ending dummy operator
    end = DummyOperator(task_id='end')

    # Define task dependencies
    start >> download_to_gcs >> upload_to_bigquery >> end

# Log messages to track task progress
download_to_gcs.doc = """
## Download to GCS Task

"""

upload_to_bigquery.doc = """
## Upload to BigQuery Task
In this task, data from the Google Cloud Storage (GCS) bucket is transferred to a BigQuery table. The task specifies the destination table in BigQuery and handles schema fields, source file format, and other relevant configurations. Data is loaded into BigQuery with options to create the table if it doesn't exist and to write/truncate existing data if needed. This task ensures that the data is available in BigQuery for further analysis.
"""

# Rest of the DAG and tasks remain the same
