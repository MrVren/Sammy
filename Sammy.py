'''
Sammy Voice Assistant v0.03

Установленные голоса (RU):  Anna
                            Arina
                            Elena
                            Irina
                            Tatiana
                            Victoria

Комментарии пишу для себя, т.к. не думаю что это вообще кто-либо увидит
'''
import os
import time
import datetime
import spotipy
import winsound
import wikipedia
import webbrowser as wb
import pyglet
from fuzzywuzzy import fuzz                                                 # модуль для распознавания нечетких сравнений
from plyer import notification                                              # просто чтоб не срать принтами в консоли
import speech_recognition as sr                                             # модуль распознавания речи
import pyttsx3                                                              # модуль отвечающий за перевод текста в речь

vocab = {                                                                   # словарь. эти слова саманта запомнит
        "alias":               ('cаманта ', 'cэмми ', 'cэм '),              # обращения к саманте
        "toBeRemoved":         ('скажи', 'расскажи', 'покажи',              # эти слова мы убираем из ответа
                                'сколько', 'произнеси', 'привет', 'ты знаешь', 'ты'), 
        "cmds": {                                                           # Словарь команд по группам
                "currentTime": ('время', 'времени', 'час'), 
                "dia1":        ('Что нам делать'), 
                "dia2":        ('как же так ничего'), 
                "dia3":        ('Жестокие слова'), 
                "whoAmI":      ('узнала меня', 'кто я'), 
                #"wikiRequet":  ('кто такой', 'найди человека', 'что такое'), 
                "playMusic":   ('включи музыку', 'музычку',                 # потребуется запущенный плеер (Spotify в моем случае)
                                'как-то здесь скучно'), 
                "stopMusic":   ('останови', 'тихо'), 
                #"openWeb":     ('открой браузер', 'открой оперу'), 
                #"openLinkVK":  ('открой вк'), 
                "exitApp":     ('отдохни', 'не подслушивай')

                }
        }



def show_notification(title, message):                                      # функция вывода уведомлений
        notification.notify(title = title, 
                            message = message, 
                            app_icon = ".\icon.ico", 
                            timeout = 5)

def talk(text):
    voice_engine.say(text)
    voice_engine.runAndWait()


def recognize_cmd(task):                                                     # поиск нечетких команд
    RC = {'task': '', 'percent': 0}
    for c, v in vocab['cmds'].items():
        for x in v:
            vrt = fuzz.ratio(task, x)
            if vrt > RC['percent']:
                RC['task'] = c
                RC['percent'] = vrt
                print(RC)
    return RC

def execute_cmd(_task):
    print(_task)
    if _task == 'currentTime':
        now = datetime.datetime.now()
        talk("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif _task == 'openWeb':
        talk("Хорошо")
        wb.open('/')

    elif _task == 'openLinkVK':
        talk("Хорошо")
        wb.get('windows-default').open('https://vk.com')

    elif _task == 'whoAmI':
        talk("Вы мой создатель, человек, благодаря которому я живу и учусь")


    elif _task == 'exitApp':
        os.system('shutdown -p')
        exit()
    # не реагирует, надо колдовать с обрезкой запроса
    elif _task == 'wikiRequest':
        result = wikipedia.summary(_task, sentences = 1)
        print(result)
        talk(result)

    elif _task == 'playMusic':
        music = pyglet.resource.media('track.mp3')
        music.play()
        pyglet.app.run()
        return

    elif _task == 'stopMusic':
        pyglet.app.exit()

    else: show_notification("Саманта", "Я не расслышала\nПовтори пожалуйста")
    print('Конец задачи')


voice_engine = pyttsx3.init()
voices = voice_engine.getProperty('voices')
voice_engine.setProperty('voice', 'ru')
wb.register('opera-gx', None, wb.BackgroundBrowser('C:/Users/Neophyte/AppData/Local/Programs/Opera GX/opera.exe'))

for voice in voices:                                                        # устанавливаем желаемый голос
    if voice.name == 'Victoria':                                            # для изменения просто смени имя в кавычках
        voice_engine.setProperty('voice', voice.id)
        show_notification("Саманта", "Голосовой движок запущен\nC тобой говорит " + voice.name)

# talk("Привет")


while True:
    try:
        r = sr.Recognizer()
        with sr.Microphone(device_index = 1) as source:
            # voice_engine.say("Я вас слушаю")
            # voice_engine.runAndWait()
        
            r.adjust_for_ambient_noise(source)
            print("Я вас слушаю...")
            audio = r.listen(source)

        voice_command = r.recognize_google(audio, language = "ru-RU").lower()
        # voice_engine.say("Вы сказали: " + query.lower())
        # voice_engine.runAndWait()
        print("Вы сказали: " + voice_command)
        try:
            print('начало перебора')
            if voice_command.startswith('саманта'):
             if 'саманта' in voice_command:
                print('триггер фраза обнаружена')
                _task = voice_command

                for x in vocab["alias"]:
                    _task = _task.replace(x, '').strip()
                    for x in vocab["toBeRemoved"]:
                        _task = _task.replace(x, '').strip()

                    _task = recognize_cmd(_task)
                    execute_cmd(_task['task'])
             else: print("триггер не обнаружен")
        except sr.UnknownValueError:
            print("[log] Повторите пожалуйста, я не расслышала")
        except sr.RequestError as error:
            print("[log] Странно, что-то не так. Проверь интернет")
        
    except sr.UnknownValueError:
        print("[log] No commanmds")
        # talk("Повторите пожалуйста, я не расслышала")

    except sr.RequestError as error:
        print("[log] Странно, что-то не так. Проверь интернет")
        # talk("Странно, что-то не так. Проверь интернет")





        
    


# def speak(_phrazeToSpeach):
#     print(_phrazeToSpeach)
#     voice_engine.say(_phrazeToSpeach)
#     voice_engine.runAndWait()
#     voice_engine.stop()

# def callback(recognizer, audio):
#     try:
#         voice = rec.recognize_google(audio, language = "ru-RU").lower()
#         print("[log] Распознано: " + voice)

#         if voice.startswitch(vocab["alias"]):
#             cmd = voice

#             for x in vocab["alias"]:
#                 cmd = cmd.replace(x, '').strip()

#             for x in vocab["toBeRemoved"]:
#                 cmd = cmd.replace(x, '').strip()

#             cmd = recognize_cmd(cmd)
#             execute_cmd(cmd['cmd'])

#     except sr.UnknownValueError:
#         print("[log] Повторите пожалуйста, я не расслышала")
#     except sr.RequestError as error:
#         print("[log] Странно, что-то не так. Проверь интернет")

# def recognize_cmd(cmd):                                                     # поиск нечетких команд
#     RC = {'cmd': '', 'percent': 0}
#     for c,v in vocab['cmds'].items():
#         for x in v:
#             vrt = fuzz.ratio(cmd, x)
#             if vrt > RC['percent']:
#                 RC['cmd'] = c
#                 RC['percent'] = vrt
#     return RC

# def execute_cmd(cmd):
#     if cmd == 'currentTime':
#         now = datetime.datetime.now()
#         speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
#     #elif cmd = 'playMusic':
#     else: show_notification("Саманта","Я не расслышала\nПовтори пожалуйста")

# speak("Привет, Семён. Давненько не виделись")




