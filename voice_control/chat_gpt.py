import argparse
import logging

import openai
from config import CONFIG


class ChatGPT:
    # TODO: Give ChatGPT awareness of date and time

    MODEL = "gpt-3.5-turbo"

    SYSTEM_MESSAGE = {
        "role": "system",
        "content": CONFIG["OPENAI"]["Context"]
    }

    def __init__(self, api_key, language):
        # self.api_key = api_key
        openai.api_key = api_key
        self.language = language

    def get_response(self, prompt: str) -> str:
        if CONFIG["OPENAI"]["DONT QUERY"]:
            return "Hier könnte Ihre Werbung stehen."

        response = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=[self.SYSTEM_MESSAGE, {"role": "user", "content": prompt}],
        )

        logging.debug(response)

        response = response["choices"][0]["message"]["content"]

        return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")

    # TODO: Load API_KEY from somewhere
    OPENAI_API_KEY = None

    chat_gpt = ChatGPT(OPENAI_API_KEY, language="de-DE")

    prompt = "Hello, World!"
    response = chat_gpt.get_response(prompt)
    logging.debug(response)


if __name__ == "__main__":
    main()
