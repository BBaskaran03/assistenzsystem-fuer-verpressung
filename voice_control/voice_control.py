import sys
from chat import Chat
from hotword import Hotword


class VoiceControl():
    def __init__(self):
        self.chat = Chat()

    def listen(): pass

    def check_context_stop(self, context: str) -> bool:
        if context.tolower().startswith("stop"):
            # Todo implement here signal
            return True


def main() -> int:
    print("Hello, World")

    voice_control = VoiceControl()
    voice_control.listen()

    return 0


if __name__ == "__main__":
    sys.exit(main())
