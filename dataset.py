import cv2
import sqlite3

# === INPUT ===
face_id = input("Enter Student ID: ")
name = input("Enter Name: ")
roll = input("Enter Roll Number: ")

# === DATABASE ===
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM students WHERE id=?", (face_id,))
if cursor.fetchone():
    print("User already exists!")
    conn.close()
    exit()

# === CAMERA ===
cam = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

count = 0

# === STABILITY VARIABLES ===
prev_direction = ""
stable_count = 0
final_direction = ""

# Capture loop
while True:
    ret, img = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        # Draw rectangle
        cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)

        # === DIRECTION LOGIC ===
        cx = x + w // 2
        frame_center = img.shape[1] // 2
        threshold = 60  # dead zone

        if cx < frame_center - threshold:
            direction = "Turn Left"
        elif cx > frame_center + threshold:
            direction = "Turn Right"
        else:
            direction = "Look Straight"

        # === STABILITY LOGIC ===
        if direction == prev_direction:
            stable_count += 1
        else:
            stable_count = 0

        if stable_count > 8:
            final_direction = direction

        prev_direction = direction

        # === DISPLAY TEXT ===
        cv2.putText(img, f"Direction: {final_direction}", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

        cv2.putText(img, f"Samples: {count}/30", (10,60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

        # === SAVE ONLY WHEN STABLE ===
        if final_direction != "" and stable_count > 8:
            count += 1
            cv2.imwrite(f"dataset/User.{face_id}.{count}.jpg",
                        gray[y:y+h, x:x+w])

    cv2.imshow('Dataset Creator', img)

    # Stop when enough samples
    if count >= 30:
        break

    # Press ESC to exit
    if cv2.waitKey(1) & 0xff == 27:
        break

# === CLEANUP ===
cam.release()
cv2.destroyAllWindows()

# === INSERT INTO DATABASE ONLY IF IMAGES CAPTURED ===
if count >= 30:
    cursor.execute("INSERT INTO students VALUES (?, ?, ?)", (face_id, name, roll))
    conn.commit()
    print("Student added successfully!")
else:
    print("Dataset not complete. Student NOT added.")

conn.close()