from vosk import Model, KaldiRecognizer
import os
import pyaudio
from rnnoise_wrapper import RNNoise

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

model = Model('/home/victor/PycharmProjects/virushack/from_audio_to_text_conversion/model')
rec = KaldiRecognizer(model, 16000)
denoiser = RNNoise()

while True:
    data = stream.read(2000)

    filtered_data = denoiser.filter(data, sample_rate=16000)

    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())

print(rec.FinalResult())
