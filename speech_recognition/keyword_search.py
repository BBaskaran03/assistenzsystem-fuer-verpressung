import re

def search_for_keywords(transcription):
    # Define the keywords to search for
    pause = ['anstrengend', 'pause']
    stop = ['aufhören', 'ich kann nicht mehr', 'keine lust']
    aus = ['aus', 'tschüss', 'ciao', 'bye']

    # Search for the keywords in the transcription
    for keyword in pause:
        match = re.search(keyword, transcription, re.IGNORECASE)
        if match:
            return ("pause", keyword, "Ich merke, dass du angestrengt bist. Brauchst du eine Pause?")
    for keyword in stop:
        match = re.search(keyword, transcription, re.IGNORECASE)
        if match:
            return ("stop", keyword, "Ich merke, dass es dir nicht gut geht. Möchtest du aufhören?")
    for keyword in aus:
        match = re.search(keyword, transcription, re.IGNORECASE)
        if match:
            return ("aus", keyword, "Bist du dir sicher, dass wir für heute aufhören sollen?")

    # If no keyword is found, return None
    return (None, None, None)
