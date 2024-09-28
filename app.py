import streamlit as st
import datetime
import json
import os
from audio_recorder_streamlit import audio_recorder
import io
import speech_recognition as sr

# Function to load existing entries
def load_entries():
    if os.path.exists("diary_entries.json"):
        with open("diary_entries.json", "r") as f:
            return json.load(f)
    return {}

# Function to save entries
def save_entries(entries):
    with open("diary_entries.json", "w") as f:
        json.dump(entries, f)

# Function for speech recognition
def speech_to_text(audio_bytes):
    r = sr.Recognizer()
    with io.BytesIO(audio_bytes) as audio_file:
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
            try:
                text = r.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                st.error("Sorry, I couldn't understand that.")
            except sr.RequestError:
                st.error("Sorry, there was an error with the speech recognition service.")
    return ""

# Load existing entries
entries = load_entries()

st.title("My Personal Diary")

# Date selection
selected_date = st.date_input("Select a date", datetime.date.today())
date_str = selected_date.strftime("%Y-%m-%d")

# Entry input method selection
input_method = st.radio("Choose input method:", ("Type", "Record"))

if input_method == "Type":
    entry = st.text_area("Write your diary entry:", entries.get(date_str, ""), height=300)
else:
    st.write("Click the microphone icon below to start recording:")
    audio_bytes = audio_recorder()
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        st.write("Converting speech to text...")
        transcribed_text = speech_to_text(audio_bytes)
        st.write("Transcribed text:")
        entry = st.text_area("Edit your transcribed entry:", transcribed_text, height=300)
        st.info("You can edit the transcribed text above to correct any errors.")
    else:
        entry = entries.get(date_str, "")

# Save button
if st.button("Save Entry"):
    entries[date_str] = entry
    save_entries(entries)
    st.success("Entry saved successfully!")

# Display entries
st.subheader("Your Diary Entries")
for date, entry in sorted(entries.items(), reverse=True):
    with st.expander(date):
        st.write(entry) 
