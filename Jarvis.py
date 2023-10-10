import speech_recognition as sr
import pyttsx3
import pywhatkit as kit 
import pyautogui
import os
import time
import pygame   
import webbrowser as wb
from datetime import datetime
import wikipedia
import xml.etree.ElementTree as ET
import subprocess
import threading
from pathlib import Path

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


# Plays the end intro when the program is started
def main_music():
    audio_file_path = ".\Sounds\JarvisStart.mp3"
    
    pygame.init()
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()
    
    time.sleep(19)  # Play for 19 seconds
    pygame.quit()

#main_music()

# Plays the end outro when the program is getting shutdowned by the shutdown command
def End_music():
    audio_file_path = ".\Sounds\JarvisEnd.mp3"
    
    pygame.init()
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()
    
    time.sleep(3)  # Play for 3 seconds
    pygame.quit()


# Used for making the settings class and is used for settings
xml_file_path = 'Settings.XML'
tree = ET.parse(xml_file_path)
root = tree.getroot()

class Settings:
    def __init__(self, name, toggleerrorprints):
        self.name = name
        self.toggleerrorprints = toggleerrorprints

user_obj = Settings(
    name=root.find('Name').text,
    toggleerrorprints=root.find('ToggleErrorPrints').text
)


class CustomCommand:
    def __init__(self, name, actions):
        self.name = name
        self.actions = actions

    def execute(self):
        threads = []
        for action in self.actions:
            try:
                thread = threading.Thread(target=lambda: eval(action))
                threads.append(thread)
                thread.start()
            except Exception as e:
                print(f"Error executing command '{self.name}': {str(e)}")


def load_custom_commands(xml_file_path):
    custom_commands = {}
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    for command in root.findall('command'):
        name = command.get('name')
        actions = [action.text for action in command.findall('action')]
        custom_commands[name] = CustomCommand(name, actions)

    return custom_commands


# Greeting the user on startup of the program
def greeting_user():
    hour = datetime.now().hour
    if hour >= 4  and hour < 12:
        talk(f'Good morning {user_obj.name}')
    elif hour >= 12 and hour < 16:
        talk(f'Good afternoon {user_obj.name}')
    elif hour >= 16 and hour < 24:
        talk(f'Good evening {user_obj.name}')
    print(f"J.A.R.V.I.S.: Awaiting your call {user_obj.name}. ") 
    time.sleep(1)   
    talk('How can I assist you? ')   
greeting_user()


def screenshot():
    img = pyautogui.screenshot()
    img.save(Path("Screenshots\Screenshot.png"))


def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            global command
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f'command = {command}')
            if name in command:
                command = command.replace('jarvis', '')
                if not 'wake up' in command and sleep_mode:
                    print('Asleep...')
                    pass
                else:
                    return command
    except sr.UnknownValueError:
        if user_obj.toggleerrorprints == 'True':
            print('Could not understand the audio')
        else:
            pass
    except sr.RequestError as e:
        if user_obj.toggleerrorprints == 'True':
            print(f'Speech recognition request failed: {str(e)}')
        else:
            pass

def takeCommand2():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")

    except Exception as e:
        print(e)
        talk("Please say that again")
        return "Try Again"

    return query



def run_jarvis():
    global sleep_mode
    sleep_mode = False

    custom_commands = load_custom_commands("CustomCommands.XML")
    
    while True:
        commandll = take_command()

        if sleep_mode:
            if commandll:
                if 'wake up' in commandll:
                    talk('I am now awake, how can I assist you?')
                    sleep_mode = False
        else:
            if commandll:

                custom_command_executed = False
                
                for command_name, action_obj in custom_commands.items():
                    if commandll.strip() == command_name:
                        print(f"Executing custom command: {command_name}")
                        action_obj.execute()
                        custom_command_executed = True
                        break
                if not custom_command_executed:
                    print("Command wasn't a custom command by user.")

                if 'play' in commandll:
                    song = commandll.replace('play', '')
                    talk('Playing ' + song)
                    kit.playonyt(song)

                if 'start google' in commandll:
                    talk('Starting Browser.')
                    wb.open('https://www.google.com') 

                if 'search on google' in  commandll:
                    talk(f'What do you want to search on Google, {user_obj.name}?')
                    query = takeCommand2().lower()
                    kit.search(query)

                if 'search on wikipedia' in commandll:
                    searchOnWikipediaCutOffText = command.replace('search on wikipedia', '')
                    try:
                        talk(f"Ok wait {user_obj.name}, Im searching...")
                        #commandll.replace('search on wikipedia', '')
                        print(searchOnWikipediaCutOffText)
                        result = wikipedia.summary(searchOnWikipediaCutOffText, sentences=2)
                        print(result)
                        talk(result)
                    except:
                        talk(f"Can't find this page {user_obj.name}, please ask about something else.")

                if 'please remember this for me' in commandll:
                    talk(f"What should I remember for you {user_obj.name}?")
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
                    talk(f'Shutting down {user_obj.name}.')
                    End_music()
                    break
        
if name == "jarvis":
    run_jarvis()