import os
import time
import math
import threading
from collections import Counter

import cv2
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode

try:
    from deepface import DeepFace
    DEEPFACE_OK = True
except Exception:
    DEEPFACE_OK = False

try:
    from google import genai
    GEMINI_OK = True
except Exception:
    GEMINI_OK = False

st.set_page_config(page_title="MockMate AI", page_icon="🎤", layout="wide")

CUSTOM_CSS = """
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 1rem; max-width: 1400px;}
.main-title {
    font-size: 2.4rem; font-weight: 800; letter-spacing: -0.03em;
    background: linear-gradient(90deg, #06b6d4, #3b82f6 45%, #8b5cf6 85%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.subtle {color: #94a3b8; font-size: 0.98rem;}
.card {
    background: linear-gradient(180deg, rgba(17,24,39,.96), rgba(15,23,42,.92));
    border: 1px solid rgba(148,163,184,.16);
    border-radius: 18px; padding: 1rem 1.05rem; box-shadow: 0 10px 35px rgba(2,6,23,.25);
}
.metric-card {
    background: rgba(15,23,42,.78);
    border: 1px solid rgba(148,163,184,.14);
    border-radius: 16px; padding: .75rem .9rem;
}
.tag {
    display:inline-block; padding:.28rem .6rem; border-radius:999px;
    border:1px solid rgba(148,163,184,.2); margin-right:.35rem; margin-bottom:.35rem;
    font-size:.82rem; color:#e2e8f0; background:rgba(30,41,59,.7);
}
.mode-online {color:#22c55e; font-weight:700;}
.mode-offline {color:#f59e0b; font-weight:700;}
hr {border-color: rgba(148,163,184,.12);}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

QUESTIONS = [
    "Tell me about yourself.",
    "Why should we hire you for this role?",
    "Describe a project where you solved a difficult problem.",
    "What are your strengths and weaknesses?",
    "Tell me about a time you worked in a team under pressure.",
    "What makes you a strong fit for this opportunity?",
]

if "stats" not in st.session_state:
    st.session_state.stats = {
        "start_time": time.time(),
        "frames": 0,
        "face_detected_frames": 0,
        "distraction_count": 0,
        "smile_events": 0,
        "emotion_log": [],
        "confidence_log": [],
        "attention_log": [],
        "question_index": 0,
    }

if "feedback_text" not in st.session_state:
    st.session_state.feedback_text = None

class InterviewTransformer(VideoTransformerBase):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.last_face_center = None
        self.lock = threading.Lock()

    def _attention_score(self, face_center, frame_center, face_area, frame_area, moved_less):
        dx = abs(face_center[0] - frame_center[0]) / max(frame_center[0], 1)
        dy = abs(face_center[1] - frame_center[1]) / max(frame_center[1], 1)
        center_score = max(0, 100 - int((dx + dy) * 50))
        size_score = min(100, int((face_area / max(frame_area, 1)) * 500))
        stability_bonus = 15 if moved_less else 0
        return float(max(0, min(100, center_score + size_score + stability_bonus)))

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        stats = st.session_state.stats
        stats["frames"] += 1

        h, w, _ = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80))
        frame_center = (w // 2, h // 2)
        frame_area = w * h

        if len(faces) > 0:
            stats["face_detected_frames"] += 1
            x, y, fw, fh = max(faces, key=lambda b: b[2] * b[3])
            face = img[y:y+fh, x:x+fw]
            face_center = (x + fw // 2, y + fh // 2)

            moved_less = False
            if self.last_face_center is not None:
                moved_less = math.dist(face_center, self.last_face_center) < 15
            self.last_face_center = face_center

            attention = self._attention_score(face_center, frame_center, fw * fh, frame_area, moved_less)
            stats["attention_log"].append(attention)
            if attention < 40:
                stats["distraction_count"] += 1

            dominant_emotion = "neutral"
            confidence = 0.0
            if DEEPFACE_OK:
                try:
                    result = DeepFace.analyze(face, actions=['emotion'], enforce_detection=False, detector_backend='opencv')
                    if isinstance(result, list):
                        result = result[0]
                    dominant_emotion = result.get("dominant_emotion", "neutral")
                    confidence = float(max(result.get("emotion", {"neutral": 0}).values()))
                except Exception:
                    dominant_emotion = "neutral"
                    confidence = 0.0
            else:
                dominant_emotion = "deepface_missing"
                confidence = 0.0

            stats["emotion_log"].append(dominant_emotion)
            stats["confidence_log"].append(confidence)
            if dominant_emotion == "happy" and confidence > 60:
                stats["smile_events"] += 1

            cv2.rectangle(img, (x, y), (x + fw, y + fh), (34, 211, 238), 2)
            cv2.putText(img, f"{dominant_emotion} ({confidence:.1f}%)", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (56, 189, 248), 2)
            cv2.putText(img, f"Attention: {attention:.1f}", (x, y + fh + 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (250, 204, 21), 2)
        else:
            stats["distraction_count"] += 1
            cv2.putText(img, "No face detected", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (239, 68, 68), 2)

        cv2.putText(img, "MockMate AI — Real-time Interview Coach", (20, img.shape[0] - 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
        return img


def get_metrics(stats):
    avg_conf = float(np.mean(stats["confidence_log"])) if stats["confidence_log"] else 0.0
    avg_attention = float(np.mean(stats["attention_log"])) if stats["attention_log"] else 0.0
    dominant = Counter(stats["emotion_log"]).most_common(1)[0][0] if stats["emotion_log"] else "N/A"
    face_ratio = (stats["face_detected_frames"] / stats["frames"] * 100) if stats["frames"] else 0.0
    duration = time.time() - stats["start_time"]
    return avg_conf, avg_attention, dominant, face_ratio, duration


def local_feedback(stats, transcript, question):
    avg_conf, avg_attention, dominant, face_ratio, _ = get_metrics(stats)
    wc = len(transcript.split()) if transcript else 0
    feedback = []
    feedback.append(f"Question practiced: {question}")
    feedback.append(f"Dominant visible emotion: {dominant}")
    feedback.append(f"Average expression confidence: {avg_conf:.1f}%")
    feedback.append(f"Average attention score: {avg_attention:.1f}")
    feedback.append(f"Face presence ratio: {face_ratio:.1f}%")

    if avg_attention >= 70:
        feedback.append("You stayed centered well and looked engaged for most of the session.")
    elif avg_attention >= 45:
        feedback.append("Your attention looked decent, but reducing side glances would improve presence.")
    else:
        feedback.append("Your attention score was low; try to keep eye-line toward the camera and reduce movement.")

    if stats["distraction_count"] > 20:
        feedback.append("High distraction count suggests visible movement or frequent loss of framing.")
    elif stats["distraction_count"] > 8:
        feedback.append("Some distractions were detected; a steadier posture will help your delivery.")
    else:
        feedback.append("Your on-screen stability looked strong overall.")

    if dominant in ["happy", "neutral"]:
        feedback.append("Your visible expression appeared calm or approachable, which supports interview confidence.")
    elif dominant in ["fear", "sad", "angry", "disgust"]:
        feedback.append("Your visible expression looked tense at times; slower breathing and pacing may help.")

    if avg_conf < 35:
        feedback.append("Detection confidence stayed low often; improve front lighting and camera placement.")

    if wc < 20:
        feedback.append("Your answer looks short; try using Situation, Action, Result structure.")
    elif wc > 140:
        feedback.append("Your answer is long; tighter structure can make it sound sharper.")
    else:
        feedback.append("Your answer length looks balanced for a mock interview response.")

    feedback.append("This tool is for mock interview coaching and demo analytics, not hiring decisions.")
    return "\n".join([f"- {x}" for x in feedback])


def gemini_feedback(stats, transcript, question):
    if not GEMINI_OK or not os.getenv("GEMINI_API_KEY"):
        return None
    avg_conf, avg_attention, dominant, face_ratio, duration = get_metrics(stats)
    try:
        client = genai.Client()
        summary = f"""
