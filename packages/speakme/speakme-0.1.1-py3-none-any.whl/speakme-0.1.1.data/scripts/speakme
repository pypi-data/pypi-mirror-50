import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib # packge use to send an email from gmail, default intalled with python setup

from selenium import webdriver
driver = webdriver.Chrome("H:/Downloads/chromedriver.exe")

#-------------------------------------------#


import pandas as pd
import numpy as np

credits_df = pd.read_csv("H:/Machine Learning/Recommendation System/tmdb_5000_credits_list.csv")
movies_df = pd.read_csv("H:/Machine Learning/Recommendation System/tmdb_5000_movies_list.csv")


credit_column_rename = credits_df.rename(columns={"movie_id":"id"} )
movies_df_merge = movies_df.merge(credit_column_rename, on='id')

movies_df_clean = movies_df_merge.drop(['homepage', 'title_x','title_y','production_companies'], axis=1)

from sklearn.feature_extraction.text import TfidfVectorizer


tfv = TfidfVectorizer(min_df=3,  max_features=None, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3),
            stop_words = 'english')

# Filling NaNs with empty string
movies_df_clean['overview'] = movies_df_clean['overview'].fillna('')

tfv_matrix = tfv.fit_transform(movies_df_clean['overview'])


from sklearn.metrics.pairwise import sigmoid_kernel

# Compute the sigmoid kernel
sig = sigmoid_kernel(tfv_matrix, tfv_matrix)

# Reverse mapping of indices and movie titles
indices = pd.Series(movies_df_clean.index, index=movies_df_clean['original_title']).drop_duplicates()

#---------------------------------------------------#

def recommend_movies(title, sig=sig):
    # Get the index corresponding to original_title
    idx = indices[title]

    # Get the pairwsie similarity scores 
    sig_scores = list(enumerate(sig[idx]))

    # Sort the movies 
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    # Scores of the 10 most similar movies
    sig_scores = sig_scores[1:11]

    # Movie indices
    movie_indices = [i[0] for i in sig_scores]

    # Top 10 most similar movies
    return movies_df_clean['original_title'].iloc[movie_indices]
		

#-------------------------------------------#
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio) # 'audio' as a string speeks by 'engine' here
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour) # getting current hour i.e time and we typecast it in int for further calculations
    
    if hour>=0 and hour<12:
        speak("Good Morning!!")
    elif hour>=12 and hour<16:
        speak("Good Afternoon!!")
    elif hour>=16 and hour<20:
        speak("Good Evening!!")
    else:
        speak("Good Night!!") 

    speak("Welcome ........this is speakme personal assistance system and my name is MARKOS . Please tell me how may I help you ?")       

def takeCommand():
    # receives input from microphone and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        speak("You need anything sir...i am waiting")  
        return "None"
    return query

def sendEmail(to, content): # first search on google  "Less secured apps in gmail" >> enable it then it will work
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('tejasjbhor@gmail.com', 'put_your_password_here')
    server.sendmail('tejasjbhor@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()

        # based on query varibale we can write our own logic
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            
            results = wikipedia.summary(query, sentences=2)
            
            speak("According to Wikipedia")
            print(results)
            speak(results)
            
        elif 'weather' in query:
            speak("which city sir!")
            city = takeCommand()
            
            driver.get("https://www.weather-forecast.com/locations/"+city+"/forecasts/latest")

            forcast=driver.find_elements_by_class_name("b-forecast__table-description-content")[0].text 
            
            # Note - since ther are muliple elements with same class (as its is having arry of elements and we need first element of that class ), 
            #we need to pass their index to get correct containt from site hence >> [0]
            
            print(forcast)
            speak(forcast)
            

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            speak("youtube opened !")

        elif 'open google' in query:
            webbrowser.open("google.com")
            speak("google opened !")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")  
            speak("stack overflow opened !")
            
        elif 'open tencent ' in query:
            sudyapubg = "C:\Program Files (x86)\Microsoft Power BI Desktop\bin\PBIDesktop.exe"
            os.startfile(sudyapubg)
            speak("Great choice sir!......i do like it ...here you go")

        elif 'play music' in query:
            music_dir = 'H:\Pictures\songs'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0])) # play first song 
            speak("Song started sir !")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")
            

        elif 'movies' in query:
            speak("Which movie did you seen recently sir ?......")
            movie = takeCommand()
            speak("Hmmmmmm.."+movie+"Great choice sir!.....i would like to recommend similer movies if you want ")
            
            query = query.replace("movies", "")
            
        elif 'go ahead' in query:
            movies_df_clean['recomandation'] = recommend_movies(movie)
            movies_df_clean=movies_df_clean[movies_df_clean.recomandation.notnull()]
            rec_list = movies_df_clean['recomandation'].to_string(index=False)
            print(rec_list)   
            #print(recommend_movies(movie))
            speak("so ...these are few suggestions like "+rec_list+" ...thats all..did you like it ?")
            
            query = query.replace("go ahead", "")
            
        elif 'yes' in query:
            speak("Great sir !....Enjoy Then")   
            
        elif 'no need i am fine' in query:
            speak("As your wish sir !...bye")    
                
            
        elif 'open code' in query:
            
            codePath1 = "C:\ProgramData\Anaconda3\pythonw.exe"
            #codePath2 = "C:\ProgramData\Anaconda3\cwp.py"
            #codePath3 = "C:\ProgramData\Anaconda3 C:\ProgramData\Anaconda3\pythonw.exe" 
            #codePath4 = "C:\ProgramData\Anaconda3\Scripts\anaconda-navigator-script.py"
                
            os.startfile(codePath1)
            #os.startfile(codePath2)
            #os.startfile(codePath3)
            #os.startfile(codePath4)

        elif 'email me' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "tejasjbhor@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry... I am not able to send this email")  
                
        elif 'no thanks' in query:
            current_time = int(datetime.datetime.now().hour)
            if current_time>=0 and current_time<12:
                speak("ok...Have a great day sir!")
            elif current_time>=12 and current_time<16:
                speak("I am here to help you anytime...Enjoy your afternoon sir!...BYE")
            elif current_time>=16 and current_time<20:
                speak("Have great Evening sir!!")
            else:
                speak("Take care...Good night ..and ..sleep well!!")
            break
