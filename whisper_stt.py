import whisper
import os
import glob

directory = "../dera/split3/*.wav"
txt_dir = "../dera/split3"

model = whisper.load_model('medium')

def converter(path):
    # open the file
    try:
        result = model.transcribe(path, fp16=False, language='Indonesian')

        # delete first space
        if (result["text"][0] == " "):
            result["text"] = result["text"][1:]
        text = os.path.splitext(os.path.basename(path))[0] + "|" + result["text"] + "|" + result["text"]
    except Exception as e:
        text = "none"
    return text

# assign directory
STT=[]

# iterate over files in that directory
itr=1
for filename in sorted(glob.glob(directory)):
    f = os.path.join(directory, filename)
    f_1=f.split("/")
    print(filename)

    text=converter(filename)
    if text == "none":
        print(text)
    else:
        print(text)
        STT.append(text)
    itr=itr+1
print(STT)

file = open(f'{txt_dir}/new_list(whisper).txt','w')
for item in STT:
    file.write(item+"\n")
file.close()
