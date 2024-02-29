import speech_recognition as sr
import pyttsx3
import re
import wikipedia
import pywhatkit as pwk
import datetime
import json

def lisen(mic,r):
    try:
        with mic as source:
            print('Listening...')
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        i = r.recognize_google(audio)
    except:
        return "Audio Not Available"
    return i

def talk(text,engine):
    engine.say(text)
    engine.runAndWait()
    
dic = json.load(open('resource.json'))

mic = sr.Microphone()
r = sr.Recognizer()

#instruction = "send hi to you"
instruction = lisen(mic,r)
# print(instruction)

engine = pyttsx3.init()
engine.setProperty('volume',1.5)
engine.setProperty('rate',150)
v = engine.getProperty('voices')
engine.setProperty('voice',v[1].id)
# talk("hi",engine)

say = r"who are you"
search = r"search "
play = r"play "
send = r"send"

if search in instruction:
    se = re.split(search,instruction)[-1]
    # print("xdx " + se)
    title = wikipedia.search(se)
    # print(title[0])
    text = wikipedia.summary(title[1])
    print(text)
    talk(text,engine)

elif say in instruction:
    talk("I am Virtual Assistant",engine)

elif play in instruction:
    pl = re.split(play,instruction)[-1]
    pwk.playonyt(pl)

elif "time" in instruction:
    t = datetime.datetime.now().strftime('%H:%M:%S')
    talk("current time is "+t,engine)

elif "date" in instruction:
    d = datetime.datetime.now().strftime('%d %m %Y')
    d = d.replace(d.split()[1],dic['month'][d.split()[1]])
    talk("Today date is "+d,engine)

elif send in instruction:
    a = re.search(r"send (.*) to (.*)",instruction)
    msg = a.group(1)
    phone = a.group(2)
    pwk.sendwhatmsg_instantly(dic['contacts'][phone],msg)

elif "how are you" in instruction:
    talk('I am fine',engine)

elif "who is " in instruction:
    a = re.split(r"who is ",instruction)[-1]
    text = wikipedia.summary(a)
    talk(a,engine)
