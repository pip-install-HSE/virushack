from vosk import Model, KaldiRecognizer
from pyaudio import paInt16, PyAudio
# from rnnoise_wrapper import RNNoise


class AudioToText:
    def __init__(self, model_name="en"):
        self.p = PyAudio()
        self.rate = 16000
        self.stream = self.p.open(format=paInt16, channels=1, rate=self.rate, input=True, frames_per_buffer=8000)
        self.rec = KaldiRecognizer(Model(model_name), self.rate)
        # self.denoiser = RNNoise()
        self.start_stream()
        self.is_started = False

    def start_stream(self):
        self.stream.start_stream()
        self.is_started = True

    def stop_stream(self):
        self.stream.stop_stream()
        self.is_started = False

    def recognize(self):
        data = self.stream.read(4000)
        # filtered_data = self.denoiser.filter(data, sample_rate=self.rate)
        filtered_data = data
        if len(filtered_data) == 0:
            return
        if self.rec.AcceptWaveform(filtered_data):
            return self.rec.Result()


if __name__ == "__main__":
    import sys
    try:
        model_name = sys.argv[1]
    except:
        model_name = "en"
    a = AudioToText(model_name)
    while True:
        x = a.recognize()
        if x:
            print(eval(x)["text"])
