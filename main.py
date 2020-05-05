# The system is developed for Virushack hackathon
# It allows to work with self-service ticket office via voise commands


from random import random
import threading
import time
import random

from text_to_command_conversion.command_to_kos import ThereIsNoProductWithCurrentName, TryOneMoreTime
from text_to_command_conversion.command_to_kos import find_product, make_action
from config import working_commands
from text_to_command_conversion.text_to_command import TextToCommand
from from_audio_to_text_conversion.audio_to_text import AudioToText
import os
import cv2

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam.
cap = cv2.VideoCapture(0)

commands = []
language = 'russian'

mutex_commands = False
face_recognized = time.time()
d_face_recognized = 2

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
    global face_recognized
    while True:
        while True:
            _, img = cap.read()
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Detect the faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            face_recognized = time.time() if len(faces) else face_recognized
            # Draw the rectangle around each face
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # Display
            cv2.imshow('img', img)
            # Stop if escape key is pressed
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
            time.sleep(1e-2)

        time.sleep(1e-2)
        if stop_threads:
            break


def speech_recognition():
    global stop_threads
    global mutex_commands
    global face_recognized
    global d_face_recogized
    while True:
        if time.time() - face_recognized > d_face_recognized:
            print("\nСпасибо за покупки))") if AtT.is_started else None
            AtT.stop_stream() if AtT.is_started else None
            time.sleep(1e-3)
            continue
        print("\nЗдравствуй, дорогой покупатель!\nРад тебя видеть!)\n") if not AtT.is_started and time.time() - face_recognized < d_face_recognized else None
        AtT.start_stream() if not AtT.is_started else None
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
        # print(commands) if commands else None
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
                    check_commands = list(set([i for i in commands_now if i]))
                    if len(check_commands) > 0:
                        # answer_to_customer(f"Отлично! Мы что-то поймали")
                        # print(f"Отлично! Мы что-то поймали")
                        # print("Есть! Распознали!")
                        if len(check_commands) == 1:
                            print("\n", *commands)
                            try:
                                make_action([check_commands[0], text])
                            except (ThereIsNoProductWithCurrentName, TryOneMoreTime):
                                pass
                        else:
                            print(f"Извините, не могли бы Вы уточнить: {check_commands}")
                            # answer_to_customer(f"Братиш, выбери из предложенного: {check_commands}")
                commands.clear()
                mutex_commands = False
                break
            time.sleep(1e-3)
        time.sleep(1e-2)
        # time.sleep(2)
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
    cap.release()
    # a = 0
    # input(a)
    # stop_threads = True
    # print('The result is', result)


if __name__ == '__main__':
    main()
