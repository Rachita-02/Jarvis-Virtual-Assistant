import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests 
import json
from gtts import gTTS
from groq import Groq 
import pygame
import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("GROQ_API_KEY"))   
print(os.getenv("NEWS_API_KEY")) 

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = os.getenv("NEWS_API_KEY")

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    
    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 
    
def aiProcess(command):
    client = Groq(api_key=os.getenv("GROQ_API_KEY")) 

    completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a virtual assisstant named jarvis skilled in general task like alexa and gloogle cloud.Give short responses please"},
        {"role": "user", "content" : command}
    ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkdin" in c.lower():
        webbrowser.open("https://linkdin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link) 

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

                
    else:
        #let openai handles the request
        output = aiProcess(c)
        speak(output)
if __name__ == "__main__":
    speak("Initializing Jarvis...")
    
    while True:
    #listen for wake word jarvis     
    #obtain audio from something
        r = sr.Recognizer()

        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listning...")
                audio = r.listen(source, timeout=5, phrase_time_limit = 5)
            word = r.recognize_google(audio)

            if(word.lower() == "jarvis"):
                speak("Ya")
                
                #listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active..")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
    

        except Exception as e:
            print("Error,{0}".format(e))
