import streamlit as st
from moviepy.editor import VideoFileClip
from deep_translator import GoogleTranslator
import speech_recognition as sr
import tempfile
import os
import ffmpeg
import librosa
import numpy as np
import requests

# ElevenLabs API
ELEVEN_API_KEY = "sk_a93dda7fd4b0b819d642ad5f160625fd8bd7f6c3a46b8cf1"
voice_map = {
    "male": "TxGEqnHWrfWFTfGW9XjX",     # Default male voice
    "female": "EXAVITQu4vr4xnSDxMaL"    # Default female voice
}

# Gender Detection using librosa pitch
def detect_gender_pitch(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    mean_pitch = np.nanmean(f0) if np.any(~np.isnan(f0)) else 0
    return "male" if mean_pitch < 160 else "female"

# ElevenLabs TTS
def elevenlabs_tts(text, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        temp_path = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name
        with open(temp_path, "wb") as f:
            f.write(response.content)
        return temp_path
    else:
        st.error(f"ElevenLabs TTS failed: {response.text}")
        return None

# Streamlit UI
st.set_page_config(page_title="🎬 ElevenLabs Video Translator", layout="centered")
st.title("🎬 Multilingual Video Translator with ElevenLabs Voice")

lang_map = {"English": "en", "Hindi": "hi", "Telugu": "te"}
uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "mkv"])
language = st.selectbox("Choose target language", list(lang_map.keys()))
gender_preference = st.radio("Select voice gender", ["Auto-detect", "Male", "Female"], horizontal=True)

if uploaded_file and st.button("Translate & Generate Video"):
    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = os.path.join(tmpdir, uploaded_file.name)
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())

        # Extract audio from video
        video = VideoFileClip(video_path)
        audio_path = os.path.join(tmpdir, "audio.wav")
        video.audio.write_audiofile(audio_path, logger=None)
        video.close()

        # Detect gender if auto
        if gender_preference == "Auto-detect":
            detected_gender = detect_gender_pitch(audio_path)
            st.info(f"Detected voice gender: {detected_gender.capitalize()}")
        else:
            detected_gender = gender_preference.lower()

        # Speech Recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)

        try:
            transcript = recognizer.recognize_google(audio_data)
            with st.expander("Original Transcript"):
                st.write(transcript)
        except Exception as e:
            st.error(f"Speech recognition failed: {e}")
            st.stop()

        # Translation
        target_lang = lang_map[language]
        try:
            translated_text = GoogleTranslator(source='auto', target=target_lang).translate(transcript)
            with st.expander("Translated Text"):
                st.write(translated_text)
        except Exception as e:
            st.error(f"Translation failed: {e}")
            st.stop()

        # TTS using ElevenLabs
        voice_id = voice_map[detected_gender]
        translated_audio_path = elevenlabs_tts(translated_text, voice_id)
        if not translated_audio_path:
            st.stop()

        # Merge audio + video
        final_output_path = os.path.join(tmpdir, "translated_output.mp4")
        try:
            input_video = ffmpeg.input(video_path)
            input_audio = ffmpeg.input(translated_audio_path)
            ffmpeg.output(input_video.video, input_audio.audio, final_output_path,
                          vcodec='copy', acodec='aac', strict='experimental').run(overwrite_output=True, quiet=True)
        except Exception as e:
            st.error(f"FFmpeg merge failed: {e}")
            st.stop()

        # Show & download
        st.success("✅ Translated video ready with gender-matched ElevenLabs voice!")
        st.video(final_output_path)
        with open(final_output_path, "rb") as f:
            st.download_button("⬇️ Download Final Video", data=f, file_name="translated_video.mp4", mime="video/mp4")
