import io
import logging
import os
import sys
import time

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
from gtts import gTTS


class TextToSpeech:
    def __init__(self, top_level_domain, language):
        self.top_level_domain = top_level_domain
        self.language = language

    def say(self, text: str):
        logging.debug(f"<{__name__}> | {text}")

        tts = gTTS(
            text=text,
            tld=self.top_level_domain,
            lang=self.language,
            slow=False,
            lang_check=False,
        )

        pygame.mixer.init()

        with io.BytesIO() as buffer:
            tts.write_to_fp(buffer)
            buffer.seek(0)

            pygame.mixer.music.load(buffer)

            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(1)


def main() -> int:
    print("Hello, World")

    # text_to_speech = TextToSpeech("de", "de")
    text_to_speech = TextToSpeech("us", "en")
    text_to_speech.say("Hello, World!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
