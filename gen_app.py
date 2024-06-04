import streamlit as st
import os
from google import generativeai as genai
import speech_recognition as sr
from dotenv import load_dotenv
import wave

# Load environment variables
load_dotenv()

# Configure the Generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# Function to generate response from the Generative AI model
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text 

# Function to recognize speech from audio
def recognize_speech():
    recognizer = sr.Recognizer()
    duration = 3  # Duration for recording in seconds

    # Record audio using the wave module
    with wave.open('temp_audio.wav', 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)

        # Placeholder for audio data
        audio_data = b'' 

        # Simulate audio recording (replace this with actual audio recording logic)
        # For example, you might capture audio from a microphone using a library like PyAudio
        # Here, we're just using a placeholder audio data
        # audio_data = YOUR_AUDIO_RECORDING_LOGIC_HERE

        wf.writeframes(audio_data)

    # Recognize speech using speech_recognition
    with sr.AudioFile('temp_audio.wav') as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

# Set Streamlit page configuration
st.set_page_config(page_title="Phoenix Lab's AI ASSISTANT: NADIA AI®", page_icon="🧠", layout='wide')

# Display header and logo
st.title("Phoenix Lab's AI ASSISTANT: NADIA AI®")
logo_path = 'logo.jpeg'
if os.path.exists(logo_path):
    st.image(logo_path, width=200)
else:
    st.warning("Logo image not found!")

# User input options
input_option = st.radio("Choose input method:", ('Text', 'Voice'))

if input_option == 'Text':
    input_text = st.text_input("Input: ")
    submit_button = st.button("GO")
    if submit_button:
        response = get_gemini_response(input_text)
        st.subheader("THE RESPONSE IS")
        st.write(response)
        
elif input_option == 'Voice':
    st.info("Please click the button below and speak clearly into your microphone.")
    record_button = st.button("Start Recording")
    if record_button:
        st.info("Recording... Speak now.")
        text_query = recognize_speech()
        st.write("Recognized Text: ", text_query)
        response = get_gemini_response(text_query)
        st.subheader("THE RESPONSE IS")
        st.write(response)

# Clean up temporary audio file
os.remove('temp_audio.wav')

# Health Check Endpoint
@st.cache
def health_check():
    return "OK"

if st.button("Check Health"):
    status = health_check()
    st.write("Health Check:", status)
