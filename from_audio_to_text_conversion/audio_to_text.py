from vosk import Model, KaldiRecognizer
from pyaudio import paInt16, PyAudio


class AudioToText:
    def __init__(self):
        self.p = PyAudio()
        self.stream = self.p.open(format=paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.rec = KaldiRecognizer(Model('/home/victor/PycharmProjects/virushack/from_audio_to_text_conversion/model'), 16000)
        self.start_stream()

    def start_stream(self):
        self.stream.start_stream()

    def recognize(self):
        data = self.stream.read(2000)
        if len(data) == 0:
            return
        if self.rec.AcceptWaveform(data):
            return self.rec.Result()


if __name__ == "__main__":
    a = AudioToText()
    while True:
        print(a.recognize())
# {
#   "result" : [{
#       "conf" : 1.000000,
#       "end" : 22.950000,
#       "start" : 22.560000,
#       "word" : "пока"
#     }],
#   "text" : "пока"
# }