Question: {question}
Transcript: {transcript}
Session duration: {duration:.1f} sec
Average emotion confidence: {avg_conf:.1f}
Average attention: {avg_attention:.1f}
Dominant emotion: {dominant}
Smile events: {stats['smile_events']}
Distraction count: {stats['distraction_count']}
Face presence ratio: {face_ratio:.1f}
"""
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=(
                "You are an interview coach. Analyze this mock interview session and give concise, practical feedback in markdown. "
                "Use these sections: Communication, Confidence, Non-verbal Signals, and 3 Actionable Tips. "
                "Do not overclaim emotion detection. Treat it as a practice aid only.\n\n"
                f"{summary}"
            )
        )
        return response.text
    except Exception:
        return None


def smart_feedback(mode, stats, transcript, question):
    if mode == "Smart Auto":
        online = gemini_feedback(stats, transcript, question)
        if online:
            return online, "Online AI Mode"
        return local_feedback(stats, transcript, question), "Offline Backup Mode"
    if mode == "Online AI":
        online = gemini_feedback(stats, transcript, question)
        if online:
            return online, "Online AI Mode"
        return local_feedback(stats, transcript, question), "Offline Backup Mode (auto fallback)"
    return local_feedback(stats, transcript, question), "Offline Backup Mode"


with st.sidebar:
    st.markdown("## ⚙️ Control Center")
    mode = st.radio("Feedback mode", ["Smart Auto", "Online AI", "Offline Backup"], index=0)
    current_q = st.selectbox(
        "Interview question",
        range(len(QUESTIONS)),
        format_func=lambda i: QUESTIONS[i],
        index=st.session_state.stats["question_index"]
    )
    st.session_state.stats["question_index"] = current_q

    st.markdown("### System status")
    st.write(f"DeepFace: {'✅ Ready' if DEEPFACE_OK else '❌ Missing'}")
    st.write(f"Gemini SDK: {'✅ Ready' if GEMINI_OK else '❌ Missing'}")
    st.write(f"API key: {'✅ Found' if os.getenv('GEMINI_API_KEY') else '⚠️ Not set'}")

    if st.button("Reset session", use_container_width=True):
        st.session_state.stats = {
            "start_time": time.time(),
            "frames": 0,
            "face_detected_frames": 0,
            "distraction_count": 0,
            "smile_events": 0,
            "emotion_log": [],
            "confidence_log": [],
            "attention_log": [],
            "question_index": 0,
        }
        st.session_state.feedback_text = None
        st.rerun()

st.markdown('<div class="main-title">MockMate AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtle">A polished mock interview assistant with live emotion analytics, confidence tracking, and a smart online/offline feedback toggle.</div>', unsafe_allow_html=True)

mode_badge = "mode-online" if (mode != "Offline Backup" and GEMINI_OK and os.getenv("GEMINI_API_KEY")) else "mode-offline"
status_text = "AI capable" if mode_badge == "mode-online" else "offline-safe"
st.markdown(f"<div class='tag'>OpenCV</div><div class='tag'>DeepFace</div><div class='tag'>Streamlit</div><div class='tag'>Smart Toggle</div><div class='tag {mode_badge}'>{status_text}</div>", unsafe_allow_html=True)

left, right = st.columns([1.5, 1])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎥 Live Interview View")
    webrtc_streamer(
        key="mockmate-webrtc",
        mode=WebRtcMode.SENDRECV,
        video_transformer_factory=InterviewTransformer,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧠 Interview Panel")
    question = QUESTIONS[st.session_state.stats["question_index"]]
    st.info(question)
    transcript = st.text_area("Answer / Transcript", height=220, placeholder="Paste transcript here or type the candidate response...")

    avg_conf, avg_attention, dominant, face_ratio, duration = get_metrics(st.session_state.stats)
    a, b = st.columns(2)
    c, d = st.columns(2)
    a.metric("Avg confidence", f"{avg_conf:.1f}%")
    b.metric("Avg attention", f"{avg_attention:.1f}")
    c.metric("Dominant emotion", dominant)
    d.metric("Face presence", f"{face_ratio:.1f}%")

    st.markdown(f"<div class='metric-card'>😊 Smile events: {st.session_state.stats['smile_events']}<br>⚠️ Distraction count: {st.session_state.stats['distraction_count']}<br>⏱️ Session duration: {duration:.1f} sec</div>", unsafe_allow_html=True)

    if st.button("Generate feedback", use_container_width=True):
        text, source_mode = smart_feedback(mode, st.session_state.stats, transcript, question)
        st.session_state.feedback_text = (text, source_mode)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("## 📊 Analytics Dashboard")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Frames processed", st.session_state.stats["frames"])
k2.metric("Faces seen", st.session_state.stats["face_detected_frames"])
k3.metric("Distractions", st.session_state.stats["distraction_count"])
k4.metric("Smiles", st.session_state.stats["smile_events"])

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Emotion distribution")
    if st.session_state.stats["emotion_log"]:
        counts = Counter(st.session_state.stats["emotion_log"])
        emotion_df = pd.DataFrame({"emotion": list(counts.keys()), "count": list(counts.values())}).sort_values("count", ascending=False)
        st.bar_chart(emotion_df.set_index("emotion"))
    else:
        st.caption("Emotion data will appear after webcam analysis begins.")
    st.markdown('</div>', unsafe_allow_html=True)

with chart_col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Attention trend")
    if st.session_state.stats["attention_log"]:
        att_df = pd.DataFrame({"attention": st.session_state.stats["attention_log"][-120:]})
        st.line_chart(att_df)
    else:
        st.caption("Attention trend will appear during the session.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("## 📝 Feedback")
st.markdown('<div class="card">', unsafe_allow_html=True)
if st.session_state.feedback_text:
    text, source_mode = st.session_state.feedback_text
    badge_class = "mode-online" if "Online" in source_mode else "mode-offline"
    st.markdown(f"**Source:** <span class='{badge_class}'>{source_mode}</span>", unsafe_allow_html=True)
    st.markdown(text)
else:
    st.caption("Generate feedback to see either Gemini-powered coaching or the local offline backup summary.")
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("🚀 Integration and run guide"):
    st.markdown("""
### Install
```bash
pip install -r requirements.txt
```

### Run
```bash
streamlit run app.py
```

### Optional online mode
Set your Gemini key only if you want AI feedback:
```bash
export GEMINI_API_KEY="your_key_here"
```

### Smart toggle logic
- **Smart Auto**: tries Gemini first, falls back to offline local feedback automatically.
- **Online AI**: prefers Gemini, but still falls back if key or tokens fail.
- **Offline Backup**: never touches API and always works locally.

### Best use in hackathon
Use this as a single polished feature page or as the main app for your mock interview demo.
""")
