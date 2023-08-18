from os import path
from pydub import AudioSegment
import os
import wave
from scipy.io import wavfile
import glob
import soundfile

def checkWav(file):
    sample_rate, data = wavfile.read(file)
    if sample_rate != 22050:
        print(file + " Does not have 22050 KHz!")
    try:
        data[:, 1]
        print(file + " is not mono!")
    except:
        pass


# example files                                                                         
# src = "transcript.mp3"
# dst = "test.wav"

# convert and resampling dataset
src_path = "../dera/split3/*.wav"
dst_path = "../dera/wavs2"

if os.path.isdir(dst_path):
    print("folder exists")
else:
    print("folder does not exist")
    print("creating folder...")
    os.mkdir(dst_path)
    print("folder created")

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
        if frame_rate == 22050:
            print(f'{base_name} does not require resampling.')     
        else:
            print(f'{base_name} has {frame_rate} sample rate, requires resampling.')

            # resample to 22050 and converts to mono
            new_rate = 22050
            # print(os.path.join(dst_path, base_name))
            os.system(f'ffmpeg -y -i {filename} -ar {new_rate} -ac 1 {os.path.join(dst_path, base_name)}') # Converts to Mono also
            print(f'Resampled file {filename}.')

