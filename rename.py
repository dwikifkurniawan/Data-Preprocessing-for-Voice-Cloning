import glob
import os

path = "../Raffi Ahmad/split2/*.wav"

# rename all files in the path
for filename in glob.glob(path):
    # print(filename)
    os.rename(filename, filename.replace("raffi", "raffi2_"))
    print(f'{filename} renamed to {filename.replace("raffi", "raffi2_")}')
