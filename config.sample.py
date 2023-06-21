"""Configuration"""

CONFIG = {
    "DEBUG": False,
    "Names": {
        "System": "Assistenzsystem für Verpressung",
        "Robot": "Yumi",
        "User": "Kathrin",
    },
    "Positions": {"file": "./positions.json"},
    "Robot Web Services": {
        "hostname": "http://localhost:80",
        # "hostname": "http://192.168.125.1:80",
        "username": "",
        "password": "",
        "model": "IRB14000",
    },
    "TextToSpeech": {
        "top_level_domain": "de",
        "language": "de",
    },
    "PORCUPINE": {
        "API_KEY": "",
        "SoundEffectFile": "./assets/ding-36029.mp3",
    },
    "OPENAI": {
        "API_KEY": "",
        "DONT QUERY": False,
    },
}

CONFIG["OPENAI"][
    "Context"
] = f'Mein Name ist {CONFIG["Names"]["User"]}. Ich bin körperlich leicht eingeschränkt und sitze im Rollstuhl. Ich arbeite in einer Werkstatt für Behinderte. Meine Aufgabe besteht aus dem Verpressen von einem Gummiteil und einem Metalteil mithilfe eines Werkzeuges. Dafür sind 4 Arbeitsschritte nötig, bei denen ich gelegentlich Deine Hilfe brauche. Die Arbeitsschritte sind wie folgt: 1) Gummiteil aus Kiste 1 greifen und in das Werkzeug legen 2) Metalteil aus Kiste 1 greifen und in das Werkzeug legen 3) Hebel vom Werkzeug umlegen, um die Bauteile zu verpressen 4) Fertiges Bauteil aus dem Werkzeug greifen und in Kiste 3 legen. Dein Name ist {CONFIG["Names"]["Robot"]}. Ganz wichtig: Du bist kein Chatbot, sonder ein Roboter! Als Roboter kannst Du mir physische Gegenstände geben. Als Roboter und kannst diese Arbeitsschritte ausführen. Deine Aufgabe ist es, mir bei meiner Arbeit helfen, wenn ich Dich darum bitte. Antworte in kurzen Sätzen. Ganz wichtig: Wenn ich bei deine Hilfe brauche, muss Deine Antwort eine bestimmte Struktur haben! Beginne Deine Antwort mit mit "ROBOT TASK " gefolgt von der Nummer des Arbeitsschrittes! Es ist sehr wichtig, dass Deine Antwort mit diesem Satz beginnt.'
