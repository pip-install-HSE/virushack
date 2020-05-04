# The system is developed for Virushack hackathon
# It allows to work with self-service ticket office via voise commands


from random import random
import threading
import time
import random

from command_to_kos import ThereIsNoProductWithCurrentName
from command_to_kos import find_product, make_action
from config import working_commands
from text_to_command_conversion.text_to_command import TextToCommand
from from_audio_to_text_conversion.audio_to_text import AudioToText
import os


commands = []
language = 'russian'

mutex_commands = False

stop_threads = False

result = None


AtT = AudioToText()
TtC = TextToCommand()
TtC.set_commands(working_commands)


def answer_to_customer(phrase):
    os.system(f'echo {phrase} | festival --tts --language {language}')


def face_recognition():
    # here goes some long calculation
    global stop_threads
    global mutex_commands
    while (True):
        while (True):
            if (not mutex_commands):
                mutex_commands = True
                # commands.append(random.uniform(2, 3))
                mutex_commands = False
                break
            time.sleep(1e-3)

        time.sleep(10)
        print("Some phrase")
        if (stop_threads):
            break


def speech_recognition():
    global stop_threads
    global mutex_commands
    while True:
        res = AtT.recognize()
        while True:
            if not mutex_commands:
                mutex_commands = True
                try:
                    res = eval(res)
                    commands.append(res['text']) if res['text'] else None
                except:
                    pass
                    # print("Pls, say smth!!!")
                mutex_commands = False
                break
            time.sleep(1e-3)
        print(commands) if commands else None
        if stop_threads:
            break


def command_handler():
    global stop_threads
    global mutex_commands
    curr_commands = []
    while True:
        while True:
            if not mutex_commands:
                mutex_commands = True
                curr_commands = commands.copy()
                for text in curr_commands:
                    commands_now = TtC.get_command(text)
                    check_commands = [i for i in commands_now if i]
                    if len(check_commands) > 0:
                        # answer_to_customer(f"Отлично! Мы что-то поймали")
                        print(f"Отлично! Мы что-то поймали")
                        if len(check_commands) == 1:
                            f = False
                            res = []
                            for i, word in enumerate(text.split()):
                                if commands_now[i]:
                                    f = True
                                    # res.append(commands_now[i])
                                elif f:
                                    res.append(word)
                            print(res)
                            try:
                                make_action([check_commands[0], text])
                            except ThereIsNoProductWithCurrentName:
                                print("Извините, однако у нас нет продуктов с таким именем")
                        else:
                            print(f"Братиш, выбери из предложенного: {check_commands}")
                            # answer_to_customer(f"Братиш, выбери из предложенного: {check_commands}")
                commands.clear()
                mutex_commands = False
                break
            time.sleep(1e-3)

        time.sleep(2)
        # print(curr_commands) if curr_commands else None
        curr_commands.clear()
        if (stop_threads):
            break


def main():
    global stop_threads
    face_recognition_thread = threading.Thread(target=face_recognition)
    face_recognition_thread.start()
    speech_recognition_thread = threading.Thread(target=speech_recognition)
    speech_recognition_thread.start()
    command_handler_thread = threading.Thread(target=command_handler)
    command_handler_thread.start()
    # wait here for the result to be available before continuing
    speech_recognition_thread.join()

    # a = 0
    # input(a)
    # stop_threads = True
    # print('The result is', result)


if __name__ == '__main__':
    main()
