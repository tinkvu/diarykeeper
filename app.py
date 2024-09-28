import streamlit as st
import datetime
import json
import os
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
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak now...")
        audio = r.listen(source)
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
    entry = st.text_area("Write your diary entry:", entries.get(date_str, ""))
else:
    if st.button("Start Recording"):
        entry = speech_to_text()
        st.write("Recorded text:", entry)
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
