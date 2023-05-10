import speech_recognition as sr
from recognize_speech import recognize_speech
from text_to_speech import speak
from keyword_search import search_for_keywords

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    while(True):
        print("Say something!")
        speech_output = recognize_speech(recognizer, microphone)

        if speech_output["error"]:
            print(f"Error: {speech_output['error']}")
        else:
            print(f"Transcription: {speech_output['transcription']}")

            keyword_output, keyword, prompt = search_for_keywords(speech_output['transcription'])

            if keyword_output == 'pause':
                print(f"Keyword: \"{keyword}\" detected")
            elif keyword_output == 'stop':
                print(f"Keyword: \"{keyword}\" detected")
            elif keyword_output == 'aus':
                print(f"Keyword: \"{keyword}\" detected")
                
            else:
                print(f"No keyword detected")

            if prompt!=None:
                speak(prompt, 'de')

if __name__ == "__main__":
    main()