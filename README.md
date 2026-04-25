# 🎓 AI Exam Cheating Detection System

An advanced **AI-powered online exam monitoring system** that detects cheating behavior in real-time using **Computer Vision and Deep Learning**.

---

## 🚀 Overview

This project aims to solve the problem of **maintaining integrity in online examinations**.
It uses AI models to monitor students through a webcam and automatically detect suspicious activities.

The system continuously analyzes video frames and identifies:

* Absence from camera
* Multiple people in frame
* Head movement (looking away)
* Identity mismatch
* Mobile phone usage

It assigns a **cheating score**, generates **alerts**, and stores **evidence for review**.

---

## 🧠 Key Features

* 🎥 Real-time webcam monitoring
* 👤 Face detection using MediaPipe
* 🧍 Multiple person detection
* 🧠 Head movement tracking
* 🧑 Identity verification using image comparison
* 📱 Mobile detection using YOLOv8
* 🚨 Real-time alerts with sound
* 📊 Live cheating score graph
* 🎯 Focus percentage tracking
* 📸 Automatic evidence capture
* 📝 Event logging (CSV file)
* 📊 Final exam summary report

---

## 🛠️ Technologies Used

* **Python**
* **Streamlit** – UI Dashboard
* **OpenCV** – Webcam & image processing
* **MediaPipe** – Face detection & tracking
* **YOLOv8 (Ultralytics)** – Object detection (mobile phones)
* **NumPy** – Image comparison
* **Pandas** – Data logging & analysis

---

## 📂 Project Structure

```
AI-Exam-Monitor/
│
├── app.py               # Main application file
├── requirements.txt    # Dependencies
├── logs.csv            # Event logs (auto-generated)
├── authorized.jpg      # Registered face image
├── alert.wav           # Alert sound file
├── evidence/           # Stored cheating screenshots
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```
git clone https://github.com/your-username/AI-Exam-Monitor.git
cd AI-Exam-Monitor
```

---

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Run the Application

```
streamlit run app.py
```

---

## 🖥️ How the System Works

### 1. Face Registration

* User captures their face using webcam
* Image is stored as `authorized.jpg`

---

### 2. Live Monitoring

* Webcam continuously captures frames using OpenCV
* Each frame is processed by AI models

---

### 3. Detection Modules

#### 👤 Face Detection

* Detects if user is present or not
* No face → increases cheating score

#### 🧍 Multiple Person Detection

* Detects more than one face
* Indicates possible assistance

#### 🧠 Head Movement Tracking

* Tracks nose position using facial landmarks
* Detects if user is looking away

#### 🧑 Identity Verification

* Compares current face with registered face
* Detects impersonation

#### 📱 Mobile Detection

* Uses YOLOv8 to detect mobile phones
* Flags cheating if detected

---

## 📊 Scoring System

| Behavior         | Score |
| ---------------- | ----- |
| No Face Detected | +2    |
| Multiple People  | +5    |
| Looking Away     | +0.5  |
| Different Person | +5    |
| Mobile Detected  | +5    |

---

## 🚨 Risk Levels

| Score Range | Risk Level |
| ----------- | ---------- |
| < 10        | LOW        |
| 10–20       | MEDIUM     |
| > 20        | HIGH       |

---

## 🔔 Alert System

When suspicious activity is detected:

* 🚨 Alert message is displayed
* 📸 Screenshot is captured in `evidence/`
* 📝 Event is logged in `logs.csv`
* 🔊 Alert sound is played

---

## 📊 Output Dashboard

The system provides:

* 🎥 Live video feed
* 📊 Real-time score graph
* 🚦 Risk level indicator
* 🎯 Focus percentage
* ⚠️ Alert notifications

---

## 📈 Final Summary

After monitoring stops:

* Total alerts count
* Maximum cheating score
* Focus percentage
* Violation breakdown

---

## ⚠️ Limitations

* Webcam access may not work in cloud deployment
* Identity verification is basic (pixel comparison)
* Requires good lighting for accurate detection

---

## 🚀 Future Improvements

* Deep learning-based face recognition
* Eye tracking for better accuracy
* Audio cheating detection
* Cloud deployment with live webcam support
* Multi-user monitoring system

---

## 🎯 Use Cases

* Online exams (schools & colleges)
* Remote hiring tests
* Certification platforms
* Training assessments

---

## 👨‍💻 Author

**Shirdi.K**
B.Tech – AI/ML Student
Focused on building real-world AI applications

---

## ⭐ Conclusion

This project demonstrates how **AI and Computer Vision** can be used to automate exam monitoring, detect cheating behavior, and improve fairness in online assessments.

---
