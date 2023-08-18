from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

'''
#### description ####
audio = audio yang akan di split
chunks = potongan audio yang sudah di split

1000 ms = 1 s
min_silence_length = minimal durasi silence dalam milisecond
silence_threshold = batas minimal volume audio dalam dBFS
max_duration = durasi maksimal audio hasil split dalam milisecond
min_split_duration = durasi minimal audio hasil split dalam milisecond

audio_length = total durasi audio
normalized_chunk = audio yang sudah di normalisasi
match_target_amplitude = fungsi untuk normalisasi audio

bitrate = bitrate audio yang akan di export
format = format audio yang akan di export
'''

# catatan : jika ingin menaikkan max_duration, maka harus menaikkan min_silence_len juga begitu juga sebaliknya
# parameter yang cocok sejauh ini 

# parameters
min_silence_length = 700
silence_threshold = -40
max_duration = 10000        # optional max
min_split_duration = 2000   # optional min

# init
audio_length = 0
total_audio = 0
min_silence = min_silence_length

# change this
output_name = "dwiki"
output_folder = "../dwiki/split/"
source= "../dwiki/coba_record[vocals].wav"

if os.path.isdir(output_folder):
    print("folder exists")
else:
    print("folder does not exist")
    print("creating folder...")
    os.mkdir(output_folder)
    print("folder created")


# normalisasi audio
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

# Load audio.
audio = AudioSegment.from_wav(source)

# Split audio 
chunks = split_on_silence (
    audio, 
    min_silence_len = min_silence,

    # Consider a chunk silent if it's quieter than -40 dBFS
    silence_thresh = silence_threshold
)

# Process each splitted audio
for i, chunk in enumerate(chunks):
    # Create a silence chunk that's 0.1 seconds (or 100 ms) long for padding.
    silence_chunk = AudioSegment.silent(duration=100)

    # Add the padding chunk to beginning and end of the entire chunk.
    audio_chunk = silence_chunk + chunk + silence_chunk

    # split and export audio more than 10 seconds
    max_audio_length = len(audio_chunk)
    flag = False
    while(max_audio_length > max_duration):
        flag = True
        min_silence -= 100
        new_chunks = split_on_silence (
            audio_chunk,
            min_silence_len = min_silence,
            silence_thresh = silence_threshold
        )

        max_audio_length = 0
        for j, new_chunk in enumerate(new_chunks):
            silence_chunk = AudioSegment.silent(duration=100)
            audio_chunk = silence_chunk + new_chunk + silence_chunk
            max_audio_length = max(max_audio_length, len(audio_chunk))
        
        # print(max_audio_length)
        if max_audio_length < max_duration:
            for j, new_chunk in enumerate(new_chunks):
                silence_chunk = AudioSegment.silent(duration=100)
                audio_chunk = silence_chunk + new_chunk + silence_chunk
                normalized_chunk = match_target_amplitude(audio_chunk, -20.0)
                
                if len(normalized_chunk) >= min_split_duration:
                    print("Exporting {0}_{1}.wav with length : {2}ms".format(output_name, total_audio, len(normalized_chunk)))
                    normalized_chunk.export(
                        "./{0}{1}_{2}.wav".format(output_folder, output_name, total_audio),
                        bitrate = "192k",
                        format = "wav"
                    )
                    # print(i)
                    audio_length += len(normalized_chunk)
                    total_audio += 1
            break
        
        if min_silence < 300:
            break
    
    min_silence = min_silence_length
    if flag:
        continue

    # Normalize the entire chunk.
    normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

    if len(normalized_chunk) >= min_split_duration:
        # Export audio with parameters bitrate and format.
        print("Exporting {0}_{1}.wav with length : {2}ms".format(output_name, total_audio, len(normalized_chunk)))
        normalized_chunk.export(
            "./{0}{1}_{2}.wav".format(output_folder, output_name, total_audio),
            bitrate = "192k",
            format = "wav"
        )
        # print(i)
        audio_length += len(normalized_chunk)
        total_audio += 1

# average audio length
print(f"average audio length : {audio_length/total_audio}ms")

# total duration
print(f"total duration : {audio_length/1000}s")