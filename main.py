from gtts import gTTS
import g4f
import speech_recognition as sr
import webbrowser
import sounddevice as sd
import soundfile as sf
import os
import random
import pyfirmata2
from datetime import datetime
import time

pins = list()
PORT = pyfirmata2.Arduino.AUTODETECT
language = "uk"
your_name = "sir"
use_light_system = ""
music_link = "https://www.spotify.com/ua-uk/free/"
telegram_path = ""
telegram_online = ""

with open("settings.txt") as open_file:
    for line in open_file:
        if line[:12] == "your_name = ":
            your_name = line[12:]
        elif line[:14] == "show_promts = ":
            show_promts = line[14:]
        elif line[:13] == "music_link = ":
            music_link = line[13:]
        elif line[:19] == "use_light_system = ":
            use_light_system = line[19:]
        elif line[:16] == "telegram_path = ":
            telegram_path = line[16:]
        elif line[:18] == "telegram_online = ":
            telegram_online = line[18:]
        elif line[:11] == "language = ":
            language = line[11:].replace("\n", "")

if use_light_system == "True\n":
    board = pyfirmata2.Arduino(PORT)
    try:
        try:
            file = open("setupPins.txt")
        except:
            if language == "uk":
                print("Не знайдено файлу з налаштуванням пінів")
            elif language == "en":
                print("No pin configuration file found")

        for line in file:
            line = line.split(",")
            pins.append(board.get_pin(line[0]))
        file.close()
    except:
        pass
print(f"                        AVRORA                            \n"
      f"Artificial Virtual Robot Optimized for Reliable Assistance")
if language == "uk":
    StandartAns1 = gTTS(text=f"звісно {your_name}", lang=language, slow=False).save("s1.mp3")
    StandartAns1 = gTTS(text=f"секунду {your_name}", lang=language, slow=False).save("s2.mp3")
    StandartAns1 = gTTS(text=f"зараз {your_name}", lang=language, slow=False).save("s3.mp3")
    print(f"\nПоточні налаштування:\n\nДо вас звертатися: {your_name}\nПосилання на музику: {music_link}\nШлях до Телеграму: {telegram_path}\n\nВикористовувати Телеграм в браузері: {telegram_online}\n\nВикористовувати систему світла: {use_light_system}\n")
elif language == "en":
    StandartAns1 = gTTS(text=f"Of course {your_name}", lang=language, slow=False).save("s1.mp3")
    StandartAns1 = gTTS(text=f"give me a second {your_name}", lang=language, slow=False).save("s2.mp3")
    StandartAns1 = gTTS(text=f"please wait {your_name}", lang=language, slow=False).save("s3.mp3")
    print(f"\nCurrent settings:\n\nTo contact you: {your_name}\nLink to music: {music_link}\nPath to Telegram: {telegram_path}\n\nUse Telegram in the browser: {telegram_online}\n\nUse the light system: {use_light_system}\n")
if language == "uk":
    ans = gTTS(text=f"Вітаю, {your_name}, всі системи активні", lang=language, slow=False)
elif language == "en":
    ans = gTTS(text=f"Hello, {your_name}, all systems are active", lang=language, slow=False)
ans.save("welcome.mp3")
data, fs = sf.read("welcome.mp3", dtype='float32')
sd.play(data, fs)


def command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        if language == "uk":
            print("Говоріть")
        elif language == "en":
            print("Talk")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        if language == "uk":
            task = r.recognize_google(audio, language="uk-in").lower()
        elif language == "en":
            task = r.recognize_google(audio, language="en-in").lower()
    except:
        task = command()
    return task


