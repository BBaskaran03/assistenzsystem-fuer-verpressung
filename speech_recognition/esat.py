from whisper_mic.mic import WhisperMic
mic = WhisperMic(timeout=5)
command = mic.listen()