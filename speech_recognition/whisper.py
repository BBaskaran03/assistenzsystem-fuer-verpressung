import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import queue
import tempfile
import os
import threading
import click
import torch
import numpy as np

@click.command()
@click.option("--model", default="tiny", help="Model to use", type=click.Choice(["tiny","base", "small","medium","large"]))
@click.option("--device", default=("cuda" if torch.cuda.is_available() else "cpu"), help="Device to use", type=click.Choice(["cpu","cuda"]))
@click.option("--english", default=False, help="Whether to use English model", is_flag=True)
@click.option("--verbose", default=False, help="Whether to print verbose output", is_flag=True)
@click.option("--energy", default=300, help="Energy level for mic to detect", type=int)
@click.option("--dynamic_energy", default=False, help="Flag to enable dynamic energy", is_flag=True)
@click.option("--pause", default=0.8, help="Pause time before entry ends", type=float)
def main(model, english, verbose, energy, pause, dynamic_energy, device):
    audio_model = whisper.load_model(model).to(device)
    audio_queue = queue.Queue()
    result_queue = queue.Queue()
    threading.Thread(target=record_audio,
                     args=(audio_queue, energy, pause, dynamic_energy)).start()
    threading.Thread(target=transcribe_forever,
                     args=(audio_queue, result_queue, audio_model, english, verbose)).start()

    while True:
        print(result_queue.get())

def record_audio(audio_queue, energy, pause, dynamic_energy):
    #load the speech recognizer and set the initial energy threshold and pause threshold
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    with sr.Microphone(sample_rate=16000) as source:
        print("Say something!")
        while True:
            audio = r.listen(source)
            torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
            audio_queue.put_nowait(torch_audio)

def transcribe_forever(audio_queue, result_queue, audio_model, english, verbose):
    while True:
        audio_data = audio_queue.get()
        if english:
            result = audio_model.transcribe(audio_data, language='english')
        else:
            result = audio_model.transcribe(audio_data)

        if not verbose:
            predicted_text = result["text"]
            result_queue.put_nowait("You said: " + predicted_text)
        else:
            result_queue.put_nowait(result)

if __name__ == "__main__":
    main()