def make_something():
    task = command()
    global run
    run = True
    if "аврора" in task[:6] or "aurora" in task[:6]:
        print(task)
        task = task[7:]
        if task != "" and task != " ":
            if "знайди" in task or "search" in task:
                task = task[7:]
                task.replace(" ", "+")
                webbrowser.open_new_tab(f"https://www.google.com/search?q={task}")
                ans = "standart"
            elif "відкрий youtube" in task or "open youtube" in task:
                webbrowser.open_new_tab("https://www.youtube.com/")
                ans = "standart"
            #elif "відкрий vs code" in task or "открой vscode" in task:
            #    os.startfile(r'"F:\MYPROGRAMS\Microsoft VS Code\Code.exe"')
            #    ans = "standart"
            elif task == "до побачення" or "goodbye" in task:
                run = False
                if language == "uk":
                    ans = gTTS(text=f"до побачення {your_name}", lang=language, slow=False)
                elif language == "en":
                    ans = gTTS(text=f"goodbye {your_name}", lang=language, slow=False)
            elif "відкрий telegram" in task or "open telegram" in task:
                if telegram_online == "True\n":
                    webbrowser.open_new_tab(f"https://web.telegram.org/k/")
                    ans = "standart"
                else:
                    os.startfile(telegram_path)
                    ans = "standart"
            elif "музику" in task or "play music" in task:
                webbrowser.open_new_tab(music_link)
                ans = "standart"
            elif "вимкни пк" in task or "shut down pc" in task:
                os.system("shutdown /s /t 5")
                if language == "uk":
                    ans = gTTS(text=f"вимикаю {your_name}", lang=language, slow=False)
                elif language == "en":
                    ans = gTTS(text=f"turning it off {your_name}", lang=language, slow=False)
            elif "дата" in task or "what's the date" in task:
                current_datetime = datetime.now()
                dayOfWeek = current_datetime.weekday()
                if dayOfWeek == 0:
                    if language == "uk":
                        dayOfWeek = "понеділок"
                    elif language == "en":
                        dayOfWeek = "monday"
                elif dayOfWeek == 1:
                    if language == "uk":
                        dayOfWeek = "вівторок"
                    elif language == "en":
                        dayOfWeek = "tuesday"
                elif dayOfWeek == 2:
                    if language == "uk":
                        dayOfWeek = "середа"
                    elif language == "en":
                        dayOfWeek = "wednesday"
                elif dayOfWeek == 3:
                    if language == "uk":
                        dayOfWeek = "четвер"
                    elif language == "en":
                        dayOfWeek = "thursday"
                elif dayOfWeek == 4:
                    if language == "uk":
                        dayOfWeek = "п'ятниця"
                    elif language == "en":
                        dayOfWeek = "friday"
                elif dayOfWeek == 5:
                    if language == "uk":
                        dayOfWeek = "субота"
                    elif language == "en":
                        dayOfWeek = "saturday"
                elif dayOfWeek == 6:
                    if language == "uk":
                        dayOfWeek = "неділя"
                    elif language == "en":
                        dayOfWeek = "sunday"
                if language == "uk":
                    ans = gTTS(
                        text=f"{your_name}, сьогодні {dayOfWeek}, {current_datetime.day} , {current_datetime.month}, {current_datetime.year}",
                        lang=language, slow=False)
                elif language == "en":
                    ans = gTTS(
                        text=f"{your_name}, today is {dayOfWeek}, {current_datetime.day} , {current_datetime.month}, {current_datetime.year}",
                        lang=language, slow=False)
            elif "microsoft office" in task:
                webbrowser.open_new_tab("https://www.office.com/")
                ans = "standart"
            elif "gemini" in task:
                webbrowser.open_new_tab("https://gemini.google.com/?hl=uk")
                ans = "standart"
            elif "chat gpt" in task or "chatgpt" in task or "чат гпт" in task or "чат gpt" in task:
                webbrowser.open_new_tab("https://chatgpt.com")
                ans = "standart"
            elif ("вимкни світло" in task or "turn off lights" in task) and use_light_system == "True\n":
                pins[10].write(0)
                ans = "standart"
            elif ("увімкни світло" in task or "turn on lights" in task) and use_light_system == "True\n":
                pins[10].write(0)
                time.sleep(0.5)
                pins[10].write(1)
                ans = "standart"
            elif "котра година" in task or "what time is it" in task:
                current_datetime = datetime.now()
                hour = current_datetime.hour
                minute = current_datetime.minute
                second = current_datetime.second
                if int(hour) < 10:
                    hour = f"0{hour}"
                if int(minute) < 10:
                    minute = f"0{minute}"
                if int(second) < 10:
                    second = f"0{second}" 
                
                if language == "uk":
                    ans = gTTS(
                    text=f"{your_name}, зараз {hour}, {minute}, {second}",
                    lang=language, slow=False)
                elif language == "en":
                    ans = gTTS(
                    text=f"{your_name}, now {hour}, {minute}, {second}",
                    lang=language, slow=False)
            else:
                if language == "uk":
                    ans = gTTS(text="Не розумію", lang=language, slow=False)
                elif language == "en":
                    ans = gTTS(text="I dont understand", lang=language, slow=False)
            if ans == "standart":
                r = random.randint(0, 3)
                if r == 0:
                    data, fs = sf.read("s1.mp3", dtype='float32')
                elif r == 1:
                    data, fs = sf.read("s2.mp3", dtype='float32')
                else:
                    data, fs = sf.read("s3.mp3", dtype='float32')
            else:
                ans.save("sound.mp3")
                data, fs = sf.read("sound.mp3", dtype='float32')
            sd.play(data, fs)
            status = sd.wait()
        else:
            pass

make_something()
while run:
    make_something()
