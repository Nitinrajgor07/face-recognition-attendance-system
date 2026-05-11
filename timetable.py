import sqlite3

# Connect to database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Clear old timetable (important to avoid duplicates)
cursor.execute("DELETE FROM timetable")

# Insert timetable data
data = [
("Monday","09:30","11:00","ADBMS Lab"),
("Monday","10:50","11:40","TD-PCL"),
("Monday","11:45","12:35","EST"),
("Monday","12:35","13:25","BC"),
("Monday","14:10","15:00","ML"),

("Tuesday","10:00","11:40","PP Lab"),
("Tuesday","11:45","12:35","ML"),
("Tuesday","12:35","13:25","ADBMS"),
("Tuesday","14:10","15:00","BC"),

("Wednesday","10:50","11:40","Library"),
("Wednesday","11:45","12:35","ADBMS"),
("Wednesday","12:35","13:25","BC"),
("Wednesday","14:10","15:00","ML"),
("Wednesday","15:00","16:40","EH Lab"),

("Thursday","11:45","12:35","PP"),
("Thursday","12:35","13:25","PP"),
("Thursday","14:10","15:00","ADBMS"),
("Thursday","15:00","16:40","ML Lab"),

("Friday","10:00","11:40","ADBMS Lab"),
("Friday","11:45","12:35","PP"),
("Friday","12:35","13:25","PP"),
("Friday","14:10","15:00","PP Lab")
]
# Insert all data
cursor.executemany("INSERT INTO timetable VALUES (?,?,?,?)", data)
# Save changes
conn.commit()
# Close database
conn.close()
print("Timetable inserted successfully")