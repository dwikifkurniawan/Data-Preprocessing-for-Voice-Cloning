from os import path
from pydub import AudioSegment
import os
import wave
from scipy.io import wavfile
import glob
import soundfile

# example files                                                                         
# src = "transcript.mp3"
# dst = "test.wav"

# convert and resampling dataset
src_path = "../dwiki/split/*.wav"
dst_path = "../dwiki/dwiki"

if os.path.isdir(dst_path):
    print("folder exists")
else:
    print("folder does not exist")
    print("creating folder...")
    os.mkdir(dst_path)
    print("folder created")

# dst_path = "G:/TTS/dataset/"
# dst_resampled = "G:/TTS/dataset_resampled/"

for filename in glob.glob(src_path):
    # filename = filename.replace("\\", "/")
    print(filename)
    speaker = filename.split("/")[-2]
    base_name = filename.split("/")[-1]
    print(base_name)

    # convert to 16bit
    data, samplerate = soundfile.read(filename)
    soundfile.write(filename, data, samplerate, subtype='PCM_16')

    with wave.open(filename, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        if frame_rate == 44100:
            print(f'{base_name} does not require resampling.')     
        else:
            print(f'{base_name} has {frame_rate} sample rate, requires resampling.')

            # resample to 44100 and converts to mono
            new_rate = 44100
            # print(os.path.join(dst_path, base_name))
            os.system(f'ffmpeg -y -i {filename} -ar {new_rate} -ac 1 {os.path.join(dst_path, base_name)}') # Converts to Mono also
            print(f'Resampled file {filename}.')


######################
# filename = "../download/raffi_social_experiment.wav"
# dst_path = "../converted"
# data, samplerate = soundfile.read(filename)
# soundfile.write(filename, data, samplerate, subtype='PCM_16')

# with wave.open(filename, "rb") as wave_file:
#     frame_rate = wave_file.getframerate()
#     if frame_rate == 22050:
#         print(f'{filename} does not require resampling.')     
#     else:
#         print(f'{filename} has {frame_rate} sample rate, requires resampling.')

#         # resample to 22050 and converts to mono
#         new_rate = 22050
#         os.system(f'ffmpeg -y -i {filename} -ar {new_rate} -ac 1 {os.path.join(dst_path, "raffi_social_experiment.wav")}') # Converts to Mono also
#         print(f'Resampled file {filename}.')