#PG / HOSTEL ROOM MANAGEMENT SYSTEM
import pymysql
import datetime
     
class Database:
    def __init__(self, database_name, table_name):
        self.database_name = database_name
        self.table_name = table_name

        self.connection = pymysql.connect(
          host="localhost", 
          user="username",
          password="Mysqlpassword"
         )
        self.cursor = self.connection.cursor()
        self.create_database()
        self.create_table()
    
    def create_database(self):
        # fixed: IF NOT EXISTS and safe quoting
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{self.database_name}`")
        self.cursor.execute(f"USE `{self.database_name}`")
        self.connection.commit()

    def create_table(self):
          query = f"""
            CREATE TABLE IF NOT EXISTS `{self.table_name}` (
            student_id INT PRIMARY KEY AUTO_INCREMENT,
            student_name VARCHAR(100),
            student_course VARCHAR(100),
            student_year INT,
            room_no INT,
            rent_paid VARCHAR(10),
            pay_day_time DATETIME
            )
            """
          # execute inside the method scope (was mis-indented previously)
          self.cursor.execute(query)
          self.connection.commit()

class Student:
    def __init__(self, student_id, student_name, student_course, student_year, room_no, rent_paid, pay_day_time=None):
          self.student_id = student_id
          self.student_name = student_name
          self.student_course = student_course
          self.student_year = student_year
          self.room_no = room_no
          self.rent_paid = rent_paid
          # fixed: correct attribute name and optional provided timestamp
          self.pay_day_time = pay_day_time if pay_day_time is not None else datetime.datetime.now("%Y-%m-%d %H:%M:%S")

class HostelManagement:
    def __init__(self, db):
          self.db = db
     
    def add_student(self):
          student_id=int(input("enter student id: "))
          student_name=input("enter student name: ")
          student_course=input("enter student course: ")
          student_year=int(input("enter student course year: "))
          room_no=int(input("enter the room no: "))
          rent_paid=input("rent paid (yes/no): ")
          # create Student object properly (fixed casing)
          student = Student(student_id, student_name, student_course, student_year, room_no, rent_paid)
          pay_day_time = student.pay_day_time
          query = f"""
          INSERT INTO {self.db.table_name}
          (student_id, student_name, student_course, student_year, room_no, rent_paid, pay_day_time)
          VALUES (%s,%s,%s,%s,%s,%s,%s)   
         """
        
          self.db.cursor.execute(query, (
            student_id, 
            student_name, 
            student_course, 
            student_year, 
            room_no, 
            rent_paid, 
            pay_day_time
          ))
          self.db.connection.commit()
          print("student added successfully:")
     
    def show_students(self):
         query =f"SELECT * FROM {self.db.table_name}"
         self.db.cursor.execute(query)
         for row in self.db.cursor.fetchall():
              print(row)

database_name = input("enter database name: ")
table_name = input("enter table name: ")

db = Database(database_name, table_name)
hostel = HostelManagement(db)

while True:
    print("""
    1. Add student
    2. Show student
    3. exit
    """)
     
    choice = int(input("enter your choice: "))

    if choice == 1:
        hostel.add_student()
    elif choice ==2:
        hostel.show_students()
    elif choice == 3:
        break
    else:
        print("invalid entry")
    

