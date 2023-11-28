from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from modules import get_data_from_api_script
from modules import generate_dim_script

def get_data_from_api_func():
    get_data_from_api_script.get_data_from_api()

def generate_dim_func(**kwargs):
    generate_dim_script.load_dimension_tables(**kwargs)

def insert_district_daily_func():
    # Your logic for inserting district daily data goes here
    pass

def insert_province_daily_func():
    # Your logic for inserting province daily data goes here
    pass

with DAG(
    dag_id='d_1_etl_FinalProject',
    start_date=datetime(2022, 5, 28),
    schedule_interval='00 00 * * *',
    catchup=False
) as dag:

    get_data_from_api = PythonOperator(
        task_id='get_data_from_api',
        python_callable=get_data_from_api_func
    )

    generate_dim = PythonOperator(
        task_id='generate_dim',
        python_callable=generate_dim_func,
        provide_context=True
    )

    insert_district_daily = PythonOperator(
        task_id='insert_district_daily',
        python_callable=insert_district_daily_func
    )

    insert_province_daily = PythonOperator(
        task_id='insert_province_daily',
        python_callable=insert_province_daily_func
    )

    get_data_from_api >> generate_dim
    generate_dim >> insert_district_daily
    generate_dim >> insert_province_daily