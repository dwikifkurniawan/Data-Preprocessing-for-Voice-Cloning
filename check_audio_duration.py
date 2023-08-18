from pydub import AudioSegment
import os

file_path = '../dwiki/dwiki'

count = 0.0
total_file = 0
for filename in os.listdir(file_path):
    audio = AudioSegment.from_file(os.path.join(file_path, filename))
    if filename.split("_")[0] == "dera9" or filename == ".DS_Store":
        continue
    if filename.endswith(".wav"):
        count = count + audio.duration_seconds
        total_file += 1
        print(f"{filename} : {audio.duration_seconds:.2f}s")

print()
print()
print(f"Total Duration : {count:.2f}s / {count/60:.2f}min")
print(f"Average Duration : {count/total_file:.2f}s")