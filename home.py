import streamlit as st
import io
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.title("Convert text to a speech in Swedish")

# Let the user choose the TTS engine
tts_engine = st.selectbox("Choose TTS Engine", options=["OpenAI", "gTTS"])

# Text input area
text_input = st.text_area("Enter text to convert to speech:", height=300)

if st.button("Generate Audio"):
    if not text_input.strip():
        st.warning("Please enter some text")
    else:
        if tts_engine == "OpenAI":
            # Using OpenAI TTS API
            # Ensure you have proper credentials and the experimental TTS API enabled
            from openai import OpenAI
            client = OpenAI(api_key=openai_api_key)  # Pass the API key

            # Define a temporary file path for the audio
            speech_file_path = Path("speech.mp3")
            response = client.audio.speech.create(
                model="tts-1",      # Update with your actual model name if different
                voice="shimmer",      # Update with your preferred voice
                input=text_input,
            )
            response.stream_to_file(speech_file_path)

            # Read the audio file as bytes
            audio_bytes = speech_file_path.read_bytes()

            st.audio(audio_bytes, format="audio/mp3")
            st.download_button(
                label="Download Audio",
                data=audio_bytes,
                file_name="speech.mp3",
                mime="audio/mp3"
            )

        else:
            # Using gTTS (Google Text-to-Speech)
            from gtts import gTTS
            tts = gTTS(text=text_input, lang="sv")  # Set language to Swedish ('sv')

            # Write the audio to an in-memory bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)

            st.audio(audio_buffer, format="audio/mp3")
            st.download_button(
                label="Download Audio",
                data=audio_buffer,
                file_name="speech.mp3",
                mime="audio/mp3"
            )
