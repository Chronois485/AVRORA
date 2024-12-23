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
language = 'uk'
your_name = "sir"
use_light_system = ""
music_link = "https://www.spotify.com/ua-uk/free/"
telegram_path = ""
telegram_online = ""

with open(".\\settings.txt") as open_file:
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
if use_light_system == "True\n":
    board = pyfirmata2.Arduino(PORT)
    try:
        try:
            file = open("setupPins.txt")
        except:
            print("Не знаєденно файлу з налаштуванням пінів")

        for line in file:
            line = line.split(",")
            pins.append(board.get_pin(line[0]))
        file.close()
    except:
        pass
print(f"                        AVRORA                            \n"
      f"Artificial Virtual Robot Optimized for Reliable Assistance")

StandartAns1 = gTTS(text=f"звісно {your_name}", lang=language, slow=False).save("s1.mp3")
StandartAns1 = gTTS(text=f"секунду {your_name}", lang=language, slow=False).save("s2.mp3")
StandartAns1 = gTTS(text=f"зараз {your_name}", lang=language, slow=False).save("s3.mp3")

print(
    f"\nПоточні налаштування:\n\nДо вас звертатися: {your_name}\nПосилання на музику: {music_link}\nШлях до телеграму: {telegram_path}\n\nВикористовувати телеграм в браузері: {telegram_online}\n\nВикористовувати систему світла: {use_light_system}\n")
ans = gTTS(text=f"Вітаю, {your_name}, всі системи активні", lang=language, slow=False)
ans.save("welcome.mp3")
data, fs = sf.read("welcome.mp3", dtype='float32')
sd.play(data, fs)


def command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Говоріть")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        task = r.recognize_google(audio, language="uk-in").lower()
    except:
        task = command()
    return task


def make_something():
    task = command()
    global run
    run = True
    if "аврора" in task[:6] or "aurora" in task[:6]:
        print(task)
        task = task[6:]
        if task != "" and task != " ":
            if "знайди" in task:
                task = task[6:]
                task.replace(" ", "+")
                webbrowser.open_new_tab(f"https://www.google.com/search?q={task}")
                ans = "standart"
            elif "відкрий youtube" in task:
                webbrowser.open_new_tab("https://www.youtube.com/")
                ans = "standart"
            #elif "відкрий vs code" in task or "открой vscode" in task:
            #    os.startfile(r'"F:\MYPROGRAMS\Microsoft VS Code\Code.exe"')
            #    ans = "standart"
            elif task == "відключись":
                run = False
                ans = gTTS(text=f"допобачення {your_name}", lang=language, slow=False)
            elif "відкрий telegram" in task:
                if telegram_online == "True\n":
                    webbrowser.open_new_tab(f"https://web.telegram.org/k/")
                    ans = "standart"
                else:
                    os.startfile(telegram_path)
                    ans = "standart"
            elif "музику" in task:
                webbrowser.open_new_tab(music_link)
                ans = "standart"
            elif "вимкни пк" in task:
                os.system("shutdown /s /t 5")
                ans = gTTS(text=f"вимикаю {your_name}", lang=language, slow=False)
            elif "дата" in task:
                current_datetime = datetime.now()
                dayOfWeek = current_datetime.weekday()
                if dayOfWeek == 0:
                    dayOfWeek = "понеділок"
                elif dayOfWeek == 1:
                    dayOfWeek = "вівторок"
                elif dayOfWeek == 2:
                    dayOfWeek = "середа"
                elif dayOfWeek == 3:
                    dayOfWeek = "четвер"
                elif dayOfWeek == 4:
                    dayOfWeek = "п'ятниця"
                elif dayOfWeek == 5:
                    dayOfWeek = "субота"
                elif dayOfWeek == 6:
                    dayOfWeek = "неділя"
                ans = gTTS(
                    text=f"{your_name}, сьогодні {dayOfWeek}, {current_datetime.day} , {current_datetime.month}, {current_datetime.year}",
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
            elif ("вимкни світло" in task) and use_light_system == "True\n":
                pins[10].write(0)
                ans = "standart"
            elif "увімкни світло" in task and use_light_system == "True\n":
                pins[10].write(0)
                time.sleep(0.5)
                pins[10].write(1)
                ans = "standart"
            elif "котра година" in task:
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

                ans = gTTS(
                    text=f"{your_name}, зараз {hour}, {minute}, {second}",
                    lang=language, slow=False)
            else:
                ans = gTTS(text="Не розумію", lang=language, slow=False)
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


def ask_gpt(promt: str) -> str:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo,
        messages=[{"role": "user", "content": promt}],
    )
    return response


make_something()
while run:
    make_something()
