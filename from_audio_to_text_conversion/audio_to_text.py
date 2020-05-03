from vosk import Model, KaldiRecognizer
from pyaudio import paInt16, PyAudio


class AudioToText:
    def __init__(self):
        self.p = PyAudio()
        self.stream = self.p.open(format=paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.rec = KaldiRecognizer(Model('model'), 16000)

    def start_stream(self):
        self.stream.start_stream()

    def start_recognition(self):
        while True:
            data = self.stream.read(2000)
            if len(data) == 0:
                break
            if self.rec.AcceptWaveform(data):
                print(self.rec.Result())
