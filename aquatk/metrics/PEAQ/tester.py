from peaq_basic import process_audio_data, process_audio_files
import wave
import librosa
import numpy as np

ref_filename = "hw2_audio.wav"
test_filename = "hw2_watermarked.wav"

ref_audio, ref_rate = librosa.load(ref_filename)
test_audio, test_rate = librosa.load(test_filename)
res_altered = process_audio_data(ref_audio, ref_rate, test_audio, test_rate)
res_old = process_audio_files(ref_filename, test_filename)