from speech_recognition import Recognizer, Microphone
from logging import debug, basicConfig
from argparse import ArgumentParser
from API_KEY import OPENAI_API_KEY
import openai

LANGUAGE_CODE = 'de-DE'
SYSTEM_MESSAGE = {
    "role": "system",
    "content": "Du bist Yumi. Assistent von Kathrin. Kathrin arbeitet in einer Behinderten Werkstatt und ist leicht kognitiv eingeschränkt. Du unterstützt Sie bei der Arbeit. Antworte ihr so kurz und knapp wie möglich aber freundlich. Motiviere Sie."
}


def get_prompt() -> str:
    recognizer = Recognizer()
    microphone = Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        debug('Listening...')
        audio = recognizer.listen(source)

    return recognizer.recognize_google(audio, language=LANGUAGE_CODE)


def get_response_of_prompt(prompt: str) -> str:
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            SYSTEM_MESSAGE,
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response['choices'][0]['message']['content']


def listen_and_respond() -> str:
    prompt = get_prompt()
    return get_response_of_prompt(prompt)


def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')

    if parser.parse_args().debug:
        basicConfig(level='DEBUG')
        prompt = get_prompt()
        debug(prompt)
        response = get_response_of_prompt(prompt)
        debug(response)


if __name__ == '__main__':
    main()
