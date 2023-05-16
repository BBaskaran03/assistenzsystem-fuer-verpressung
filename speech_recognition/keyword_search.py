import re

def search_for_keywords(transcription):
    # Define the keywords to search for

    # befehle
    isprompt = False
    yumi = ['Yumi', 'Dummi', 'You me', 'Yume', 'Yomi', 'Yome', 'Juni', 'Jumi', 'Lumi', 'Gummi']


    aus = ['aus', 'tschüss', 'ciao', 'bye', 'stop']

    # spymode befehle
    pause = ['anstrengend', 'pause']
    stop = ['aufhören', 'ich kann nicht mehr', 'keine lust', 'stop', 'halt']

    # easter egg befehle
    bad = ['hurensohn', 'huhrensohn', 'hurrensohn', 'hurrelsohn', 'hurelsohn', 'bastard', 'arschloch', 'wichser', 'fick dich', 'fuck you', 'fuck off', 'verpiss dich', 'penner']


    # Yumi Keyword
    for keyword in yumi:
        match = re.search(keyword, transcription, re.IGNORECASE) and not re.search('aus', transcription, re.IGNORECASE)
        if match:
            isprompt = True

    # Yumi Befehle
    for keyword in aus:
        match = re.search(keyword, transcription, re.IGNORECASE)
        if match and isprompt:
            return ("aus", keyword, "Wir hören jetzt auf")


    # Spymode        
    for keyword in pause:
        match = re.search(keyword, transcription, re.IGNORECASE)
        if match:
            return ("pause", keyword, "Ich merke, dass du angestrengt bist. Brauchst du eine Pause?")
    for keyword in stop:
        match = re.search(keyword, transcription, re.IGNORECASE)
        if match :
            return ("stop", keyword, "Ich merke, dass es dir nicht gut geht. Möchtest du aufhören?")

    # Eastereggs
    for keyword in bad:
        match = re.search(keyword, transcription, re.IGNORECASE)
        if match:
            return ("bad", keyword, "Solche Worte wollen wir hier nicht nutzen. Das verletzt meine Gefühle!")

    # If no keyword is found, return None
    return (None, None, None)
