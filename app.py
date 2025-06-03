import streamlit as st
from moviepy.editor import VideoFileClip
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
import ffmpeg

st.title("🎬 Multilingual Video Translator")

# Language mapping for translation & TTS
lang_map = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te"
}

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "mkv"])
language = st.selectbox("Choose language for translation", list(lang_map.keys()))

if uploaded_file and st.button("Translate & Generate Video"):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Save uploaded video temporarily
        video_path = os.path.join(tmpdir, uploaded_file.name)
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())

    
        # Extract audio from video
        video = VideoFileClip(video_path)
        audio_path = os.path.join(tmpdir, "extracted_audio.wav")
        video.audio.write_audiofile(audio_path, logger=None)
        video.close()  # Important: close the video file to release handle

        # Transcribe audio to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        try:
            transcript = recognizer.recognize_google(audio_data)
            st.text_area("Original Transcript", transcript, height=150)
        except Exception as e:
            st.error(f"Speech Recognition failed: {e}")
            st.stop()

        # Translate transcript to target language
        target_lang_code = lang_map[language]
        translated_text = GoogleTranslator(source='auto', target=target_lang_code).translate(transcript)
        st.text_area("Translated Text", translated_text, height=150)

        # Convert translated text to speech (mp3)
        tts = gTTS(text=translated_text, lang=target_lang_code)
        translated_audio_path = os.path.join(tmpdir, "translated_audio.mp3")
        tts.save(translated_audio_path)

        # Replace original audio with translated audio in the video using ffmpeg
        final_output_path = os.path.join(tmpdir, "translated_video.mp4")
        
        # Run ffmpeg process to merge video (without audio) and new audio
        input_video = ffmpeg.input(video_path)
        input_audio = ffmpeg.input(translated_audio_path)
        ffmpeg.output(input_video.video, input_audio.audio, final_output_path, vcodec='copy', acodec='aac', strict='experimental').run(overwrite_output=True)

        # Show success and download button
        st.success("✅ Video generated with translated audio.")
        with open(final_output_path, "rb") as f:
            st.download_button(
                label="Download Translated Video",
                data=f,
                file_name="translated_video.mp4",
                mime="video/mp4"
            )
