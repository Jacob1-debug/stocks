import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('instance/stocks.db')  # Adjust the path as necessary
cursor = conn.cursor()

# Query the database
cursor.execute("SELECT * FROM stock")
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the connection
conn.close()
