from gtts import gTTS
import g4f
import speech_recognition as sr
import webbrowser
import sounddevice as sd
import soundfile as sf
import os
import random
from datetime import datetime

language = 'uk'
last_promts = list()
last_answers = list()
count_of_remembered_promts = 16
your_name = "sir"
show_promts = 0
terraria_path = ""
print(f"                        AVRORA                            \n"
      f"Artificial Virtual Robot Optimized for Reliable Assistance")
with open(".\\settings.txt") as open_file:
    for line in open_file:
        if line[:29] == "count_of_remembered_promts = ":
            count_of_remembered_promts = int(line[29:])
        elif line[:12] == "your_name = ":
            your_name = line[12:]
        elif line[:14] == "show_promts = ":
            show_promts = line[14:]
        elif line[:19] == "path_to_terraria = ":
            terraria_path = line[19:]

print(
    f"Поточні налаштування:\nКількість запам'ятовуємих промтів: {count_of_remembered_promts}\nДо вас звертатися: {your_name}")
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
        print(task)
    except:
        task = command()
    return task


def make_something():
    task = command()
    global run
    run = True
    standart_answer = ""
    r = random.randint(0, 3)

    if r == 0:
        standart_answer = f"звісно {your_name}"
    elif r == 1:
        standart_answer = f"секунду {your_name}"
    else:
        standart_answer = f"зараз {your_name}"
    if "аврора" in task[:6]:
        print(task)
        task = task[6:]
        if task != "" and task != " ":
            if "знайди" in task:
                task = task[6:]
                task.replace(" ", "+")
                webbrowser.open_new_tab(f"https://www.google.com/search?q={task}")
                ans = gTTS(text=standart_answer, lang=language, slow=False)
            elif "відкрий youtube" in task:
                webbrowser.open_new_tab("https://www.youtube.com/")
                ans = gTTS(text=standart_answer, lang=language, slow=False)
            elif "відкрий terraria" in task:
                os.startfile(terraria_path)
                ans = gTTS(text=standart_answer, lang=language, slow=False)
            elif "відкрий vs code" in task or "открой vscode" in task:
                os.startfile(r'C:\Users\matvii\AppData\Local\Programs\Microsoft VS Code\Code.exe')
                ans = gTTS(text=standart_answer, lang=language, slow=False)
            elif "вимкнись" in task:
                run = False
                ans = gTTS(text=f"допобачення {your_name}", lang=language, slow=False)
            elif "відкрий telegram" in task:
                os.startfile(r'C:\Program Files\WindowsApps\TelegramMessengerLLP.TelegramDesktop_5.2.3'
                             r'.0_x64__t4vj0pshhgkwm\Telegram.exe')
                ans = gTTS(text=standart_answer, lang=language, slow=False)
            elif "музику" in task:
                webbrowser.open_new_tab("https://soundcloud.com/matvij-kalinin/sets/playlist")
                ans = gTTS(text=standart_answer, lang=language, slow=False)
            elif "вимкни пк" in task:
                os.system("shutdown /s /t 15")
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
                webbrowser.open_new_tab("https://www.office.com/?auth=1")
                ans = gTTS(text=standart_answer, lang=language, slow=False)
            elif "котра година" in task:
                current_datetime = datetime.now()
                ans = gTTS(
                    text=f"{your_name}, зараз {current_datetime.hour}, {current_datetime.minute}, {current_datetime.second}",
                    lang=language, slow=False)
            else:
                promt = (f"Ти голосовий помічник AVRORA що розшифровується як Artificial Virtual Robot Optimized for "
                         f"Reliable Assistance,"
                         f"остані запити: {last_promts}, останні відповіді: {last_answers}, використовуй історію "
                         f"відповідей і запитів щоб відповісти на наступний запит якщо це потрібно також "
                         f"обов'язково відповідай коротко і формально і українською і не потрібно додавати "
                         f"форматування до"
                         f"тексту уяви, що пишеш у звичайному блокноті і звертайся до мене {your_name}, ось питання: "
                         f"{task}")
                if len(last_promts) < count_of_remembered_promts:
                    last_promts.append(task)
                else:
                    last_promts.pop(0)
                    last_promts.append(task)
                if len(last_answers) < count_of_remembered_promts:
                    last_answers.append(ask_gpt(task))
                else:
                    last_answers.pop(0)
                    last_answers.append(ask_gpt(task))
                ans = gTTS(text=ask_gpt(promt), lang=language, slow=False)
                if show_promts == "1":
                    print(f"Текущий промт: {promt}")
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
