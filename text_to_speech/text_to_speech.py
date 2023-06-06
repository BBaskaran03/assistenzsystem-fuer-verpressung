import sys
import voice_control.online.text_to_speech as OnlineTTS
from robot_web_services.positions import Position


class TextToSpeech():
    def __init__(self): pass

    def say(self, text: str):
        # print(f"<TextToSpeech> | {text}")
        OnlineTTS.speak(text,'de')


def main() -> int:
    print("Hello, World")

    text_to_speech = TextToSpeech()
    text_to_speech.say("Hello, World!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
