import logging

import speech_recognition


class SpeechToText:
    def __init__(self, language):
        self.language = language

    def get_prompt(self) -> str:
        recognizer = speech_recognition.Recognizer()
        microphone = speech_recognition.Microphone()

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)

            logging.debug("Listening for prompt ...")
            voice_recording = recognizer.listen(source)

        # TODO: Check, if we need a custom API key here
        # The Google Speech Recognition API key is specified by key. If not specified, it uses a generic key that works out of the box. This should generally be used for personal or testing purposes only, as it **may be revoked by Google at any time**.

        voice_recording_as_text = recognizer.recognize_google(
            voice_recording, language=self.language
        )

        logging.debug(f"Recorded: {voice_recording_as_text}")

        return voice_recording_as_text


def main():
    speech_to_text = SpeechToText("de")

    prompt = speech_to_text.get_prompt()
    print(prompt)


if __name__ == "__main__":
    main()
