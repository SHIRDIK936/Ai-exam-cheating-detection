import streamlit as st
import cv2
import mediapipe as mp
import pandas as pd
import time
import os
import numpy as np
from datetime import datetime
import base64
from ultralytics import YOLO  # ✅ NEW

# ---------------- UI ----------------
st.set_page_config(layout="wide")
st.title("🎓 AI Exam Cheating Detection System")

run = st.checkbox("Start Monitoring")

capture_btn = st.button("📸 Capture Face")
confirm_btn = st.button("✅ Confirm Register")
reset_btn = st.button("🔄 Reset Session")

# ---------------- YOLO MODEL ----------------
model = YOLO("yolov8n.pt")  # ✅ NEW

# ---------------- SESSION STORAGE ----------------
if "score_data" not in st.session_state:
    st.session_state.score_data = []

if "event_counts" not in st.session_state:
    st.session_state.event_counts = {
        "NO_FACE": 0,
        "MULTIPLE": 0,
        "HEAD_MOVE": 0,
        "IDENTITY": 0,
        "HIGH_SCORE": 0,
        "MOBILE": 0  # ✅ NEW
    }

if "focus_time" not in st.session_state:
    st.session_state.focus_time = 0

if "away_time" not in st.session_state:
    st.session_state.away_time = 0

if "exam_finished" not in st.session_state:
    st.session_state.exam_finished = False

# ---------------- RESET ----------------
if reset_btn:
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# ---------------- FILE SETUP ----------------
if not os.path.exists("evidence"):
    os.makedirs("evidence")

log_file = "logs.csv"

