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
    "PORCUPINE": {"API_KEY": ""},
    "OPENAI": {"API_KEY": "", "DONT QUERY": False},
}
