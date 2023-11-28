import mysql.connector
# MySQL connection parameters
mysql_conn_params = {
    'host': '192.168.100.11',
    'port': 3307,
    'user': 'mysql',
    'password': 'mysql',
    'database': 'mysql',
}

conn = mysql.connector.connect(**mysql_conn_params)
cursor = conn.cursor(dictionary=True)

query = "SELECT * FROM covid_jabar"
cursor.execute(query)

# Fetch all rows
result = cursor.fetchall()

# Print or process the data
for row in result:
    print(row['CLOSECONTACT'])

# Close the cursor and connection
cursor.close()
conn.close()