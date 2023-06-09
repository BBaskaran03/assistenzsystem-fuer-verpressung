import logging
import sys

from pvporcupine import create
from pvrecorder import PvRecorder

from voice_control.models.models import KEY_WORDS, KEY_WORDS_PATH, MODEL_PATH


class Hotword:
    def __init__(self, porcupine_api_key):
        self.porcupine = create(
            access_key=porcupine_api_key,
            keyword_paths=KEY_WORDS_PATH,
            model_path=MODEL_PATH,
            sensitivities=[0.75, 0.75, 0.75],
        )

    def run(self):
        recorder = PvRecorder(device_index=-1, frame_length=self.porcupine.frame_length)

        recorder.start()
        while True:
            pcm = recorder.read()
            keyword_index = self.porcupine.process(pcm)

            if keyword_index < 0:
                continue

            # Ensure recording is stopped
            recorder.delete()

            keyword = KEY_WORDS[keyword_index]
            logging.debug(f"Keyword recogniced: {keyword}")

            return keyword


def main() -> int:
    # TODO: Get porcupine_api_key from somewhere
    porcupine_api_key = None

    hotword = Hotword(porcupine_api_key)
    hotword.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())
