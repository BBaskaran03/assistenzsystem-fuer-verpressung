# Speech Recognition für das Modul Menschzentrierte Robotik

Benutzt Python SpeechRecognition um Sprache zu erkennen und Google TextToSpeech um Sprache auszugeben

Kompatibel für Windows und Linux

- Requirements installierbar mit install_requirements.bat oder install_requirements.sh
  - requirements.txt erstellt durch pipreqs

## Keyword Search

Das Programm besitzt zurzeit 3 verschiedene "States"

1. Pause
2. Stop
3. Aus

Diese States werden in einer while(true) Schleife, durch mithören des Mikrophons und Selektion einzelner Schlüsselwörter, selected.

Schlüsselwörter für die jeweiligen "States" sind

1. "anstrengend", "pause"
2. "aufhören", "ich kann nicht mehr", "keine lust"
3. "aus", "tschüss", "ciao", "bye"

Zurzeit gibt das program nur an, dass es bemerkt hat dass der "State" sich am wechseln ist und fragt nach erlaubnis

## Speech Recognition Variants

Zum Testen der Speech to Text Funktionen wurde ein Satz verwendet, das schwer auszusprechen und schwer zu verstehen ist.
> Ich lade meinen Ballermann und baller dann auf alle Mann in deiner Bande, Motherfucker, bange deine Mama vor der Kamera, der Kanada-germane mit der Gun im Arm ist back. Es ist Kollegah, der Boss.

### Whisper (Offline)

- Large
  - Ausgabe: Ich lade meinen Ballermann und ballert dann auf alle Mann in deiner Bande, Motherfucker, bänge deine Mama vor der Kamera, der kannade gemeine Mitte, Kann im Arbis beckerst, Kollege, der Boss.
  - Dauer: 4 minuten

- Base
  - Ausgabe: Ich schlage auf meine Ball savory properly, wenn du einen Band suck巧ches饒你的ставля es ready you are you can never miss backers koll good boss
  - Dauer: 20 Sekunden

- Tiny
  - Ausgabe: ""
  - Dauer: 6 sekunden

### SpeechRecognizer (Online / Offline)

- recognize_google (online)
  - Ausgabe: Ich lade meinen Ballermann und baller dann auf alle Mann in deiner Bande madafaka bänge deine Mama vor der Kamera der Kanada gemeine Mann der gar nicht mehr mispag ist Kollegah der Boss
  - Dauer: 4 sekunden
- recognize_sphinx (offline)
  - hat keine deutsche library

## Special Acknowledgements

whisper_mic : @mallorbc https://github.com/mallorbc/whisper_mic/blob/main/whisper_mic 
