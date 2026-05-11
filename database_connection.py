import sqlite3
# Connect to database (creates file if not exists)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
# Create students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    roll TEXT,
    name TEXT
)
""")
# Create timetable table
cursor.execute("""
CREATE TABLE IF NOT EXISTS timetable (
    day TEXT,
    start TEXT,
    end TEXT,
    subject TEXT
)
""")
# Create attendance table
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    roll TEXT,
    name TEXT,
    subject TEXT,
    date TEXT,
    time TEXT
)
""")
# Save changes
conn.commit()
# Close connection
conn.close()
print("Database created successfully")