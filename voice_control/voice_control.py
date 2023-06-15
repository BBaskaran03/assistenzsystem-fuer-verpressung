import logging
import sys

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
            return False
        if hotword == "YUMI_WEITER":
            return False

    def check_response(self, response: str) -> bool:
        # TODO: Implement this

        if response.startswith("ROBOT TASK"):
            return False

        return True

    def listen(self) -> str:
        hotword = self.hotword.wait_for_hotword()

        if self.check_hotword(hotword) is False:
            return hotword

        prompt = self.speech_to_text.get_prompt()
        logging.info(
            f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["User"]}> {prompt}'
        )

        response = self.chat_gpt.get_response(prompt)
        logging.info(
            f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["Robot"]}> {response}'
        )

        if self.check_response(response) is False:
            return response

        self.text_to_speech.say(response)

    def start(self):
        if CONFIG["DEBUG"]:
            return

        prompt = f'Hallo {CONFIG["Names"]["Robot"]}. Begrüße mich bitte in einem Satz.'

        # Temporary fix: Stop ChatGPT from answering with "ROBOT TASK 0: ..."
        prompt = f"{prompt} Beginne Deine Antwort nicht mit ROBOT TASK 0: "

        logging.debug(
            f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["User"]}> {prompt}'
        )

        response = self.chat_gpt.get_response(prompt)
        logging.info(
            f'[{CONFIG["Names"]["System"]}] <{CONFIG["Names"]["Robot"]}> {response}'
        )
        self.text_to_speech.say(response)

    def wait_for_task(self) -> str:
        i_should_listen = True

        while i_should_listen:
            response = self.listen()

            if response is not None:
                return response


def main() -> int:
    print("Hello, World")

    # TODO: Load PORCUPINE_API_KEY and OPENAI_API_KEY from somewhere
    porcupine_api_key, openai_api_key = None, None

    voice_control = VoiceControl(porcupine_api_key, openai_api_key)
    voice_control.listen()

    return 0


if __name__ == "__main__":
    sys.exit(main())
