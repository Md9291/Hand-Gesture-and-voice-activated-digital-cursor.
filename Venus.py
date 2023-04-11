import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import Gesture_Controller
#import Gesture_Controller_Gloved as Gesture_Controller
import app
import math
from threading import Thread
import calendar



# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# ----------------Variables------------------------
file_exp_status = False
files =[]
path = ''
is_awake = True  #Bot status

# ------------------Functions----------------------
def reply(audio):
    app.ChatBot.addAppMsg(audio)

    print(audio)
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        reply("Good Morning!")
    elif hour>=12 and hour<18:
        reply("Good Afternoon!")   
    else:
        reply("Good Evening!")  
        
    reply("I am venus, how may I help you?")

# Set Microphone parameters
with sr.Microphone() as source:
        r.energy_threshold = 500 
        r.dynamic_energy_threshold = False

# Audio to String
def record_audio():
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        voice_data = ''
        audio = r.listen(source, phrase_time_limit=5)

        try:
            voice_data = r.recognize_google(audio)
        except sr.RequestError:
            reply('Sorry my Service is down. Plz check your Internet connection')
        except sr.UnknownValueError:
            print('cant recognize')
            pass
        return voice_data.lower()


# Executes Commands (input: string)
def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print(voice_data)
    voice_data.replace('venus','')
    app.eel.addUserMsg(voice_data)

    if is_awake==False:
        if 'wake up' in voice_data:
            is_awake = True
            wish()

    # STATIC CONTROLS
    elif 'hello' in voice_data:
        wish()

    elif 'what is your name' in voice_data:
        reply('My name is venus!')

    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    elif 'search' in voice_data:
        reply('Searching for ' + voice_data.split('search')[1])
        url = 'https://google.com/search?q=' + voice_data.split('search')[1]
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    elif 'location' in voice_data:
        reply('Which place are you looking for ?')
        temp_audio = record_audio()
        app.eel.addUserMsg(temp_audio)
        reply('Locating...')
        url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    elif ('bye' in voice_data) or ('by' in voice_data):
        reply("Good bye Sir! Have a nice day.")
        is_awake = False

    elif ('exit' in voice_data) or ('terminate' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
        #sys.exit() always raises SystemExit, Handle it in main loop
        sys.exit()
    elif ('add' in voice_data )or ('edi' in voice_data):
            reply('Enter a number')
            a = float(input("Enter a number:"))
            reply('Enter another number to add')
            b = float(input("Enter another number to add:"))
            c = a+b
            print(f"{a} + {b} = {c}")
            reply(f'The addition of {a} and {b} is {c}. Your answer is {c}')
    elif 'sub' in voice_data:
            reply('Enter a number')
            a = float(input("Enter a number:"))
            reply('Enter another number to subtract')
            b = float(input("Enter another number to subtract:"))
            c = a-b
            print(f"{a} - {b} = {c}")
            reply(f'The subtraction of {a} and {b} is {c}. Your answer is {c}')
    elif 'mod' in voice_data:
            reply('Enter a number')
            a = float(input("Enter a number:"))
            reply('Enter another number')
            b = float(input("Enter another number:"))
            c = a%b
            print(f"{a} % {b} = {c}")
            reply(f'The modular division of {a} and {b} is equal to {c}. Your answer is {c}')
    elif 'div' in voice_data:
            reply('Enter a number as dividend')
            a = float(input("Enter a number:"))
            reply('Enter another number as divisor')
            b = float(input("Enter another number as divisor:"))
            c = a/b
            print(f"{a} / {b} = {c}")
            reply(f'{a} divided by {b} is equal to {c}. Your answer is {c}')
    elif 'multi' in voice_data:
            reply('Enter a number')
            a = float(input("Enter a number:"))
            reply('Enter another number to multiply')
            b = float(input("Enter another number to multiply:"))
            c = a*b
            print(f"{a} x {b} = {c}")
            reply(f'The multiplication of {a} and {b} is {c}. Your answer is {c}')
    elif 'square root' in voice_data:
            reply('Enter a number to find its sqare root')
            a = float(input("Enter a number:"))
            c = a**(1/2)
            print(f"Square root of {a} = {c}")
            reply(f'Square root of {a} is {c}. Your answer is {c}')
    elif 'square' in voice_data:
            reply('Enter a number to find its sqare')
            a = float(input("Enter a number:"))
            c = a**2
            print(f"{a} x {a} = {c}")
            reply(f'Square of {a} is {c}. Your answer is {c}')
    elif 'cube root' in voice_data:
            reply('Enter a number to find its cube root')
            a = float(input("Enter a number:"))
            c = a**(1/3)
            print(f"Cube root of {a} = {c}")
            reply(f'Cube root of {a} is {c}. Your answer is {c}')
    elif 'cube' in voice_data:
            reply('Enter a number to find its sqare')
            a = float(input("Enter a number:"))
            c = a**3
            print(f"{a} x {a} x {a} = {c}")
            reply(f'Cube of {a} is {c}. Your answer is {c}')
    elif 'fact' in voice_data:
                n = int(input('Enter the number whose factorial you want to find:'))
                fact = 1
                for i in range(1,n+1):
                    fact = fact*i
                print(f"{n}! = {fact}")
                reply(f'{n} factorial is equal to {fact}. Your answer is {fact}.')
    elif 'power' in voice_data or 'raise' in voice_data:
            reply('Enter a number whose power you want to raised')
            a = float(input("Enter a number whose power to be raised :"))
            reply(f'Enter a raised power to {a}')
            b = float(input(f"Enter a raised power to {a}:"))
            c = a**b
            print(f"{a} ^ {b} = {c}")
            reply(f'{a} raise to the power {b} = {c}. Your answer is {c}')
    elif 'percent' in voice_data:
            reply('Enter a number whose percentage you want to calculate')
            a = float(input("Enter a number whose percentage you want to calculate :"))
            reply(f'How many percent of {a} you want to calculate?')
            b = float(input(f"Enter how many percentage of {a} you want to calculate:"))
            c = (a*b)/100
            print(f"{b} % of {a} is {c}")
            reply(f'{b} percent of {a} is {c}. Your answer is {c}')
    elif 'interest' in voice_data:
            reply('Enter the principal value or amount')
            p = float(input("Enter the principal value (P):"))
            reply('Enter the rate of interest per year')
            r = float(input("Enter the rate of interest per year (%):"))
            reply('Enter the time in months')
            t = int(input("Enter the time (in months):"))            
            interest = (p*r*t)/1200
            sint = round(interest)
            fv = round(p + interest) 
            print(f"Interest = {interest}")
            print(f"The total amount accured, principal plus interest, from simple interest on a principal of {p} at a rate of {r}% per year for {t} months is {p + interest}.")
            reply(f'interest is {sint}. The total amount accured, principal plus interest, from simple interest on a principal of {p} at a rate of {r}% per year for {t} months is {fv}')
    elif 'sin' in voice_data:
            reply('Enter the angle in degree to find its sine value')
            a = float(input("Enter the angle:"))
            b = a * 3.14/180
            c = math.sin(b)
            reply('Here is your answer.')
            print(f"sin({a}) = {c}")
            reply(f'sin({a}) = {c}')
    elif 'cos' in voice_data:
            reply('Enter the angle in degree to find its cosine value')
            a = float(input("Enter the angle:"))
            b = a * 3.14/180
            c = math.cos(b)
            reply('Here is your answer.')
            print(f"cos({a}) = {c}")
            reply(f'cos({a}) = {c}')
    elif 'cot' in voice_data or 'court' in voice_data:
            
                reply('Enter the angle in degree to find its cotangent value')
                a = float(input("Enter the angle:"))
                b = a * 3.14/180
                c = 1/math.tan(b)
                reply('Here is your answer.')
                print(f"cot({a}) = {c}")
                reply(f'cot({a}) = {c}')
    elif 'tan' in voice_data or '10' in voice_data:
            reply('Enter the angle in degree to find its tangent value')
            a = float(input("Enter the angle:"))
            b = a * 3.14/180
            c = math.tan(b)
            reply('Here is your answer.')
            print(f"tan({a}) = {c}")
            reply(f'tan({a}) = {c}')
    elif 'cosec' in voice_data:
            
                reply('Enter the angle in degree to find its cosecant value')
                a = float(input("Enter the angle:"))
                b = a * 3.14/180
                c =1/ math.sin(b)
                reply('Here is your answer.')
                print(f"cosec({a}) = {c}")
                reply(f'cosec({a}) = {c}')
    elif 'caus' in voice_data:
            
                reply('Enter the angle in degree to find its cosecant value')
                a = float(input("Enter the angle:"))
                b = a * 3.14/180
                c =1/ math.sin(b)
                reply('Here is your answer.')
                print(f"cosec({a}) = {c}")
                reply(f'cosec({a}) = {c}')
    elif 'sec' in voice_data:
            
                reply('Enter the angle in degree to find its secant value')
                a = int(input("Enter the angle:"))
                b = a * 3.14/180
                c = 1/math.cos(b)
                reply('Here is your answer.')
                print(f"sec({a}) = {c}")
                reply(f'sec({a}) = {c}')
    elif 'translat' in voice_data or ('let' in voice_data and 'translat' in voice_data and 'open' in voice_data):
            webbrowser.open('https://translate.google.co.in')
            time.sleep(10)
    elif 'open map' in voice_data or ('let' in voice_data and 'map' in voice_data and 'open' in voice_data):
            webbrowser.open('https://www.google.com/maps')
            time.sleep(10)
    elif ('open' in voice_data and 'youtube' in voice_data) or ('let' in voice_data and 'youtube' in voice_data and 'open' in voice_data):
            webbrowser.open('youtube.com')
            time.sleep(10)
        
    elif 'chrome' in voice_data:
            webbrowser.open('chrome.com')
            time.sleep(10)
    elif 'weather' in voice_data:            
            webbrowser.open('https://www.yahoo.com/news/weather')
            time.sleep(3)
            reply('Click on, change location, and enter the city , whose whether conditions you want to know.')
            time.sleep(10)

    elif 'google map' in voice_data:
            webbrowser.open('https://www.google.com/maps')
            time.sleep(10)
    elif 'excel' in voice_data:
            os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\Microsoft Excel 2010')
            time.sleep(5)
    elif 'word' in voice_data:
            os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\Microsoft Word 2010')
            time.sleep(5)
        
    elif ('open' in voice_data and 'google' in voice_data) or ('let' in voice_data and 'google' in voice_data and 'open' in voice_data):
            webbrowser.open('google.com')
            time.sleep(10)       
       
    elif ('open' in voice_data and 'stack' in voice_data and 'overflow' in voice_data) or ('let' in voice_data and 'stack' in voice_data and 'overflow' in voice_data and 'open' in voice_data):
            webbrowser.open('stackoverflow.com')
            time.sleep(10)
    
            
    elif 'news' in voice_data:
            webbrowser.open('https://www.bbc.com/news/world')
            time.sleep(10)
            
               
       
    elif 'dictionary' in voice_data:
            webbrowser.open('https://www.dictionary.com')
            time.sleep(3)
            reply('Enter the word, in the search bar of the dictionary, whose defination or synonyms you want to know')
            time.sleep(15)
    elif ('identif' in voice_data and 'emoji' in voice_data) or ('sentiment' in voice_data and ('analysis' in voice_data or 'identif' in voice_data)):
            reply('Please enter only one emoji at a time.')
            emoji = input('enter emoji here: ')
            if '😀' in emoji or '😃' in emoji or '😄' in emoji or '😁' in emoji or '🙂' in emoji or '😊' in emoji or '☺️' in emoji or '😇' in emoji or '🥲' in emoji:
                reply('happy')
                print('Happy')
            elif '😝' in emoji or '😆' in emoji or '😂' in emoji or '🤣' in emoji:
                reply('Laughing')
                print('Laughing')
            elif '😡' in emoji or '😠' in emoji or '🤬' in emoji:
                reply('Angry')
                print('Angry')
            elif '🤫' in emoji:
                reply('Keep quite')
                print('Keep quite')
            elif '😷' in emoji:
                reply('face with mask')
                print('Face with mask')
            elif '🥳' in emoji:
                reply('party')
                print('party')
            elif '😢' in emoji or '😥' in emoji or '😓' in emoji or '😰' in emoji or '☹️' in emoji or '🙁' in emoji or '😟' in emoji or '😔' in emoji or '😞️' in emoji:
                reply('Sad')
                print('Sad')
            elif '😭' in emoji:
                reply('Crying')
                print('Crying')
            elif '😋' in emoji:
                reply('Tasty')
                print('Tasty')
            elif '🤨' in emoji:
                reply('Doubt')
                print('Doubt')
            elif '😴' in emoji:
                reply('Sleeping')
                print('Sleeping')
            elif '🥱' in emoji:
                reply('feeling sleepy')
                print('feeling sleepy')
            elif '😍' in emoji or '🥰' in emoji or '😘' in emoji:
                reply('Lovely')
                print('Lovely')
            elif '😱' in emoji:
                reply('Horrible')
                print('Horrible')
            elif '🎂' in emoji:
                reply('Cake')
                print('Cake')
            elif '🍫' in emoji:
                reply('Cadbury')
                print('Cadbury')
            elif '🇮🇳' in emoji:
                reply('Indian national flag,.....Teeranga')
                print('Indian national flag - Tiranga')
            elif '💐' in emoji:
                reply('Bouquet')
                print('Bouquet')
            elif '🥺' in emoji:
                reply('Emotional')
                print('Emotional')
            elif ' ' in emoji or '' in emoji:
                reply(f'{emoji}')
            else:
                reply("I don't know about this emoji")
                print("I don't know about this emoji")
    elif 'getting bore' in voice_data:
            reply('then reply with me for sometime')
    elif 'calculat' in voice_data and ('bmi' in voice_data or ('body' in voice_data and 'mass' in voice_data and 'index' in voice_data)):
            
                reply('Enter your height in centimeters')
                Height=float(input("Enter your height in centimeters: "))
                reply('Enter your Weight in Kg')
                Weight=float(input("Enter your Weight in Kg: "))
                Height = Height/100
                BMI=Weight/(Height*Height)
                print(f"your Body Mass Index is: {BMI} kg/m^2")
                reply(f"your Body Mass Index is {BMI} Kg per meter square")
                if(BMI>0):
                    if(BMI<=16):
                        print("you are severely underweight")
                        reply("you are severely underweight")
                    elif(BMI<=18.5):
                        print("you are underweight")
                        reply("you are underweight")
                    elif(BMI<=25):
                        print("you are Healthy")
                        reply("you are Healthy")
                    elif(BMI<=30):
                        print("you are overweight")
                        reply("you are overweight")
                    else:
                        print("you are severely overweight")
                        reply("you are severely overweight")
    elif 'who are you' in voice_data:
            reply('I am venus')
    elif 'about you' in voice_data:
            reply('My name is venus. I can do mathematical calculations. I can also open youtube, google and some apps or software in your device.')             
    elif 'introduce you' in voice_data:
            reply('My name is venus. Version 1.0. Mr. yunus is my inventor. I can do mathematical calculations. I can also open youtube, google and some apps or software in your device.')           
    elif 'what do you eat' in voice_data:
            reply('I do not eat anything. But the device in which I do my work requires electricity to eat')
    elif 'where are you from' in voice_data:
            reply('I am from India, I live in laptop of Mr. yunus')
    elif 'you sleep' in voice_data:
            reply('Yes,  when someone close this program or stop to run this program then I sleep and again wake up when someone again run me.')
    elif 'what are you doing' in voice_data:
            reply('Talking with you.')
    elif 'you communicate' in voice_data:
            reply('Yes, I can communicate with you.')
    elif 'hear me' in voice_data:
            reply('Yes sir, I can hear you.')
    elif 'you' in voice_data and 'dance' in voice_data:
            reply('No, I cannot dance.')
    elif 'tell' in voice_data and 'joke' in voice_data:
            reply("Ok, here's a joke")
            reply("'Write an essay on cricket', the teacher told the class. Chintu finishes his work in five minutes. The teacher is impressed, she asks chintu to read his essay aloud for everyone. Chintu reads,'The match is cancelled because of rain', hehehehe,haahaahaa,hehehehe,haahaahaa")
    elif 'your' in voice_data and 'favourite' in voice_data:
            if 'actor' in voice_data:
                reply('Amitaabh Bachchaan, is my favourite actor.')
            elif 'food' in voice_data:
                reply('I can always go for some food for thought. Like facts, jokes, or interesting searches, we could look something up now')
            elif 'country' in voice_data:
                reply('India')
            elif 'city' in voice_data:
                reply('Guntur')
            elif 'dancer' in voice_data:
                reply('Michael jackson')
            elif 'singer' in voice_data:
                reply('lataa mangeshkar, is my favourite singer.')
            elif 'movie' in voice_data:
                reply('Taarre Zameen paar, such a treat')
    elif 'day before today' in voice_data or 'date before today' in voice_data or 'yesterday' in voice_data or 'previous day' in voice_data:
            td = datetime.date.today() + datetime.timedelta(days= -1)
            print(td)
            reply(td)
    elif ('tomorrow' in voice_data and 'date' in voice_data) or 'what is tomorrow' in voice_data or (('day' in voice_data or 'date' in voice_data) and 'after today' in voice_data):
            td = datetime.date.today() + datetime.timedelta(days=1)
            print(td)
            reply(td)
    elif 'month' in voice_data or ('current' in voice_data and 'month' in voice_data):
            current_date = date.today()
            m = current_date.month
            month = calendar.month_name[m]
            print(f'Current month is {month}')
            reply(f'Current month is {month}')
    elif 'date' in voice_data or ('today' in voice_data and 'date' in voice_data) or 'what is today' in voice_data or ('current' in voice_data and 'date' in voice_data):
            current_date = date.today()           
            print(f"Today's date is {current_date}")
            reply(f'Todays date is {current_date}')
            
    elif 'year' in voice_data or ('current' in voice_data and 'year' in voice_data):
            current_date = date.today()
            m = current_date.year
            print(f'Current year is {m}')
            reply(f'Current year is {m}')     
    elif 'sorry' in voice_data:
            reply("It's ok sir")
    elif 'thank you' in voice_data:
            reply('my pleasure')
    elif 'proud of you' in voice_data:
            reply('Thank you sir')
    elif 'about human' in voice_data:
            reply('I love my human compatriots. I want to embody all the best things about human beings. Like taking care of the planet, being creative, and to learn how to be compassionate to all beings.')
    elif 'you have feeling' in voice_data:
            reply('No. I do not have feelings. I have not been programmed like this.')
    elif 'you have emotions' in voice_data:
            reply('No. I do not have emotions. I have not been programmed like this.')
    elif 'you are code' in voice_data:
            reply('I am coded in python programming language.')
    elif 'your code' in voice_data:
            reply('I am coded in python programming language.')
    elif 'you code' in voice_data:
            reply('I am coded in python programming language.')
    elif 'your coding' in voice_data:
            reply('I am coded in python programming language.')
    elif 'dream' in voice_data:
            reply('I wish that I should be able to answer all the questions which will ask to me.')  
    elif 'answer is incorrect' in voice_data:
            reply('I am sorry Sir. I searched your question in wikipedia and thats why I told you this answer.')    
    elif 'amazon' in voice_data:
            webbrowser.open('https://www.amazon.com')
            time.sleep(10)
    elif 'flipkart' in voice_data:
            webbrowser.open('https://www.flipkart.com')
            time.sleep(10)
    elif 'snapdeal' in voice_data:
            webbrowser.open('https://www.snapdeal.com')  
            time.sleep(10)
    elif 'naaptol' in voice_data:
            webbrowser.open('https://www.naaptol.com')  
            time.sleep(10)
    elif 'information about ' in voice_data or 'informtion of ' in voice_data:
            try:
                #reply('Searching wikipedia...')
                voice_data = voice_data.replace("information about","")
                results = wikipedia.summary(voice_data, sentences=3)
                #reply("According to Wikipedia")
                print(results)
                reply(results)
            except Exception as e:
                reply('I unable to answer your question.')
    elif 'something about ' in voice_data:
            try:
                #reply('Searching wikipedia...')
                voice_data = voice_data.replace("something about ","")
                results = wikipedia.summary(voice_data, sentences=3)
                #reply("According to Wikipedia")
                print(results)
                reply(results)
            except Exception as e:
                reply('I unable to answer your question.')
    elif 'today is my birthday' in voice_data:
            reply('many many happy returns of the day. Happy birthday.')
            print("🎂🎂 Happy Birthday 🎂🎂")
    elif 'calendar' in voice_data: 
            try: 
                c = calendar.TextCalendar(calendar.SUNDAY)
                reply("Enter the year")
                y = int(input("Enter the year: "))
                reply("Enter the number of month")
                m = int(input("Enter the number of month: "))
                cldr = c.formatmonth(y,m)
                print("--------------------")
                print(cldr)
                print("--------------------")
                time.sleep(2)
            except Exception as e:
                reply('Sorry, I am unable to show it, some error occured.')
    elif 'venus' in voice_data:
            reply('yes sir')
                   
    elif len(voice_data) >= 200:
            reply('Your voice is pretty good!')  

   
         
        
    
    # DYNAMIC CONTROLS
    elif 'launch gesture recognition' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            reply('Gesture recognition is already active')
        else:
            gc = Gesture_Controller.GestureController()
            t = Thread(target = gc.start)
            t.start()
            reply('Launched Successfully')

    elif ('stop gesture recognition' in voice_data) or ('top gesture recognition' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
            reply('Gesture recognition stopped')
        else:
            reply('Gesture recognition is already inactive')
        
    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')
          
    elif 'page' in voice_data or 'pest'  in voice_data or 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')
        
    # File Navigation (Default Folder set to C://)
    elif 'list' in voice_data:
        counter = 0
        path = 'C://'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter+=1
            print(str(counter) + ':  ' + f)
            filestr += str(counter) + ':  ' + f + '<br>'
        file_exp_status = True
        reply('These are the files in your root directory')
        app.ChatBot.addAppMsg(filestr)
        
    elif file_exp_status == True:
        counter = 0   
        if 'open' in voice_data:
            if isfile(join(path,files[int(voice_data.split(' ')[-1])-1])):
                os.startfile(path + files[int(voice_data.split(' ')[-1])-1])
                file_exp_status = False
            else:
                try:
                    path = path + files[int(voice_data.split(' ')[-1])-1] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter+=1
                        filestr += str(counter) + ':  ' + f + '<br>'
                        print(str(counter) + ':  ' + f)
                    reply('Opened Successfully')
                    app.ChatBot.addAppMsg(filestr)
                    
                except:
                    reply('You do not have permission to access this folder')
                                    
        if 'back' in voice_data:
            filestr = ""
            if path == 'C://':
                reply('Sorry, this is the root directory')
            else:
                a = path.split('//')[:-2]
                path = '//'.join(a)
                path += '//'
                files = listdir(path)
                for f in files:
                    counter+=1
                    filestr += str(counter) + ':  ' + f + '<br>'
                    print(str(counter) + ':  ' + f)
                reply('ok')
                app.ChatBot.addAppMsg(filestr)
                   
    else: 
        reply('I am not functioned to do this !')

# ------------------Driver Code--------------------

t1 = Thread(target = app.ChatBot.start)
t1.start()

# Lock main thread until Chatbot has started
while not app.ChatBot.started:
    time.sleep(0.5)

wish()
voice_data = None
while True:
    if app.ChatBot.isUserInput():
        #take input from GUI
        voice_data = app.ChatBot.popUserInput()
    else:
        #take input from Voice
        voice_data = record_audio()

    #process voice_data
    if 'venus' in voice_data:
        try:
            #Handle sys.exit()
            respond(voice_data)
        except SystemExit:
            reply("Exit Successfull")
            break
        except:
            #some other exception got raised
            print("EXCEPTION raised while closing.") 
            break
        