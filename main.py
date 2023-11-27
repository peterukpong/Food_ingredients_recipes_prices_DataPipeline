from airflow import DAG
import os
from datetime import datetime, timedelta
from web.operators.Eviction_operator import WebToGCSHKOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.operators.dummy import DummyOperator
from typing import Dict, Any, Optional, Sequence, Union
from airflow.models import BaseOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
import pandas as pd
import requests

# Define your default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

# Retrieve environment variables
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
DATASET = "Main_food"
OBJECT = "food_recipe"

# Create your DAG with a unique identifier
with DAG(dag_id="LoadFoodDataFromWebToGCSToBQ",
    default_args=default_args,
    schedule_interval="0 6 2 * *",
    ) as dag:

    # Create a starting dummy operator
    start = DummyOperator(task_id='start')

    # Define a custom Airflow operator named WebToGCSHKOperator
    class WebToGCSHKOperator(BaseOperator):
        def __init__(
            self,
            gcs_bucket_name: str,
            gcs_object_name: str,
            api_endpoint: str,
            api_headers: Dict[str, str],
            api_params: Dict[str, Union[str, int]],
            *args,
            **kwargs
        ) -> None:
            super().__init__(*args, **kwargs)
            self.gcs_bucket_name = gcs_bucket_name
            self.gcs_object_name = gcs_object_name
            self.api_endpoint = api_endpoint
            self.api_headers = api_headers
            self.api_params = api_params

        def execute(self, context: Dict[str, Any]) -> None:
            response = requests.get(self.api_endpoint, params=self.api_params, headers=self.api_headers)
            if response.status_code == 200:
                results_df = pd.DataFrame(response.json())
                csv_content = results_df.to_csv(index=False)
                gcs_hook = GCSHook(google_cloud_storage_conn_id="google_cloud_default")
                gcs_hook.upload(
                    bucket_name=self.gcs_bucket_name,
                    object_name=self.gcs_object_name,
                    data=csv_content.encode('utf-8'),
                    mime_type='text/csv',
                )
                self.log.info(f"Data uploaded to GCS: gs://{self.gcs_bucket_name}/{self.gcs_object_name}")
            else:
                self.log.error(f"Failed to retrieve data. Status code: {response.status_code}")
                raise ValueError(f"Failed to retrieve data. Status code: {response.status_code}")

    # Fetch and store data from an API into Google Cloud Storage
    download_to_gcs = WebToGCSHKOperator(
        task_id='download_to_gcs',
        gcs_bucket_name='Main_food',
        gcs_object_name='Food_recipe.csv',
        api_endpoint='https://api.spoonacular.com/recipes/1003464/priceBreakdownWidget.json',
        api_headers={
            "X-App-Token": '',
            "X-App-Secret": 'f4fa8a14706e47558346b15411ca4a9c',
        },
        api_params={
            "$limit": 2000,
        },
    )

    # Push data from Google Cloud Storage to BigQuery
    upload_to_bigquery = GCSToBigQueryOperator(
        task_id='upload_to_bigquery',
        source_objects=['Food-Data.csv'],
        destination_project_dataset_table=f"{DATASET}.{OBJECT}_table",
        schema_fields=[],
        skip_leading_rows=1,
        source_format='CSV',
        field_delimiter=',',
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_TRUNCATE',
        autodetect=True,
        bucket="Main_food",
    )

    # Create an ending dummy operator
    end = DummyOperator(task_id='end')

    # Define task dependencies
    start >> download_to_gcs >> upload_to_bigquery >> end
