import speech_recognition as sr
import pyttsx3
import pywhatkit
import pyautogui
import os
import time
import pygame   
import webbrowser
from datetime import datetime

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
    audio_file_path = "C:\\Users\\jordy\\OneDrive\\Documenten\\Project jarvis\\jarvis.mp3"
    
    pygame.init()
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()
    
    time.sleep(19)  # Play for 19 seconds
    pygame.quit()

main_music()

def End_music():
    audio_file_path = "C:\\Users\\jordy\\OneDrive\\Documenten\\Project jarvis\\end.mp3"
    
    pygame.init()
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()
    
    time.sleep(19)  # Play for 19 seconds
    pygame.quit()



def greeting_user():
    hour = datetime.now().hour
    if (hour >= 6)  and (hour < 12):
        talk('Good morning boss')
    elif (hour >=12) and (hour <16):
        talk('Good afternoon boss')
    elif (hour >= 16) and (hour <= 19):
        talk('Good evening boss')
    print("J.A.R.V.I.S.: Awaiting your call sir. ") 
    time.sleep(1)   
    talk('How can i assist you? ')   
greeting_user()


def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
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
                    
                    
                
                
                if 'start brawlhalla' in commandll:
                    os.startfile('E:\SteamLibrary\steamapps\common\Brawlhalla\BrawlhallaEAC.exe')
                    talk('Starting Brawlhalla')
                 
                if 'stop brawlhalla' in commandll:
                    talk('exiting brawlhalla')
                    os.system('taskill /IM BrawlhallaEAC.exe')
                     
                if 'start runescape' in commandll:
                    os.startfile('E:\SteamLibrary\steamapps\common\RuneScape\Bin\win64\RuneScape.exe')
                    talk('Starting RuneScape')
                
                if 'stop runescape' in commandll:
                    talk('exiting runescape')
                    os.system('taskkill /IM RuneScape.exe /F ')
                if 'start browser' in commandll:
                    talk('Starting Browser.')
                    webbrowser.open('https://www.google.com')
                
                if 'open ets2' in commandll:
                    os.startfile('C:\SteamLibrary\steamapps\common\Euro Truck Simulator 2\Bin\win_x64\eurotrucks2.exe')
                    talk('Starting Euro Truck Simulator 2')
                
                if 'stop ets2' in commandll:
                    talk('exiting Eurotruck simulator 2')
                    os.system('taskkill /IM eurotrucks2.exe /F ')

                if 'open cmd' in commandll:
                    talk('starting cmd sir')
                    os.system('start cmd')

                if 'start notepad' in commandll:
                    talk('Starting notepad')
                    os.startfile('C:\\WINDOWS\\system32\\notepad.exe')

                if 'stop notepad' in commandll:
                    talk('stopping notepad')
                    os.system('taskkill /IM notepad.exe /F ')    
                if 'start gta' in commandll:
                    talk("Starting gtav")
                    os.startfile('E:\GTAV\GTA5.exe')   

                if 'stop gta' in commandll:
                    talk('stopping Grand theft auto 5 ')
                    os.system('taskkill /IM GTA5.exe /F ')    

                if 'start for honor' in commandll:
                    talk('starting ForHonor')
                    os.startfile('E:\ForHonor\eac.Exe')
                
                if 'stop for honor' in commandll:
                    talk('exiting for honor')
                    os.system('taskkill /IM eac.Exe /F ')

                if 'start the isle' in commandll:
                    talk('starting the isle')
                    os.startfile('E:\SteamLibrary\steamapps\common\The Isle\TheIsle.exe')      

                if 'stop the isle' in commandll:
                    talk('exiting the isle')
                    os.system('taskkill /IM TheIsle.exe /F ')

                if 'start phasmophobia' in commandll:
                    talk('starting phasmophobia')
                    os.startfile('E:\SteamLibrary\steamapps\common\Phasmophobia\Phasmophobia.exe')   

                if 'stop phasmophobia' in commandll:
                    talk('exiting phasmophobia')
                    os.system('taskkill /IM Phasmophobia.exe /F ')         

                if 'start content manager' in commandll:
                    talk('starting content manager')
                    os.startfile('Downloads\Content Manager.exe') 

                if 'stop content manager' in commandll:
                    talk('exiting content manager')
                    if 'stop phasmophobia' in commandll:
                    talk('exiting phasmophobia')
                    os.system('taskkill /IM Content Manager /F ')    

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