from pvporcupine import create
from pvrecorder import PvRecorder
from API_KEY import PORCUPINE_KEY
from models.models import KEY_WORDS_PATH, MODEL_PATH, KEY_WORDS

class Hotword:
    def __init__(self):
        self.porcupine = create(
            access_key=PORCUPINE_KEY,
            keyword_paths=KEY_WORDS_PATH,
            model_path=MODEL_PATH,
            sensitivities=[0.75, 0.75, 0.75],
        )

    def run(self):
        recorder = PvRecorder(device_index=-1, frame_length=self.porcupine.frame_length)
        recorder.start()

        try:
            while True:
                pcm = recorder.read()
                keyword_index = self.porcupine.process(pcm)

                if keyword_index >= 0:
                    # Todo implement here signals
                    print(f"Detected: {KEY_WORDS[keyword_index]}")
        except:
            pass
        finally:
            recorder.delete()
            self.porcupine.delete()


if __name__ == '__main__':
    Keyword().run()
