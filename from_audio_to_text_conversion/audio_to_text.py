from vosk import Model, KaldiRecognizer
from pyaudio import paInt16, PyAudio
from rnnoise_wrapper import RNNoise


class AudioToText:
    def __init__(self):
        self.p = PyAudio()
        self.rate = 16000
        self.stream = self.p.open(format=paInt16, channels=1, rate=self.rate, input=True, frames_per_buffer=8000)
        self.rec = KaldiRecognizer(Model('/home/victor/PycharmProjects/virushack/from_audio_to_text_conversion/model'), self.rate)
        self.denoiser = RNNoise()
        self.start_stream()
        self.is_started = False

    def start_stream(self):
        self.stream.start_stream()
        self.is_started = True

    def stop_stream(self):
        self.stream.stop_stream()
        self.is_started = False

    def recognize(self):
        data = self.stream.read(2000)
        filtered_data = self.denoiser.filter(data, sample_rate=self.rate)
        if len(filtered_data) == 0:
            return
        if self.rec.AcceptWaveform(filtered_data):
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
