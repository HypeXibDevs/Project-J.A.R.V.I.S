import speech_recognition as sr
import pyttsx3
import pywhatkit
import pyautogui
import os
import time
import pygame   
import webbrowser as wb
from datetime import datetime
import wikipedia
import pyautogui
from pathlib import Path
from PIL import Image, ImageGrab
import io
import ctypes

startlus = False
stoplus = False 

name = 'jarvis'
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def main_music():
    audio_file_path = ".\Sounds\JarvisStart.mp3"
    
    pygame.init()
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()
    
    time.sleep(19)  # Play for 19 seconds
    pygame.quit()

#main_music()

def End_music():
    audio_file_path = ".\Sounds\JarvisEnd.mp3"
    
    pygame.init()
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()
    
    time.sleep(3)  # Play for 3 seconds
    pygame.quit()


def greeting_user():
    hour = datetime.now().hour
    if hour >= 4  and hour < 12:
        talk('Good morning boss')
    elif hour >= 12 and hour < 16:
        talk('Good afternoon boss')
    elif hour >= 16 and hour < 24:
        talk('Good evening boss')
    print("J.A.R.V.I.S.: Awaiting your call sir. ") 
    time.sleep(1)   
    talk('How can i assist you? ')   
greeting_user()

def screenshot():
    img = pyautogui.screenshot()
    img.save(Path("Screenshots\Screenshot.png"))


def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            global command
            command = listener.recognize_google(voice)
            command = command.lower()
            if name in command:
                command = command.replace('jarvis', '')
                if not 'wake up' in command and sleep_mode:
                    print('asleep...')
                    pass
                else:
                    return command
    except sr.UnknownValueError:
        print('Could not understand the audio')
    except sr.RequestError as e:
        print(f'Speech recognition request failed: {str(e)}')

def takeCommand2():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(query)

    except Exception as e:
        print(e)
        speak("Please say that again")
        return "Try Again"

    return query

def run_jarvis():
    global sleep_mode
    sleep_mode = False

    while True:
        commandll = take_command()
        print(commandll)

        if sleep_mode:
            if commandll:
                if 'wake up' in commandll:
                    talk('I am now awake, how can I assist you?')
                    sleep_mode = False
        else:
            if commandll:
                if 'play' in commandll:
                    song = commandll.replace('play', '')
                    talk('Playing ' + song)
                    pywhatkit.playonyt(song)

                if 'start google' in commandll:
                    talk('Starting Browser.')
                    wb.open('https://www.google.com') 

                if 'search on wikipedia' in commandll:
                    searchOnWikipediaCutOffText = command.replace('search on wikipedia', '')
                    try:
                        talk("Ok wait sir, Im searching...")
                        #commandll.replace('search on wikipedia', '')
                        print(searchOnWikipediaCutOffText)
                        result = wikipedia.summary(searchOnWikipediaCutOffText, sentences=2)
                        print(result)
                        talk(result)
                    except:
                        talk("Can't find this page sir, please ask about something else.")

                if 'please remember this for me' in commandll:
                    talk("What should I remember for you sir?")
                    data = takeCommand2()
                    talk("You told me to remember:" + data)
                    print("You told me to remember:" + str(data))
                    remember = open("Data\Remember.txt", "w")
                    remember.write(data)
                    remember.close

                if 'do you remember anything for me' in commandll:
                    remember = open("Data\Remember.txt", "r")
                    talk("You told me to remember:" + remember.read())
                    print("You told me to remember:" + str(remember))
                    remember.close

                if 'take a screenshot' in commandll:
                    screenshot()
                    talk("I took a screenshot, go checck it out sir.")

                if ('shut down pc') in commandll:
                    talk('shutting down this pc')
                    os.system(' shutdown /s /t 10')
     
                if 'go to sleep' in commandll:
                    talk('Going to sleep. Wake me up with the command "Wake up".')
                    sleep_mode = True

                if 'shut down' in commandll:
                    talk('Shutting down boss.')
                    End_music()
                    break
        
if name == "jarvis":
    run_jarvis()