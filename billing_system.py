from datetime import datetime
import pymysql

db_name = input("Enter the database name: ")
table_name = input("Enter table name: ")

conn = pymysql.connect(
    host="localhost",
    user="user_name",
    password="mysql_password",
    database=db_name
)

cursor = conn.cursor()

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
cursor.execute(f"USE {db_name}")

cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    bill_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(225) NOT NULL,
    product_name VARCHAR(225) NOT NULL,
    product_price FLOAT NOT NULL,
    product_quantity INT NOT NULL,
    total FLOAT,
    bill_time DATETIME
)
""")

# BILL INPUT
customer_name = input("Enter customer name: ")
product_name = input("Enter product name: ")
product_quantity = int(input("Enter product quantity: "))
product_price = int(input("Enter price per item: "))

total = product_quantity * product_price
bill_time = datetime.now()

# INSERT DATA
query = f"""
INSERT INTO {table_name} 
(customer_name, product_name, product_price, product_quantity, total, bill_time)
VALUES (%s, %s, %s, %s, %s, %s)
"""
cursor.execute(query, (
    customer_name,
    product_name,
    product_price,
    product_quantity,
    total,
    bill_time
))
conn.commit()

bill_id = cursor.lastrowid

# CREATE BILL FILE
file_name = f"Bill_{bill_id}.txt"

with open(file_name, "w") as bill:
    bill.write("           -:CUSTOMER BILL:-          \n")
    bill.write(f"Bill ID       :    {bill_id}\n")
    bill.write(f"Date & Time   :    {bill_time}\n")
    bill.write("------------------------------------------------\n")
    bill.write(f"Customer Name :     {customer_name}\n")
    bill.write(f"Product Name  :     {product_name}\n")
    bill.write(f"Quantity      :     {product_quantity}\n")
    bill.write(f"Price         :     Rs {product_price}\n")
    bill.write("------------------------------------------------\n")
    bill.write(f"TOTAL AMOUNT  :     Rs {total}\n")
    bill.write("------------------------------------------------\n")
    bill.write("Thank you for shopping with us!\n")

print(f"Bill generated successfully: {file_name}")

cursor.close()
conn.close()
