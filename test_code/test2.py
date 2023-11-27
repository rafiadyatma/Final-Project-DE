import mysql.connector

# MySQL connection parameters
mysql_conn_params = {
    'host': '192.168.100.11',
    'user': 'mysql',
    'password': 'mysql',
    'database': 'mysql',
}

# Connect to MySQL
conn = mysql.connector.connect(**mysql_conn_params)
cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easier data access

# Execute a query
query = "SELECT * FROM covid_jabar LIMIT 2"
cursor.execute(query)

# Fetch all rows
result = cursor.fetchall()

# Print or process the data
if result:
    for row in result:
        print(row)
else:
    print("No data found in the table.")

# Close the cursor and connection
cursor.close()
conn.close()
