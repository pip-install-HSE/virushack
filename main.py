# The system is developed for Virushack hackathon
# It allows to work with self-service ticket office via voise commands


from random import random
import threading
import time
import random
from text_to_command_conversion.text_to_command import TextToCommand
from from_audio_to_text_conversion.audio_to_text import AudioToText
import os


commands = []
working_commands = ["начать", "добавить", "далее", "оплата", "банковский"]
mutex_commands = False

stop_threads = False

result = None

AtT = AudioToText()
TtC = TextToCommand(working_commands)


def answer_to_customer(phrase):
    os.system(f'echo {phrase} | festival --tts')


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
        print(commands)
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
                    if len(commands_now) > 0:
                        answer_to_customer(f"Отлично! Мы что-то поймали")
                        if len(commands_now) == 1:
                            pass
                        else:
                            answer_to_customer(f"Братиш, выбери из предложенного: {commands_now}")
                commands.clear()
                mutex_commands = False
                break
            time.sleep(1e-3)

        time.sleep(2)
        print(curr_commands)
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
