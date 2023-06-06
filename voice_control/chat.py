from speech_recognition import Recognizer, Microphone
from logging import debug, basicConfig
from argparse import ArgumentParser
from API_KEY import OPENAI_API_KEY
import openai


class Chat:
    LANGUAGE_CODE = 'de-DE'
    SYSTEM_MESSAGE = {
        "role": "system",
        "content": "Du bist Yumi. Assistent von Kathrin. Kathrin arbeitet in einer Behinderten Werkstatt und ist leicht kognitiv eingeschränkt. Du unterstützt Sie bei der Arbeit. Antworte ihr so kurz und knapp wie möglich aber freundlich. Motiviere Sie."
    }

    def get_prompt(self) -> str:
        recognizer = Recognizer()
        microphone = Microphone()

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            debug('Listening...')
            audio = recognizer.listen(source)

        return recognizer.recognize_google(audio, language=self.LANGUAGE_CODE)


    def get_response_of_prompt(self, prompt: str) -> str:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                self.SYSTEM_MESSAGE,
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response['choices'][0]['message']['content']


    def listen_and_respond(self) -> str:
        prompt = self.get_prompt()
        return self.get_response_of_prompt(prompt)


def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')

    if parser.parse_args().debug:
        chat = Chat()
        basicConfig(level='DEBUG')
        prompt = chat.get_prompt()
        response = chat.get_response_of_prompt(prompt)
        debug(response)


if __name__ == '__main__':
    main()
