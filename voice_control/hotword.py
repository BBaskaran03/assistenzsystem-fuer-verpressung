import logging
import os
import sys
import threading
import time

import vlc
from pvporcupine import create
from pvrecorder import PvRecorder

from config import CONFIG
from voice_control.models.models import KEY_WORDS, KEY_WORDS_PATH, MODEL_PATH


class Hotword:
    def __init__(self, porcupine_api_key):
        self.porcupine = create(
            access_key=porcupine_api_key,
            keyword_paths=KEY_WORDS_PATH,
            model_path=MODEL_PATH,
            sensitivities=[0.75, 0.75, 0.75],
        )

        # TODO: [WARN] Overflow - reader is not reading fast enough.
        # Workaround: Suppress error with <log_overflow=False>
        self.recorder = PvRecorder(
            device_index=-1,
            frame_length=self.porcupine.frame_length,
            log_overflow=False,
        )

    def play_sound_effect(self):
        file = f'{CONFIG["PORCUPINE"]["SoundEffectFile"]}'

        vlc_instance = vlc.Instance()
        player = vlc_instance.media_player_new()
        media = vlc_instance.media_new(file)
        player.set_media(media)

        player.play()
        time.sleep(1.5)

        duration = player.get_length() / 1000
        time.sleep(duration)

    def wait_for_hotword(self):
        self.recorder.start()

        while True:
            pcm = self.recorder.read()
            keyword_index = self.porcupine.process(pcm)

            if keyword_index < 0:
                continue

            # Ensure recording is stoppe
            self.recorder.stop()

            keyword = KEY_WORDS[keyword_index]
            logging.debug(f"Keyword recogniced: {keyword}")

            thread_sound_effect = threading.Thread(target=self.play_sound_effect)
            thread_sound_effect.start()

            return keyword


def main() -> int:
    # TODO: Get porcupine_api_key from somewhere
    porcupine_api_key = None

    hotword = Hotword(porcupine_api_key)
    hotword.wait_for_hotword()

    return 0


if __name__ == "__main__":
    sys.exit(main())
