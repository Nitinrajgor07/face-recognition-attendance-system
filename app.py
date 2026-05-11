import cv2
import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from imutils.video import VideoStream
import time

# Load model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')

# Face detector
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# DB connection
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Get today's subject
today = datetime.now().strftime("%A")
cursor.execute("SELECT DISTINCT subject FROM timetable WHERE day=?", (today,))
subjects = [row[0] for row in cursor.fetchall()]

# Show only one subject (demo-friendly)
today = datetime.now().strftime("%A")
cursor.execute("SELECT DISTINCT subject FROM timetable WHERE day=?", (today,))
subjects = [row[0] for row in cursor.fetchall()]

# Attendance function
def start_attendance(subject):

    vs = VideoStream(src=0).start()
    time.sleep(2.0)

    frame_count = 0

    while True:
        img = vs.read()

        if img is None:
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        # Show camera FIRST
        cv2.imshow(f"Attendance - {subject}", img)

        frame_count += 1

        # Wait ~1 sec before detection
        if frame_count < 30:
            cv2.waitKey(1)
            continue

        for (x, y, w, h) in faces:

            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            if confidence < 60:

                cursor.execute("SELECT roll, name FROM students WHERE id=?", (id,))
                result = cursor.fetchone()

                if result:
                    roll, name = result

                    now = datetime.now()
                    day = now.strftime("%A")
                    current_time = now.strftime("%H:%M")
                    date = now.strftime("%Y-%m-%d")

                    # Time validation
                    cursor.execute("""
                    SELECT * FROM timetable
                    WHERE day=? AND subject=? AND start<=? AND end>=?
                    """, (day, subject, current_time, current_time))

                    if cursor.fetchone():

                        # Duplicate check
                        cursor.execute("""
                        SELECT * FROM attendance
                        WHERE roll=? AND subject=? AND date=?
                        """, (roll, subject, date))

                        vs.stop()
                        cv2.destroyAllWindows()

                        if cursor.fetchone():
                            messagebox.showinfo("Attendance", "Already Marked")
                        else:
                            cursor.execute("""
                            INSERT INTO attendance VALUES (?,?,?,?,?)
                            """, (roll, name, subject, date, current_time))
                            conn.commit()
                            messagebox.showinfo("Attendance", f"Marked: {name} ({roll})")

                        return

                    else:
                        vs.stop()
                        cv2.destroyAllWindows()
                        messagebox.showerror("Attendance", "Invalid Time")
                        return

            else:
                vs.stop()
                cv2.destroyAllWindows()
                messagebox.showerror("Error", "Face not recognized")
                return

        if cv2.waitKey(1) & 0xff == 27:
            break

    vs.stop()
    cv2.destroyAllWindows()

# GUI
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("400x400")

tk.Label(root, text="Face Recognition Attendance", font=("Arial", 16)).pack(pady=10)
tk.Label(root, text=f"Today: {today}", font=("Arial", 12)).pack(pady=5)

for subject in subjects:
    tk.Button(root, text=subject, width=25,
              command=lambda s=subject: start_attendance(s)).pack(pady=10)

# View attendance
def view_attendance():
    win = tk.Toplevel()
    win.title("Attendance Records")

    cursor.execute("SELECT * FROM attendance")
    rows = cursor.fetchall()

    for row in rows:
        tk.Label(win, text=str(row)).pack()

tk.Button(root, text="View Attendance", command=view_attendance).pack(pady=20)

root.mainloop()

#source venv311/bin/activate#