# ---------------- CAMERA ----------------
uploaded_file = st.file_uploader("📂 Upload Exam Video", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    with open("temp.mp4", "wb") as f:
        f.write(uploaded_file.read())

    cap = cv2.VideoCapture("temp.mp4")
else:
    st.warning("Please upload a video to start monitoring")
    st.stop()

# ---------------- FACE REGISTRATION ----------------
if "captured_image" not in st.session_state:
    st.session_state.captured_image = None

if capture_btn:
    ret, frame = cap.read()
    if ret:
        st.session_state.captured_image = frame
        st.success("Image Captured! Check below 👇")

if st.session_state.captured_image is not None:
    st.image(st.session_state.captured_image, channels="BGR", caption="Captured Face Preview")

if confirm_btn and st.session_state.captured_image is not None:
    cv2.imwrite("authorized.jpg", st.session_state.captured_image)
    st.success("✅ Face Registered Successfully!")
    st.session_state.captured_image = None

# ---------------- LOAD AUTH FACE ----------------
authorized = None
if os.path.exists("authorized.jpg"):
    authorized = cv2.imread("authorized.jpg")
    authorized = cv2.resize(authorized, (100, 100))

# ---------------- MEDIAPIPE ----------------
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(0.5)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# ---------------- SOUND ----------------
audio_base64 = None
if os.path.exists("alert.wav"):
    with open("alert.wav", "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode()

# ---------------- UI HOLDERS ----------------
frame_window = st.image([])
chart_placeholder = st.empty()
risk_placeholder = st.empty()
focus_placeholder = st.empty()

# ---------------- VARIABLES ----------------
score = 0
prev_risk = None
last_event = None

# ---------------- LOG FUNCTION ----------------
def save_log(event):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([[now, event, score]], columns=["Time","Event","Score"])

    if not os.path.exists(log_file):
        df.to_csv(log_file, index=False)
    else:
        df.to_csv(log_file, mode='a', header=False, index=False)

# ---------------- MAIN LOOP ----------------
while run:
    ret, frame = cap.read()
    if not ret:
        st.error("Camera error")
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    status = "Normal"

    # -------- FACE DETECTION --------
    result = face_detection.process(rgb)
    face_count = len(result.detections) if result.detections else 0

    if face_count == 0:
        score += 2
        status = "No Face"
        st.session_state.away_time += 1
    else:
        st.session_state.focus_time += 1

    if face_count > 1:
        score += 5
        status = "Multiple People 🚨"

    # -------- HEAD MOVEMENT --------
    mesh = face_mesh.process(rgb)
    if mesh.multi_face_landmarks:
        for lm in mesh.multi_face_landmarks:
            nose_x = int(lm.landmark[1].x * w)

            if nose_x < w * 0.4:
                score += 0.5
                status = "Looking Right"

            elif nose_x > w * 0.6:
                score += 0.5
                status = "Looking Left"

    # -------- AUTH CHECK --------
    if authorized is not None:
        face_small = cv2.resize(frame, (100, 100))
        diff = np.mean(cv2.absdiff(face_small, authorized))

        if diff > 50:
            score += 5
            status = "Different Person"

    # -------- OBJECT DETECTION (MOBILE) --------
    results = model(frame)

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2),
                          (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 255, 0), 2)

            if label == "cell phone":
                score += 5
                status = "Mobile Detected 🚨"

    # -------- RISK --------
    if score < 10:
        risk = "LOW"; color = "green"
    elif score < 20:
        risk = "MEDIUM"; color = "orange"
    else:
        risk = "HIGH"; color = "red"

    if risk != prev_risk:
        risk_placeholder.markdown(f"### Risk Level: :{color}[{risk}]")
        prev_risk = risk

    # -------- EVENT --------
    current_event = "NORMAL"

    if face_count == 0:
        current_event = "NO_FACE"
    elif face_count > 1:
        current_event = "MULTIPLE"
    elif status in ["Looking Left", "Looking Right"]:
        current_event = "HEAD_MOVE"
    elif status == "Different Person":
        current_event = "IDENTITY"
    elif status == "Mobile Detected 🚨":
        current_event = "MOBILE"
    elif score > 15:
        current_event = "HIGH_SCORE"

    # -------- ALERT --------
    if current_event != "NORMAL" and current_event != last_event:

        st.error(f"🚨 ALERT: {current_event}")

        filename = f"evidence/{datetime.now().strftime('%H%M%S')}.jpg"
        cv2.imwrite(filename, frame)

        save_log(current_event)
        st.session_state.event_counts[current_event] += 1

        if audio_base64:
            st.markdown(f"""
            <audio autoplay>
            <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
            </audio>
            """, unsafe_allow_html=True)

    if current_event == "NORMAL":
        last_event = None
    else:
        last_event = current_event

    # -------- FOCUS --------
    total_time = st.session_state.focus_time + st.session_state.away_time
    if total_time > 0:
        focus_percent = (st.session_state.focus_time / total_time) * 100
        focus_placeholder.markdown(f"### 🎯 Focus: {focus_percent:.1f}%")

    # -------- DISPLAY --------
    cv2.putText(frame, status, (20,50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    frame_window.image(frame, channels="BGR")

    # -------- GRAPH --------
    st.session_state.score_data.append(score)
    df = pd.DataFrame(st.session_state.score_data, columns=["Score"])
    chart_placeholder.line_chart(df)

    time.sleep(0.2)

cap.release()

# ---------------- STOP DETECT ----------------
if not run:
    st.session_state.exam_finished = True

# ---------------- SUMMARY ----------------
if st.session_state.exam_finished:

    st.subheader("📊 Exam Summary")

    total_alerts = sum(st.session_state.event_counts.values())
    max_score = max(st.session_state.score_data) if st.session_state.score_data else 0

    total_time = st.session_state.focus_time + st.session_state.away_time
    focus_percent = (st.session_state.focus_time / total_time * 100) if total_time > 0 else 0

    st.write(f"Total Alerts: {total_alerts}")
    st.write(f"Max Score: {int(max_score)}")
    st.write(f"Focus Score: {focus_percent:.1f}%")

    st.write("Violations:")
    for k, v in st.session_state.event_counts.items():
        st.write(f"{k}: {v}")
