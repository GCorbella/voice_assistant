import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia


# listen microphone & turn audio as text
def trans_audio_to_text():

    # store recognizer in var
    r = sr.Recognizer()

    # config. microphone
    with sr.Microphone() as origin:

        # wait time
        r.pause_threshold = 0.4

        # record started info
        print("Record started")

        # save audio
        audio = r.listen(origin)

        try:
            # search in Google
            request = r.recognize_google(audio, language="en-en")

            # request info
            print("Info entered: " + request)

            # return request
            return request

        # if audio not recognizable
        except sr.UnknownValueError:

            # error info
            print("Not understood")

            # return error
            return "Still waiting"

        # if it can't resolve
        except sr.RequestError:

            # error info
            print("Couldn't  fulfill")

            # return error
            return "Still waiting"

        # unexpected error
        except:

            # error info
            print("Something went wrong")

            # return error
            return "Still waiting"


# function for the assistant to speak
def talk(message):

    # English voice
    id1 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

    # initialize pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("voice", id1)

    # pronounce message
    engine.say(message)
    engine.runAndWait()


# inform of the day of the week
def ask_day():

    # create var with today info
    day = datetime.date.today()

    # create var with weeks day
    week_day = day.weekday()

    # days name
    days_dict = {0: "Monday",
                 1: "Tuesday",
                 2: "Wednesday",
                 3: "Thursday",
                 4: "Friday",
                 5: "Saturday",
                 6: "Sunday"}

    # say day of the week
    talk(f"Today is {day}, {days_dict[week_day]}")


# inform hour
def ask_hour():

    # create hour data var
    moment = datetime.datetime.now()

    if moment.minute == 15:
        minutes = "a quarter"
    elif moment.minute == 30:
        minutes = "a half"
    elif moment.minute == 45:
        minutes = "three quarters"
    else:
        minutes = str(moment.minute) + "minutes"

    moment = f"In this moment is {moment.hour} and {minutes}"

    # say hour
    talk(moment)


# initial salute
def salute():

    # daytime var
    daytime = datetime.datetime.now()
    if 7 <= daytime.hour < 14:
        daytime_salute = "Good Morning"
    elif 14 <= daytime.hour < 20:
        daytime_salute = "Good Afternoon"
    elif daytime.hour >= 20:
        daytime_salute = "Good night"
    else:
        daytime_salute = "Good night"

    # salute
    talk(f"{daytime_salute}, I'm Zira, your virtual assistant. Please, tell me what can I do for you")


# principal function
def home():

    # salute
    salute()

    # exit var
    start = True

    # loop
    while start:

        # start microphone and cast request to str
        request = trans_audio_to_text().lower()

        if "open youtube" in request:
            talk("Of course, I'm opening YouTube")
            webbrowser.open("https://www.Youtube.com")
            continue

        elif "open the browser" in request:
            talk("Of course, I'm opening the browser")
            webbrowser.open("https://www.google.com")
            continue

        elif "what day is today" in request:
            ask_day()
            continue

        elif "what time is it" in request:
            ask_hour()
            continue

        elif "search in wikipedia" in request:
            talk("Searching in Wikipedia")
            request = request.replace("search in wikipedia", "")
            wikipedia.set_lang("en")
            result = wikipedia.summary(request, sentences=1)
            talk("Wikipedia says: ")
            talk(result)
            continue

        elif "search in google" in request:
            talk("Im on it")
            request = request.replace("search in google", "")
            pywhatkit.search(request)
            talk("This is what I've found")
            continue

        elif "play" in request:
            talk("Good idea, I'm starting to play it")
            request = request.replace("play", "")
            pywhatkit.playonyt(request)
            continue

        elif "joke" in request:
            talk(pyjokes.get_joke("en"))
            continue

        elif "stocks of" in request:
            stock = request.split("of")[-1].strip()
            wallet = {"apple": "APPL",
                      "amazon": "AMZN",
                      "google": "GOOGL"}
            try:
                w_stock = wallet[stock]
                w_stock = yf.Ticker(w_stock)
                price = w_stock.info["regularMarketPrice"]
                talk(f"I found it. The price of {stock} is {price}")
                continue
            except:
                talk("Sorry. I couldn't find it")
                continue

        elif "shutdown" in request:
            talk("I'm shutting down")
            break


home()
