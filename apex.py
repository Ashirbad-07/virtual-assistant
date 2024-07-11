import streamlit as st
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia

listener = sr.Recognizer()
machine = pyttsx3.init()

def talk(text):
    """Convert text to speech and output it."""
    st.write(f"Apex says: {text}")
    machine.say(text)
    machine.runAndWait()

def input_instruction():
    """Capture and process the voice command."""
    try:
        with sr.Microphone() as origin:
            listener.adjust_for_ambient_noise(origin)
            st.write("Listening...")
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech)
            st.write(f"Raw recognized instruction: {instruction}")  # Debug statement
            instruction = instruction.lower()
            if "apex" in instruction:  # Updated to check for "apex"
                instruction = instruction.replace('apex', '')
                st.write(f"Processed instruction: {instruction}")  # Debug statement
                return instruction.strip()
            else:
                st.write("Apex not mentioned in the instruction.")
                talk("You need to call me 'Apex' for me to respond.")
    except sr.UnknownValueError:
        st.write("Google Speech Recognition could not understand the audio.")
        talk("I didn't catch that. Please repeat.")
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")
        talk("There was an error with the speech recognition service.")
    except Exception as e:
        st.write(f"Exception: {e}")
        talk("I didn't catch that. Please repeat.")
    return ""

def execute_instruction(instruction):
    """Execute the given instruction."""
    if "play" in instruction:
        content = instruction.replace("play", "").strip()
        if "video" in content:
            video = content.replace("video", "").strip()
            talk("playing " + video + " on YouTube")
            pywhatkit.playonyt(video)
        else:
            talk("playing " + content + " on YouTube")
            pywhatkit.playonyt(content)
    elif 'time' in instruction:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'date' in instruction:
        date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk("Today's date is " + date)
    elif 'how are you' in instruction:
        talk('I am fine, how about you')
    elif 'what is your name' in instruction:
        talk('I am Apex, what can I do for you?')  # Updated response
    elif 'who is' in instruction:
        human = instruction.replace('who is', "").strip()
        info = wikipedia.summary(human, 1)
        st.write(info)
        talk(info)
    elif 'exit' in instruction or 'quit' in instruction:
        talk('Goodbye!')
        return False
    else:
        st.write(f"Instruction not recognized: {instruction}")
        talk('Please repeat')
    return True

def play_apex():
    """Main function to run the Apex assistant."""
    instruction = input_instruction()
    if instruction:
        st.write(f"Executing instruction: {instruction}")
        return execute_instruction(instruction)
    return True

if st.button('Start Apex'):
    while True:
        if not play_apex():
            break
