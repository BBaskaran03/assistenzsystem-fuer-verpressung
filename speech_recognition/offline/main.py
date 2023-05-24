from pvporcupine import create
from pvrecorder import PvRecorder
from keys import ACCESS_KEY
from models.models import KEY_WORDS_PATH, MODEL_PATH, KEY_WORDS
# from time import time


porcupine = create(
    access_key=ACCESS_KEY,
    keyword_paths=KEY_WORDS_PATH,
    model_path=MODEL_PATH,
    sensitivities=[0.75, 0.75]
)

recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
recorder.start()

try:
    # t = time()

    while True:
        # if time() - t > 2:
        #     t = time()
        #     print("Still listening")

        pcm = recorder.read()
        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print(f"Detected: {KEY_WORDS[keyword_index]}")
except:
    pass
finally:
    recorder.delete()
    porcupine.delete()
