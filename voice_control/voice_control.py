import logging
import os
import sys

import vlc

from config import CONFIG
from text_to_speech.text_to_speech import TextToSpeech
from voice_control.chat_gpt import ChatGPT
from voice_control.hotword import Hotword
from voice_control.speech_to_text import SpeechToText


class VoiceControl:
    def __init__(self, porcupine_api_key, openai_api_key):
        self.chat_gpt = ChatGPT(openai_api_key, language="de-DE")
        self.hotword = Hotword(porcupine_api_key)
        self.speech_to_text = SpeechToText("de")
        self.text_to_speech = TextToSpeech("de", "de")

    def check_hotword(self, hotword: str) -> bool:
        # TODO: Implement this correctly
        if hotword == "HEY_YUMI":
            return True
        if hotword == "YUMI_STOP":
            return True
        if hotword == "YUMI_WEITER":
            return True

    def check_response(self, context: str) -> bool:
        # TODO: Implement this

        if context.lower().startswith("stop"):
            # TODO: Implement signal here
            return True

    def listen(self):
        hotword = self.hotword.wait_for_hotword()
        vlc.MediaPlayer(
            f"{os.path.dirname(os.path.realpath(__file__))}/ding-36029.mp3"
        ).play()
        self.check_hotword(hotword)

        prompt = self.speech_to_text.get_prompt()
        logging.info(f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["User"]}> {prompt}')

        response = self.chat_gpt.get_response(prompt)
        self.check_response(response)
        logging.info(f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["Robot"]}> {response}')

        self.text_to_speech.say(response)

    def start(self):
        prompt = f'Hallo {CONFIG["Names"]["Robot"]}. Begrüße mich bitte in einem Satz.'
        logging.debug(f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["User"]}> {prompt}')

        response = self.chat_gpt.get_response(prompt)
        logging.info(f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["Robot"]}> {response}')
        self.text_to_speech.say(response)

        i_should_listen = True
        while i_should_listen:
            self.listen()


def main() -> int:
    print("Hello, World")

    # TODO: Load PORCUPINE_API_KEY and OPENAI_API_KEY from somewhere
    porcupine_api_key, openai_api_key = None, None

    voice_control = VoiceControl(porcupine_api_key, openai_api_key)
    voice_control.listen()

    return 0


if __name__ == "__main__":
    sys.exit(main())
