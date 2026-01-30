import pymysql
import random
from datetime import datetime
import smtplib

# mysql connection
db_name = input("enter your database name: ")
table_name = input("enter table name: ")

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="MySQLBharti@2006"
) 
cursor = conn.cursor()

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
cursor.execute(f"USE {db_name}")

# create table
cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {table_name} (
id INT PRIMARY KEY AUTO_INCREMENT,
transaction_type VARCHAR(225),
amount FLOAT,
data_time DATETIME,
balance FLOAT
)
""")

# initial balance
amount = 10000

for i in range(5):
    print("\nwelcome to ATM")
    print("press 1 for deposit: \npress 2 for withdrawal: \npress 3 for check balance")
    choice = int(input())

    if choice == 1:
        purpose = "deposit"
    elif choice == 2:
        purpose = "withdrawal"
    elif choice == 3:
        purpose = "check balance"
    else:
        print("invalid choice")
        exit()

    user_email = input("enter your email: ")

    otp = random.randint(100000, 999999)

    sender_email = "sharmabharti7112006@gmail.com"
    sender_password = "vxow ilnj itcu fwwj"

    message = f"""Subject: ATM {purpose} Verification

Your OTP for {purpose} is: {otp}"""

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, user_email, message)
    server.quit()

    print("OTP sent successfully for your ATM", purpose)

    user_email_otp = int(input("Enter OTP: "))

    if user_email_otp == otp:

        current_time = datetime.now()

        if choice == 1:
            deposit_amount = int(input("Enter amount to deposit: "))
            amount += deposit_amount
            print("Your balance is:", amount)

            cursor.execute(f"""
            INSERT INTO {table_name} (transaction_type, amount, data_time, balance)
            VALUES (%s, %s, %s, %s)
            """, ("Deposit", deposit_amount, current_time, amount))
            conn.commit()

            with open(f"{table_name}_passbook.txt", "a") as f:
                f.write(f"| Deposit | {deposit_amount} | {amount}\n")

        elif choice == 2:
            withdraw_amount = int(input("Enter amount to withdraw: "))
            if withdraw_amount <= amount:
                amount -= withdraw_amount
                print("Your balance is:", amount)

                cursor.execute(f"""
                INSERT INTO {table_name} (transaction_type, amount, data_time, balance)
                VALUES (%s, %s, %s, %s)
                """, ("Withdrawal", withdraw_amount, current_time, amount))
                conn.commit()

                with open(f"{table_name}_passbook.txt", "a") as f:
                    f.write(f"| Withdrawal | {withdraw_amount} | {amount}\n")
            else:
                print("Insufficient balance ❌")

        elif choice == 3:
            print("Your balance is:", amount)

            cursor.execute(f"""
            INSERT INTO {table_name} (transaction_type, amount, data_time, balance)
            VALUES (%s, %s, %s, %s)
            """, ("Check Balance", 0, current_time, amount))
            conn.commit()

            with open(f"{table_name}_passbook.txt", "a") as f:
                f.write(f"| Check Balance | 0 | {amount}\n")

    else:
        print("Invalid OTP ❌")

cursor.close()
conn.close()
print(f"Passbook saved successfully as {table_name}_passbook.txt")
