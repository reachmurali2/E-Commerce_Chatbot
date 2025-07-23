import pandas as pd
import sqlite3

# 📂 Define File Paths
# Database and CSV file paths
db_path = 'db.sqlite'
csv_path = 'flipkart_product_data.csv'

# 🛠️ Connect to Database
# Connect to SQLite database (creates one if not exists)
conn = sqlite3.connect(db_path)                                     # Creates or connects to the database file.
cursor = conn.cursor()                                              # Initializes a cursor to execute SQL commands.

# 🧱 Create Table (If Not Exists)
# Create the product table if it does not exist                     # Creates a table named product with columns matching the CSV schema.
cursor.execute('''
CREATE TABLE IF NOT EXISTS product (
    product_link TEXT,
    title TEXT,
    brand TEXT,
    price INTEGER,
    discount FLOAT,
    avg_rating FLOAT,
    total_ratings INTEGER
);
''')

# 💾 Commit Table Creation
# Commit the table creation                                        # Ensures that the table creation is saved in the DB.
conn.commit()

# 📥 Load and Insert CSV Data
# Read CSV file using pandas
df = pd.read_csv(csv_path)                                         # Reads the CSV into a DataFrame df.

# Insert data into the product table
df.to_sql('product', conn, if_exists='append', index=False)  # Inserts all rows into the product table.

# 🔚 Close Connection
# Close the connection     
conn.close()                                                       # Closes the database connection to release resources.

# ✅ Confirmation Message
print("Data inserted successfully!")                               # Console log to confirm successful operation.
