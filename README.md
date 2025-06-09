# 🎥 Video Translator App

This is a simple Streamlit web application that allows users to **upload short videos**, **extract audio**, **translate subtitles**, and **display them with translated text,with video**.


## 🚀 Features

- Upload a short video file (preferably under 20MB)
- Automatically extract audio
- Generate subtitles using speech recognition
- Translate subtitles to the selected language
- Display original + translated subtitles
- Easy-to-use Streamlit interface
- Use your own eleven labs api key


## ⚠️ Limitations

- Currently supports **only small video files (under 20MB)** due to Streamlit file handling and memory limits.
- Large files may fail to process or cause performance issues.

## 🛠 Tech Stack

- 🐍 Python
- 🎙️ `speech_recognition` – to convert audio to text
- 🌍 `deep_translator` – for translating subtitles
- 🗣️ `Eleven labs` – Google Text-to-Speech for generating translated audio
- 🎞️ `moviepy` – for audio extraction from video
- 🛠️ `ffmpeg` (via `ffmpeg-python`) – to merge video with translated audio
- 🌐 Streamlit – for building the interactive UI

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


🙋‍♀️ Author
Kavyasri Kammari
AI Enthusiast | Developer
📧 Contact:kammarikavyasri11@gmail.com

 
