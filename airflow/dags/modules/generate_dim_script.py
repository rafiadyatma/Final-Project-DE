import mysql.connector
import psycopg2
from airflow import DAG
from datetime import datetime, timedelta
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator

# Get MySQL connection
def get_mysql_connection():
    return mysql.connector.connect(
        host='192.168.100.11',
        port = 3307,
        user='mysql',
        password='mysql',
        database='mysql'
    )

# Function to get PostgreSQL connection
def get_postgres_connection():
    return psycopg2.connect(
        host='192.168.100.11',
        port = 5435,
        user='postgres',
        password='postgres',
        database='dwh'
    )

# Function to create and load data into dimension tables
def load_dimension_tables(**kwargs):
    ti = kwargs['ti']
    mysql_conn = get_mysql_connection()
    postgres_conn = get_postgres_connection()

    # Load data into dim_province table
    ti.xcom_push(key='dim_province_data', value=load_dim_province(mysql_conn, postgres_conn))

    # Load data into dim_district table
    ti.xcom_push(key='dim_district_data', value=load_dim_district(mysql_conn, postgres_conn))

    # Close connections
    mysql_conn.close()
    postgres_conn.close()

def load_dim_province(mysql_conn, postgres_conn):
    
    cursor_mysql = mysql_conn.cursor(dictionary=True)
    cursor_mysql.execute('SELECT kode_prov, nama_prov FROM covid_jabar')
    dim_province_data = cursor_mysql.fetchall()

    cursor_postgres = postgres_conn.cursor()
    for row in dim_province_data:
        cursor_postgres.execute('INSERT INTO dim_province (province_id, province_name) VALUES (%s, %s) ON CONFLICT (province_id) DO NOTHING',
                                (row['kode_prov'], row['nama_prov']))

    postgres_conn.commit()
    cursor_mysql.close()
    cursor_postgres.close()

    return dim_province_data

def load_dim_district(mysql_conn, postgres_conn):
   
    cursor_mysql = mysql_conn.cursor(dictionary=True)
    cursor_mysql.execute('SELECT kode_kab, kode_prov, nama_kab FROM covid_jabar')
    dim_district_data = cursor_mysql.fetchall()

    cursor_postgres = postgres_conn.cursor()
    for row in dim_district_data:
        cursor_postgres.execute('INSERT INTO dim_district (district_id, province_id, district_name) VALUES (%s, %s, %s) ON CONFLICT (district_id) DO NOTHING',
                                (row['kode_kab'], row['kode_prov'], row['nama_kab']))

    postgres_conn.commit()
    cursor_mysql.close()
    cursor_postgres.close()

    return dim_district_data
