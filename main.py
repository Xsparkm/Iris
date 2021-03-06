import pyttsx3
import datetime
import speech_recognition as sr
import os
import json
import webbrowser
import wikipedia
import random
import akinator
import requests
import googletrans
from googletrans import Translator
translator = Translator()

from dotenv import load_dotenv
load_dotenv()

name = 'sparkm'
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices)
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour<=12:
        speak(f"Good Morning {name}! ")
    elif hour >=12 and hour <=18:
        speak(f"Good Afternoon {name}! ")
    else:
        speak(f"Good Evening {name}! ")
        
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        speak("listening") 
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        

    except Exception as e:
        speak("I was unable to recognize. Please say that again")
        print("I was unable to recognize. Please say that again")
        return "None"
    return query

def chatCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...") 
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        

    except Exception as e:
        speak("I was unable to recognize. Please say that again")
        print("I was unable to recognize. Please say that again")
        r.pause_threshold = 1
        audio = r.listen(source)
        speak('listening')

        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        speak(query)
    return query

if __name__=='__main__':
    wishme()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            query = query.replace('in wikipedia',"")
            query = query.replace('search for',"")
            out = wikipedia.summary(query, sentences=3)
            print(out)
            speak(f'According to wikipedia, {out}')
            
        elif 'stop the program' in query:
            speak("Ok! stopping the program")
            break    

        elif 'google' in query:
            query = query.replace('in google',"")
            query = query.replace('search for',"")
            speak(f"Searching for {query} in google")
            webbrowser.open(f'https://www.google.com/search?q={query}')
            
        elif 'youtube' in query:
            query = query.replace('in youtube',"")
            query = query.replace('search for',"")
            speak(f"Searching for {query} in youtube")
            webbrowser.open(f'https://www.youtube.com/results?search_query={query}')
        
        elif 'play rock paper scissors' in query:
            speak("Enter a choice (rock, paper, scissors): ") 
            user_action=takeCommand().lower()
            possible_actions = ["rock", "paper", "scissors"]
            computer_action = random.choice(possible_actions)
            speak(f"You chose {user_action}, computer chose {computer_action}.")

            if user_action == computer_action:
                speak(f"Both players selected {user_action}. It's a tie!")
            elif user_action == "rock":
                if computer_action == "scissors":
                    speak("Rock smashes scissors! You win!")
                else:
                    speak("Paper covers rock! You lose.")
            elif user_action == "paper":
                if computer_action == "rock":
                    speak("Paper covers rock! You win!")
                else:
                    speak("Scissors cuts paper! You lose.")
            elif user_action == "scissors":
                if computer_action == "paper":
                    speak("Scissors cuts paper! You win!")
            else:
                speak("Rock smashes scissors! You lose.")

        elif 'play akinator' in query:
            #try

            while True:
                aki = akinator.Akinator()
                speak(aki.start_game())
                q = aki.start_game()
                while aki.progression <= 80:
                    speak(q + "\n\t")   
                    a = takeCommand().lower()
                    if a == "b":
                        try:
                            q = aki.back()
                        except akinator.CantGoBackAnyFurther:
                            pass
                    else:
                        q = aki.answer(a)
                aki.win()

                speak(f"It's {aki.first_guess['name']} ({aki.first_guess['description']})! Was I correct?")
                correct = takeCommand().lower()
                if correct.lower() == "yes" or correct.lower() == "y":
                    speak("I won")
                else:
                    speak("you won")

        elif 'translate' in query:
            #this code provides the output but won't speak it, if you know the solution please dm me on discord : sparkm#5400
            speak('Which language would you like to translate to?')
            lang_to = takeCommand().lower()
            if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
                speak('Invalid Language.')
            else:                
                speak('Please say what you would like to translate')
                text = takeCommand().lower()
                translator = Translator()
                out = translator.translate(text, dest=lang_to)
                text_translated = translator.translate(text, dest=lang_to).text
                print(text_translated)
                speak(text_translated)

        elif 'chat mode' in query:
            speak('entering chat mode!')
            while True:
                message = chatCommand()
                url = "https://random-stuff-api.p.rapidapi.com/ai"
                Aut= os.getenv['Authorization']
                API_KEY= os.getenv['X-RapidAPI-Key']
                API_HOST = os.getenv['X-RapidAPI-Host']
                                

                querystring = {'msg': message,"bot_name":"Iris", "bot_name":"Iris","bot_gender":"female","bot_master":"sparkm","bot_age":"0","bot_birth_year":"2001","bot_birth_date":"8th June, 2022","bot_favorite_color":"Dark Blue","bot_favorite_artist":"TK" }
                headers = {
                    "Authorization": Aut,
                    "X-RapidAPI-Key": API_KEY,
                    "X-RapidAPI-Host": API_HOST
                }

                response = requests.request("GET", url, headers=headers, params=querystring)
                shush = response.json()
                out = shush["AIResponse"]
                print(out)



                speak(out)

 