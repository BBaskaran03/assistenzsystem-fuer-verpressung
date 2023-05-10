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

## Datum

Stand: 11.05.2023 - 0:50
