import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
from datetime import datetime
import requests

engine = pyttsx3.init()
news_api = "63380b637c47484f93b0912351a119b6"


def speak(text):
    engine.say(text)
    engine.runAndWait()


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
    elif "time" in c.lower():
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")
    elif "date" in c.lower():
        today = datetime.today()
        current_date = today.strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api}"
        )
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            for article in articles:
                speak(article["title"])
    else:
        pass


if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    r = sr.Recognizer()
    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
                word = r.recognize_google(audio)
                if word.lower() == "jarvis":
                    speak("Hello! How can I help you?")
                    with sr.Microphone() as source:
                        print("Jarvis Active...")
                        audio = r.listen(source)
                        command = r.recognize_google(audio)
                        processCommand(command)
        except Exception as e:
            print(f"Error; {e}")
