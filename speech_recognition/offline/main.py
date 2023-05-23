from pvporcupine import create
from pvrecorder import PvRecorder
from keys import ACCESS_KEY
from models.models import KEY_WORDS_PATH, MODEL_PATH, KEY_WORDS

recorder = PvRecorder()
recorder.start()

porcupine = create(
    access_key=ACCESS_KEY,
    keyword_paths=KEY_WORDS_PATH,
    model_path=MODEL_PATH
)

try:
    while True:
        pcm = recorder.read()
        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print(f"Detected: {KEY_WORDS[keyword_index]}")
except:
    pass
finally:
    recorder.delete()
    porcupine.delete()
