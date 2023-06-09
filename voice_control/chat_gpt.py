import argparse
import logging

import openai
import speech_recognition


class ChatGPT:
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

    def get_response(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=[self.SYSTEM_MESSAGE, {"role": "user", "content": prompt}],
        )
        response = response["choices"][0]["message"]["content"]

        return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")

    # TODO: Load API_KEY from somewhere
    OPENAI_API_KEY = None

    chat_gpt = ChatGPT(OPENAI_API_KEY, language="de-DE")

    prompt = chat_gpt.get_prompt()
    response = chat_gpt.get_response(prompt)
    logging.debug(response)


if __name__ == "__main__":
    main()
