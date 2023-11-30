import psycopg2
import MySQLdb
from datetime import datetime

def insert_district_daily():
    # PostgreSQL connection
    connection_postgres = psycopg2.connect(
        host='192.168.100.11',
        port = 5435,
        user='postgres',
        password='postgres',
        database='dwh'
    )
    cursor_postgres = connection_postgres.cursor()

    # MySQL connection
    connection_mysql = MySQLdb.connect(
        host='192.168.100.11',
        port = 3307,
        user='mysql',
        password='mysql',
        database='mysql'
    )
    cursor_mysql = connection_mysql.cursor()

    try:
       
        cursor_postgres.execute("SET search_path TO dwh;")

        query_dim_case = "SELECT id, status FROM public.dim_case"
        cursor_postgres.execute(query_dim_case)
        dim_case_data = cursor_postgres.fetchall()

        for dim_case_row in dim_case_data:
            case_id, status = dim_case_row

            query_mysql = f"""
                SELECT 
                    kode_kab,
                    tanggal,
                    SUM({status}) as total
                FROM covid_jabar
                GROUP BY kode_kab, tanggal
            """

            cursor_mysql.execute(query_mysql)
            mysql_data = cursor_mysql.fetchall()

            insert_query = """
                INSERT INTO public.district_daily (district_id, case_id, date, total)
                VALUES (%s, %s, %s, %s)
            """

            cursor_postgres.executemany(
                insert_query, [(row[0], case_id, row[1], row[2]) for row in mysql_data]
            )

        # Commit the transaction
        connection_postgres.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursors and connections
        cursor_postgres.close()
        connection_postgres.close()

        cursor_mysql.close()
        connection_mysql.close()

if __name__ == "__main__":
    insert_province_daily()
