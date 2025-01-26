import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft
from scipy.signal.windows import hann
import wave
from Sideify import testvector

def get_wave_info(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        n_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        framerate = wav_file.getframerate()
        n_frames = wav_file.getnframes()
        compression_type = wav_file.getcomptype()
        compression_name = wav_file.getcompname()
        
        duration = n_frames / framerate
        
        print("Number of channels:", n_channels)
        print("Sample width (bytes):", sample_width)
        print("Frame rate (samples per second):", framerate)
        print("Number of frames:", n_frames)
        print("Compression type:", compression_type)
        print("Compression name:", compression_name)
        print("Duration (seconds):", duration)

        data = wav_file.readframes(n_frames)

        return n_channels, sample_width, framerate, n_frames, duration, data
    

    
n_channels, sample_width, framerate, n_frames, duration, data = get_wave_info("testtone.wav")

# Turn bytes --> pcm
pcm = np.frombuffer(data, dtype=np.int16) #PCM data, derived from raw bytes

# Turns 1d pcm --> 2d pcm which each item being [index, value]. This is our (x,y) coordinates
pcm_indices = np.arange(pcm.size)
original = np.column_stack((pcm_indices,pcm))
#print(zipped)

# Rotates the (x,y) coordinates by the specified angle
degree = 90
transformed_pcm_array = testvector.rotation(original,degree) #INPUT, DEGREE

original_distance = abs(pcm_indices.min()) + abs(pcm_indices.max()) 
transformed_distance = abs(transformed_pcm_array[:,0].min()) + abs(transformed_pcm_array[:, 0].max()) #even though its vertical, there are just as many x values as indices

distance_ratio = original_distance / transformed_distance
distance_ratio = round(distance_ratio)

print(original_distance, transformed_distance, distance_ratio)

reduced_pcm = testvector.reduce_frames(original, transformed_pcm_array, distance_ratio)
print(reduced_pcm)

# Turns 2d pcm --> 1d pcm --> bytes
reduced_pcm = reduced_pcm[:,1] #takes value column to convert back to 1d
print(reduced_pcm.min(),reduced_pcm.max())
print(len(reduced_pcm))
modified_data = reduced_pcm.astype(np.int16).tobytes()

# Creates .wav with bytes as data
with wave.open("transformedouput.wav", mode="wb") as wav_file:
    wav_file.setnchannels(n_channels)
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(framerate)
    wav_file.writeframes(modified_data)



