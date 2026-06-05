# Attendance-System
# 📸 ESP32-CAM Attendance System

A real-time AI-based Face Recognition Attendance System using **ESP32-CAM + Python + OpenCV**.

---

## 🚀 Project Overview

This project captures live video from an **ESP32-CAM**, streams it over Wi-Fi, and processes it on a PC using **Python + OpenCV + face_recognition** library to automatically mark attendance.

---

## 🏗️ System Architecture

- ESP32-CAM captures live video
- Video stream sent via Wi-Fi
- Laptop/PC receives stream
- Python processes frames
- Face detection + recognition
- Attendance stored in CSV file

---

## ⚙️ Components Used

- ESP32-CAM module
- Wi-Fi Router / Mobile Hotspot
- Laptop / PC
- Python 3.x
- OpenCV
- face_recognition library

---

## 🔄 System Flow
ESP32-CAM → Wi-Fi Stream → Python OpenCV → Face Detection → Face Recognition → Attendance CSV

---

## 📊 Attendance CSV Format

| Name  | Date       | Time     | Status  |
|-------|-----------|----------|---------|
| Rohan | 23-05-2025 | 10:15:30 | Present |
| Sohan | 23-05-2025 | 10:15:45 | Present |

---

## 🧪 Working

1. ESP32-CAM powers ON and connects to Wi-Fi  
2. It starts video streaming  
3. Python script reads stream using OpenCV  
4. Faces are detected & compared with dataset  
5. If match found → Attendance marked in CSV  

---

## 🛠️ Installation

```bash
pip install opencv-python
pip install face_recognition
pip install numpy
