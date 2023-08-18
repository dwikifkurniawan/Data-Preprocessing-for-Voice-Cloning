import speech_recognition as sr
import os
import glob

directory = "../Raffi Ahmad/raffi_ahmad/wavs/*.wav"
txt_dir = "../Raffi Ahmad/raffi_ahmad/"

def converter(r,path):
    # open the file
    with sr.AudioFile(path) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language='id')
            text = os.path.splitext(os.path.basename(path))[0] + "|" + text + ".|" + text + "."
        except Exception as e:
            text = "none"
    return text

# assign directory
STT=[]

# iterate over files in that directory
itr=1
for filename in glob.glob(directory):
    f = os.path.join(directory, filename)
    f_1=f.split("/")
    print(filename)
    # initialize the recognizer
    r = sr.Recognizer()
    text=converter(r,filename)
    if text == "none":
        print(text)
    else:
        print(text)
        STT.append(text)
    itr=itr+1
print(STT)

file = open(f'{txt_dir}/new_list.txt','w')
for item in STT:
    file.write(item+"\n")
file.close()
