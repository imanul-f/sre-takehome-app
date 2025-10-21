import sqlite3

# Connect to the database file
conn = sqlite3.connect('access_log.db')

# Create a cursor object
cursor = conn.cursor()

# Execute a SELECT query
cursor.execute("SELECT * FROM log;")

# Fetch all results
rows = cursor.fetchall()

# Print the header
print("ID | Timestamp              | Remote Address")
print("---|------------------------|------------------")
# Print the rows
for row in rows:
    print(f"{row[0]}  | {row[1]} | {row[2]}")

# Close the connection
conn.close()
