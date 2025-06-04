# 🎥 Video Translator App

This is a simple Streamlit web application that allows users to **upload short videos**, **extract audio**, **translate subtitles**, and **display them with translated text**,with video.

> ✅ Built as part of an assignment for **Naventra**.

## 🚀 Features

- Upload a short video file (preferably under 20MB)
- Automatically extract audio
- Generate subtitles using speech recognition
- Translate subtitles to the selected language
- Display original + translated subtitles
- Easy-to-use Streamlit interface

## ⚠️ Limitations

- Currently supports **only small video files (under 20MB)** due to Streamlit file handling and memory limits.
- Large files may fail to process or cause performance issues.

## 🛠 Tech Stack

- 🐍 Python
- 🧠 `speech_recognition` for audio-to-text
- 🌐 `googletrans` for translation
- 📺 Streamlit for UI

## ▶️ How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/video-translator-app.git
   cd video-translator-app
2.  Create a virtual environment (recommended)
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3.  Install dependencies
    pip install -r requirements.txt
4.Run the app
    streamlit run app.py
📁 Folder Structure
css
Copy
Edit
video-translator-app/
├── app.py
├── requirements.txt
├── README.md
└── ...

📩 Assignment Submission Info
This project was submitted as part of the assignment.
Deployed version available at:
🌐 Streamlit App Link: https://vediotraslaterapp-nvfmfhkshbddm6tmhjfzsr.streamlit.app/

🙋‍♀️ Author
Kavyasri Kammari
AI Enthusiast | Developer
📧 Contact:kammarikavyasri11@gmail.com

 
