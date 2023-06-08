import sys
import logging

from text_to_speech.text_to_speech import TextToSpeech
from voice_control.chat import Chat
from voice_control.hotword import Hotword


class VoiceControl:
    def __init__(self, porcupine_api_key, openai_api_key):
        self.text_to_speech = TextToSpeech("de", "de")
        self.hotword = Hotword(porcupine_api_key)
        self.chat = Chat(openai_api_key, language="de-DE")

    def listen(self):
        i_should_listen = True

        while i_should_listen:
            keyword = self.hotword.run()
            logging.debug(f"Keyword detected: {keyword}")

            # TODO: Sound abspielen
            response = self.chat.listen_and_respond()
            self.text_to_speech.say(response)

    def check_context_stop(self, context: str) -> bool:
        # TODO: Implement this
        if context.tolower().startswith("stop"):
            # TODO: Implement signal here
            return True


def main() -> int:
    print("Hello, World")

    # TODO: Load PORCUPINE_API_KEY and OPENAI_API_KEY from somewhere
    porcupine_api_key, openai_api_key = None, None

    voice_control = VoiceControl(porcupine_api_key, openai_api_key)
    voice_control.listen()

    return 0


if __name__ == "__main__":
    sys.exit(main())
