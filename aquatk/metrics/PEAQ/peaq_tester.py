from .peaq_basic import process_audio_data, process_audio_files
import wave
import librosa
import numpy as np

ref_filename = "PEAQ/hw2_audio.wav"
test_filename = "PEAQ/hw2_watermarked.wav"

print("preload")
ref_audio, ref_rate = librosa.load(ref_filename, sr=None)
test_audio, test_rate = librosa.load(test_filename, sr=None)
print("old way")
res_old = process_audio_files(ref_filename, test_filename)
print("new way")
res_altered = process_audio_data(ref_audio, ref_rate, test_audio, test_rate)

print(res_old)
print(res_altered)

assert res_old["Distortion Index"] == res_altered["Distortion Index"]
assert res_old["Objective Difference Grade"] == res_altered["Objective Difference Grade"]
