# Food_ingredients_recipes_prices_DataPipeline

# Introduction:
This Airflow DAG is designed to automate the process of fetching data from the Spoonacular and Food Open Data API, storing it in a Google Cloud Storage (GCS) bucket, and subsequently loading the data into a BigQuery table. The DAG is scheduled to run at 6:00 AM every month.

# Data Architecture:
A robust data architecture is crucial for ensuring data quality, integrity, and accessibility. Here's the architecture for your Food Data Pipeline:

# Data Architecture
![image](https://github.com/peterukpong/Food_ingredients_recipes_prices_DataPipeline/assets/66263101/8897f0a0-b443-4207-b148-45857c1db29b)

1. Data Source:

"*" Spoonacular and Food Data API (Main_food dataset)

2. ETL (Extract, Transform, Load) Pipeline:

"*" Apache Airflow for orchestration and automation
"*" Custom operators for extracting data from the API and loading it into Google Cloud Storage (GCS)
"*" Google Cloud Storage (GCS) for intermediate storage of raw data

3. Data Warehouse:

"*" Google BigQuery for data warehousing
"*" Create a dedicated dataset in BigQuery (e.g., Main_food)
"*" Use tables in BigQuery to store raw and transformed data

4. Data Transformation:

"*" dbt (Data Build Tool) for data modeling, transformation, and analytics
"*" Data Reporting and Visualization:

5. Business Intelligence (BI) tools such as Tableau, Looker, or Google Data Studio

# Dataset Description:
"*" **Name**: Food Ingredients
"*" **Category**: Recipes, Ingredients and Prices
"*" **Data Source**: Spoonacular
"*" **Description**: This dataset contains food recipes, ingredients and prices obtained and made public by Spoonacular.

**Columns in the Dataset- Data Dictionary**
Rows - 39
Columns - 6

"*" **Name** (Text): The name of recipe or ingredient.
"*" **Amount** (Float): The amount the ingredient was bought.
"*" **Country** (Text): The country where the recipe originates.

# Data Pipeline:
The Eviction Notices Data Pipeline uses Apache Airflow to automate the process. Here's an overview:

1. **Start**: The DAG begins with a dummy operator.

2. **Download to GCS**: This task fetches data from the Spoonacular and Food Open Data API dataset, specifying the API endpoint, headers, and parameters. The data is stored in a Google Cloud Storage bucket.

**Explanation of Code**: The code for this task is defined in the WebToGCSHKOperator class within the WebToGCSHKOperator module. The class takes care of connecting to the API endpoint, retrieving the data, and saving it to a specified GCS bucket. It is scheduled to run at 6:00 AM every month, and the API token and parameters are defined in the task configuration.

3. **Upload to BigQuery**: Data from GCS is transferred to a BigQuery table. You can specify schema fields, file format, and other details for the data transfer.

**Explanation of Code**: The code for this task is defined in the GCSToBigQueryOperator class provided by the Google Cloud provider. This task reads data from the GCS bucket and loads it into a BigQuery table, specifying the destination table, schema fields, and other relevant configurations.

4. **End**: The DAG concludes with another dummy operator.

# Execution Frequency:
The pipeline is scheduled to run at 6:00 AM every month.

# Logs and Monitoring:
You can monitor task progress and success in the Airflow logs. Check for "INFO" level log entries for detailed task execution information.

# Error Handling:
In case of errors or failures, the pipeline is designed to handle them gracefully. For example, when the API is unavailable, the pipeline logs the error and retries the API call after a specified delay. If there are schema mismatches during the BigQuery upload, the pipeline can be configured to skip or handle them according to your defined rules.

# Data Validation:
Data validation checks are performed before data is loaded into BigQuery to ensure data completeness, consistency, and accuracy. Any data that does not conform to validation rules is flagged and logged for review.

# Authentication and Authorization:
Access to the pipeline and its components is secured using authentication and authorization mechanisms. Permissions are granted based on the principle of least privilege to restrict access to sensitive data and operations.

# Monitoring and Alerting:
Monitoring and alerting tools such as Stackdriver or Prometheus can be used to keep an eye on the pipeline's health.

# Scalability and Performance:
The pipeline is designed to handle large volumes of data efficiently. It can be scaled horizontally or vertically based on the changing data requirements. The performance of the pipeline is optimized to ensure data processing within defined SLAs.

# Data Retention:
Data retention policies are in place. For example, data is stored in GCS for a defined period, and there's a process for data archiving and purging as needed.

# DBT Integration:
To further enhance data transformation and modeling, dbt (Data Build Tool) is integrated into the pipeline. dbt models are structured to perform transformations and analytics on the data before it's made available for reporting and visualization.

# Pipeline Version Control:
Pipeline versions are managed to ensure proper documentation of changes and updates. Version control systems such as Git can be used to track pipeline code and configuration changes.

# Access to Data:
The data is accessible in BigQuery under the Main_food dataset, in a table named food_ingredients_data_table. You can run SQL queries for analysis.

# API Query:
You can retrieve data from the FOOD dataset using the following SoQL query: https://api.spoonacular.com/recipes/1003464/priceBreakdownWidget.json?apiKey=f4fa8a14706e47558346b15411ca4a9c

# Conclusion:
The Food Recipes Inredients and Prices Data Pipeline automates data extraction, storage, and analysis from Spoonacular (food) API. It ensures data integrity and accessibility in Google Cloud Storage and BigQuery for further analysis and reporting.

_Happy data engineering!_
