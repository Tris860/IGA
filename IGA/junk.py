import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('website/app.db')

# Create a cursor object
cursor = conn.cursor()

# SQL statement to delete a record
delete_query = "ALTER TABLE Users RENAME TO  User"
query="ALTER TABLE User  ADD COLUMN status  BOOLEAN"
query3='UPDATE User SET username = "Janson Marcelo Kaske"  where  email ="ndayizeyejanson15@gmail.com"'
query2="DROP TABLE posts "
query4="CREATE TABLE posts( document_id Integer PRIMARY KEY,email VARCHAR(150) not null,title VARCHAR(150) not null,link VARCHAR(1000) not null,level VARCHAR(150) not null,lesson VARCHAR(150) not null,dateuploaded DATETIME ,status BOOLEAN not null,FOREIGN KEY(email) REFERENCES User(email))"

# The ID of the record to be deleted
record_id = 2

try:
    # Execute the delete statement
    # cursor.execute(query)
    cursor.execute(query3)
    # Commit the changes
    conn.commit()
    print("Record deleted successfully.")
except sqlite3.Error as error:
    print("Error while deleting record:", error)
finally:
    # Close the connection
    if conn:
        conn.close()
# update_query = """ UPDATE User SET  account_type = ? WHERE id = ? """ # Step 4: Execute the update query with parameters
# cursor.execute(update_query, ('Admin', 4)) # Step 5: Commit the transaction 
# conn.commit() 
# # Step 6: Close the connection 
# conn.close()
