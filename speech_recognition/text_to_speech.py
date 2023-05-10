from gtts import gTTS
import io
import pygame

def speak(audio_string, language):
    with io.BytesIO() as file:
        tts = gTTS(text=audio_string, lang=language, tld='de', slow=False, lang_check=False)
        tts.write_to_fp(file)
        file.seek(0)

        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            continue
