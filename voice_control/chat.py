import argparse
import logging

import openai
import speech_recognition


class Chat:
    # TODO: Give ChatGPT awareness of date and time

    MODEL = "gpt-3.5-turbo"

    SYSTEM_MESSAGE = {
        "role": "system",
        "content": "Du bist Yumi. Assistent von Kathrin. Kathrin arbeitet in einer Behinderten Werkstatt und ist leicht kognitiv eingeschränkt. Du unterstützt Sie bei der Arbeit. Antworte ihr so kurz und knapp wie möglich aber freundlich. Motiviere Sie.",
    }

    def __init__(self, api_key, language):
        # self.api_key = api_key
        openai.api_key = api_key
        self.language = language

    def get_prompt(self) -> str:
        recognizer = speech_recognition.Recognizer()
        microphone = speech_recognition.Microphone()

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)

            logging.info("Listening for prompt...")
            voice_recording = recognizer.listen(source)

        # TODO: Check, if we need a custom API key here
        # The Google Speech Recognition API key is specified by key. If not specified, it uses a generic key that works out of the box. This should generally be used for personal or testing purposes only, as it **may be revoked by Google at any time**.

        voice_recording_as_text = recognizer.recognize_google(
            voice_recording, language=self.language
        )

        return voice_recording_as_text

    def get_response(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=[self.SYSTEM_MESSAGE, {"role": "user", "content": prompt}],
        )
        response = response["choices"][0]["message"]["content"]

        return response

    def listen_and_respond(self) -> str:
        prompt = self.get_prompt()
        logging.info(f"User said: {prompt}")

        response = self.get_response(prompt)
        logging.debug(f"{self.MODEL} answered: {response}")

        return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")

    # TODO: Load API_KEY from somewhere
    OPENAI_API_KEY = None

    chat = Chat(OPENAI_API_KEY, language="de-DE")

    prompt = chat.get_prompt()
    response = chat.get_response(prompt)
    logging.debug(response)


if __name__ == "__main__":
    main()
