import cv2
import face_recognition
import os
import numpy as np
import pandas as pd
from datetime import datetime

# ===== ESP32-CAM STREAM URL =====
url = "http://172.20.10.3:81/stream"   # इथे तुझा IP टाक

# ===== LOAD KNOWN FACES =====
path = "faces"

images = []
classNames = []

for file in os.listdir(path):
    img = face_recognition.load_image_file(f"{path}/{file}")
    images.append(img)
    classNames.append(os.path.splitext(file)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        enc = face_recognition.face_encodings(img)
        if len(enc) > 0:
            encodeList.append(enc[0])
    return encodeList

encodeListKnown = findEncodings(images)

print("Faces Loaded:", classNames)

# ===== ATTENDANCE =====
csv_file = "attendance.csv"

if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=["Name", "Date", "Time"])
    df.to_csv(csv_file, index=False)

def markAttendance(name):
    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%H:%M:%S")

    df = pd.read_csv(csv_file)

    if not ((df["Name"] == name) & (df["Date"] == date)).any():
        new_row = {
            "Name": name,
            "Date": date,
            "Time": time
        }
        df = pd.concat([df, pd.DataFrame([new_row])],
                       ignore_index=True)
        df.to_csv(csv_file, index=False)
        print(f"Attendance Marked: {name}")

# ===== VIDEO STREAM =====
cap = cv2.VideoCapture(url)

while True:

    success, img = cap.read()

    if not success:
        print("Camera Not Connected")
        continue

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(
        imgS,
        facesCurFrame
    )

    for encodeFace, faceLoc in zip(encodesCurFrame,
                                   facesCurFrame):

        matches = face_recognition.compare_faces(
            encodeListKnown,
            encodeFace
        )

        faceDis = face_recognition.face_distance(
            encodeListKnown,
            encodeFace
        )

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:

            name = classNames[matchIndex].upper()

            y1, x2, y2, x1 = faceLoc

            y1 *= 4
            x2 *= 4
            y2 *= 4
            x1 *= 4

            cv2.rectangle(
                img,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                img,
                name,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            markAttendance(name)

        else:

            y1, x2, y2, x1 = faceLoc

            y1 *= 4
            x2 *= 4
            y2 *= 4
            x1 *= 4

            cv2.rectangle(
                img,
                (x1, y1),
                (x2, y2),
                (0, 0, 255),
                2
            )

            cv2.putText(
                img,
                "UNKNOWN",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

    cv2.imshow("ESP32-CAM Attendance System", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()